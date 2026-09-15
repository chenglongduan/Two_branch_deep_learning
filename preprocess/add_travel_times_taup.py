# Calculate predicted P and S traveltimes using 1D velocity models
# Input: (1) processed ASDF data, (2) taup velocity model
# Output: (1) auxiliary data: P and S traveltimes, (2) log file
# Author: Ross Maguire, modified by Chenglong Duan, 2023
# Revision history:
# 6/23/2023: debug the code
# 9/1/2025: print to real-time monitor the predicted traveltimes


import obspy
import pyasdf
import subprocess
import numpy as np
import pandas as pd
from sys import argv


# perimeter of a fan: 2*pi*R*(theta/360), assume radius of Earth = 6371 km, theta = 1 deg
km_per_degree = (2*np.pi*6371.0)/360.0

input_file = argv[1]
taup_model = argv[2]

ds = pyasdf.ASDFDataSet(input_file)

#remove travel times if they exist
try:
    del ds.auxiliary_data.travel_times
except:
    pass

n_events = len(ds.events)


for i_ev,event in enumerate(ds.events):
    print('event: {}/{}'.format(i_ev+1,n_events))

    origin = event.preferred_origin() or event.origins[0]
    event_name = '{}'.format(origin.time)
    event_depth = origin.depth

    #some explosion event depths are above sea level (negative depth)
    if event_depth < 0:
        event_depth = 0.0

    d = ds.auxiliary_data.distances.distances[event_name]
    distance_dict = d.parameters

    P_time_dict = {}
    S_time_dict = {}
    P_times = []
    S_times = []
    store_P_times = []  # clduan
    store_S_times = []  # clduan

    for station in ds.ifilter(ds.q.event == event):

        #get stream
        seis = station.processed
        net_code = seis[0].stats.network
        sta_code = seis[0].stats.station

        #get distance
        dist = distance_dict['{}.{}'.format(net_code,sta_code)]
        dist_degree = dist / km_per_degree

        a = subprocess.Popen('taup_time -mod {} -h {} -deg {} -ph P,p --time'.format(taup_model,event_depth,dist_degree),stdout=subprocess.PIPE,shell=True)
        b = subprocess.Popen('taup_time -mod {} -h {} -deg {} -ph S,s --time'.format(taup_model,event_depth,dist_degree),stdout=subprocess.PIPE,shell=True)
        P_arrs = a.stdout.read()
        S_arrs = b.stdout.read()

        P_times = P_arrs.split()
        S_times = S_arrs.split()

        if len(P_times) == 0 or len(S_times) == 0:  # ensure both Tp and Ts are not empty
            print(f'  traveltime missing for {net_code}.{sta_code}: dist = {dist} km, event_depth = {event_depth} km')
            #print('  {} {}'.format(P_times,S_times))
            continue

        else:
            P_time = float(P_arrs.split()[0])
            S_time = float(S_arrs.split()[0])
        
        print(f'{net_code}.{sta_code}: Tp={P_time}, Ts={S_time}')

        P_time_dict['{}.{}'.format(net_code,sta_code)] = P_time
        S_time_dict['{}.{}'.format(net_code,sta_code)] = S_time
        store_P_times.append(P_time)  #P_times.append(P_time)   clduan
        store_S_times.append(S_time)  #S_times.append(S_time)   clduan

    ds.add_auxiliary_data(data = np.array(store_P_times), data_type = 'travel_times', path = 'P_times/{}'.format(origin.time), parameters = P_time_dict) #np.array(P_times)  clduan
    ds.add_auxiliary_data(data = np.array(store_S_times), data_type = 'travel_times', path = 'S_times/{}'.format(origin.time), parameters = S_time_dict) #np.array(S_times)  clduan



