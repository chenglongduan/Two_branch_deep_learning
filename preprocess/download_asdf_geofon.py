# Download data from IRIS 
# Input: a parameter file
# Output: (1) raw ASDF data, (2) station list
# Author: Ross Maguire, modified by Chenglong Duan, 2023
# Revision history:
# 6/16/2023: correct a bug in output event location

import os
import sys
import obspy
import pyasdf
import numpy as np
import pandas as pd

from sys import argv
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from configobj import ConfigObj
from obspy.geodetics import gps2dist_azimuth

from obspy.core.event.origin import Origin
from obspy.core.event.event import Event
from obspy.core.event.event import EventDescription
from obspy.core.event.source import FocalMechanism
from obspy.core.event.source import MomentTensor
from obspy.core.event.source import Tensor
from obspy.core.event.magnitude import Magnitude
from obspy.core.inventory.network import Network
from obspy.core.inventory.network import Station
from obspy.core.inventory.channel import Channel


def read_param_dict(inparam_file,debug=True):
    params = ConfigObj(inparam_file).dict()
    if debug:
        print('--------------------------------------------------------')
        print('inparam_file: {}'.format(inparam_file)) 
        print('params:')
        print(params)
        print('--------------------------------------------------------')
    return params


def main(params,debug=False):
    f_cat = open(params['catalog'],'r')
    lines = f_cat.readlines()
    n_events = len(lines)
    event_dict = {}

    for line in lines:
        items = line.strip().split()
        year = int(items[0])
        month = int(items[1])
        day = int(items[2])
        hour = int(items[3])
        minute = int(items[4])
        second = int(items[5])
        fsec = int(items[6])
        latitude = float(items[7])
        longitude = float(items[8])
        depth = float(items[9])
        magnitude = float(items[10])
        etype = int(items[11])

        evtid = '{}:{:02d}:{:02d}:{:02d}:{:02d}:{:02d}.{:02d}'.format(year,month,day,hour,minute,second,fsec)
        event_dict[evtid] = {}
        event_dict[evtid]['latitude'] = latitude
        event_dict[evtid]['longitude'] = longitude
        event_dict[evtid]['depth'] = depth
        event_dict[evtid]['magnitude'] = magnitude
        event_dict[evtid]['etype'] = etype

    n_events = len(event_dict)
    event_names = list(event_dict.keys())
    
    #*****************************************
    ncol = 50000
    col1 = np.zeros((ncol, 1),dtype=int)
    col2 = np.zeros((ncol, 5),dtype=np.float32)
    count = 0
    #*****************************************

    #--------------------------------------------------------------------
    #Loop through events
    #--------------------------------------------------------------------
    for i_event in range(0,n_events,1):
        
        #open asdf dataset
        ds = pyasdf.ASDFDataSet(params['filename'])

        print('working on event {} ... ({}/{})'.format(event_names[i_event],i_event+1,n_events))
        iris = Client('https://geofon.gfz-potsdam.de')

        #add metadata to event object
        event_name = event_names[i_event]
        e = Event()
        e.resource_id = obspy.core.event.ResourceIdentifier()

        #description
        descr1 = EventDescription(text=event_name,type='earthquake name')
        e.event_descriptions = [descr1]

        #origins
        origin_time = UTCDateTime(event_name)
        evlo = event_dict[event_name]['longitude']
        evla = event_dict[event_name]['latitude']
        evdp = event_dict[event_name]['depth']
        o1 = Origin(time=origin_time,longitude=evlo,latitude=evla,depth=evdp)
        o1.resource_id = obspy.core.event.origin.ResourceIdentifier()
        e.origins = [o1]

        #magnitude
        m1 = Magnitude(mag=event_dict[event_name]['magnitude'],magnitude_type='Ml')
        m1.resource_id = obspy.core.event.magnitude.ResourceIdentifier()
        e.magnitudes = [m1]

        #event type
        if event_dict[event_name]['etype'] == 0:
            e.event_type = 'explosion'
        elif event_dict[event_name]['etype'] == 1:
            e.event_type = 'earthquake'
        e.event_type_certainty = 'known'

        ds.add_quakeml(e)

        #-----------------------------------------------------------
        #Get stations
        #-----------------------------------------------------------
        starttime = origin_time - float(params['preset'])
        endtime = origin_time + float(params['offset'])
        station_box = params['station_box']
        box_bounds = station_box.split('/')
        minlatitude = float(box_bounds[0])
        maxlatitude = float(box_bounds[1])
        minlongitude = float(box_bounds[2])
        maxlongitude = float(box_bounds[3])

        if type(params['channel'] == list):
            channel = params['channel'][0]
            for chn in params['channel'][1:]:
                channel = channel +',{}'.format(chn)
        else:
            channel = params['channel']

        inv = iris.get_stations(starttime = starttime, endtime = endtime,
                network = params['network'], channel = channel,
                minlatitude=minlatitude, maxlatitude=maxlatitude,
                minlongitude=minlongitude, maxlongitude=maxlongitude, level='response')

        ds.add_stationxml(inv)

        #print(inv) #
        #inv.plot() #
        #inv[0].plot_response(min_freq=1E-4) #

        #-----------------------------------------------------------
        #Get waveform data
        #-----------------------------------------------------------
        for net in inv:
            for sta in net:
        
                stla = sta.latitude
                stlo = sta.longitude
                dist_m, baz, az = gps2dist_azimuth(stla,stlo,evla,evlo)
                dist_km = dist_m / 1000.

                seis = obspy.Stream()

                try:
                    seis = iris.get_waveforms(net.code,sta.code,'*',"BH*",starttime,endtime)
                except:
                    try:
                        seis = iris.get_waveforms(net.code,sta.code,'*',"HH*",starttime,endtime)
                    except:
                        try:
                            seis = iris.get_waveforms(net.code,sta.code,'*',"EH*",starttime,endtime)
                        except:
                            print('could not find any data BH*, HH*, EH* for station {}.{}'.format(net.code,sta.code))

        
                if len(seis) > 1:  #this condition ensures asdf only record multi-component waveforms
                    
                    print(seis) #
                    #seis.plot() #
                    #***********************
                    col1[count] = i_event+1
                    col2[count,0] = evla
                    col2[count,1] = evlo
                    col2[count,2] = stla
                    col2[count,3] = stlo
                    col2[count,4] = dist_km
                    count += 1
                    #************************
                    ds.add_waveforms(seis,tag='raw_recording',event_id=e)
                
                else:
                    continue

    #*************************************************
    df1 = pd.DataFrame(col1)
    df1.rename(columns={0: 'src_count'}, inplace=True)
    df2 = pd.DataFrame(col2)
    df3 = pd.concat([df1,df2],axis=1)
    df4 = df3.iloc[:count]
    df4.to_csv('station_info.csv', sep=' ', header=False, index=False)
    #*************************************************
    
    sys.exit()


params = read_param_dict(argv[1])
main(params)

