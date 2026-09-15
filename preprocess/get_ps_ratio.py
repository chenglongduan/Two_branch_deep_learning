# Calculate P/S ratios and SNRs within time windows
# Input: processed ASDF data
# Output: (1) auxiliary data: P/S ratios, (2) auxiliary data: SNRs, (3) log file
# Author: Ross Maguire, modified by Chenglong Duan, 2023
# Revision history:
# 6/23/2023: debug the code, add a runtime log file
# 1/18/2024: add an option to output time window ranges
# 1/18/2024: max (saturated) time window changes to 4 sec (previous is 3 sec)
# 1/18/2024: skip the trace if np.isnan(SNR) is True


import obspy
import pyasdf
import numpy as np
import pandas as pd
from sys import argv

input_file = argv[1]
out_twin_dir = argv[2]
ds = pyasdf.ASDFDataSet(input_file)

#==================================
TF_filter = True
fmin = 6.0
fmax = 18.0

TF_output_twin = True
#==================================


#delete auxiliary data if exists
try:
    del ds.auxiliary_data.PS_ratios
    del ds.auxiliary_data.SNR
except:
    pass


n_events = len(ds.events)
loginfo = np.zeros((n_events, 6),dtype=int)


for iev,event in enumerate(ds.events):
    
    print('event: {}/{}'.format(iev+1,n_events))
    loginfo[iev,0] = iev+1
    
    if TF_output_twin:
        n_twin = 0
        twininfo = np.zeros((1000, 9),dtype=object) # output time windows

    origin = event.preferred_origin() or event.origins[0]
    event_name = '{}'.format(origin.time)

    ad1 = ds.auxiliary_data.distances.distances[event_name]
    distance_dict = ad1.parameters

    ad2 = ds.auxiliary_data.travel_times.P_times[event_name]
    P_time_dict = ad2.parameters

    ad3 = ds.auxiliary_data.travel_times.S_times[event_name]
    S_time_dict = ad3.parameters

    SNR_dict = {}
    PS_ratio_dict = {}
    SNRs = []
    PS_ratios = []
    

    for station in ds.ifilter(ds.q.event == event):

        #get stream
        seis = station.processed
        net_code = seis[0].stats.network
        sta_code = seis[0].stats.station

        #get distance and traveltimes
        try:
            dist = distance_dict['{}.{}'.format(net_code,sta_code)]
        except:
            print('No distance found for {}.{}'.format(net_code,sta_code))
            continue
        
        try:
            P_time = P_time_dict['{}.{}'.format(net_code,sta_code)]
            S_time = S_time_dict['{}.{}'.format(net_code,sta_code)]
        except:
            print('No P or S time found for {}.{}'.format(net_code,sta_code))
            loginfo[iev,2] += 1
            continue

        if TF_filter:
            seis.filter('bandpass',freqmin=fmin,freqmax=fmax,corners=2,zerophase=True)
        
        #calculate P/S ratios, SNR
        components = [tr.stats.channel[-1] for tr in seis]

        if "R" in components and "T" in components and "Z" in components:

            trZ = seis.select(channel = '*HZ')[0]
            trR = seis.select(channel = '*HR')[0]
            trT = seis.select(channel = '*HT')[0]
            net_code = trZ.stats.network
            sta_code = trZ.stats.station

            #set relative time window (t0=0s)
            W = (S_time - P_time)*0.5
            if W < 1:
                loginfo[iev,3] += 1
                continue
            elif W > 4:  # elif W > 3:
                W = 4    # W = 3

            P2 = P_time - (W*0.05)
            S2 = S_time - (W*0.05)
            N = 9.0
            
            #set datatime time window
            starttime_P = origin.time + P2
            starttime_S = origin.time + S2
            starttime_N = origin.time - N
            endtime_P = starttime_P + W
            endtime_S = starttime_S + W
            endtime_N = starttime_N + W
            
            #save relative time window (t0=0s)
            if TF_output_twin:
                twininfo[n_twin,0] = net_code
                twininfo[n_twin,1] = sta_code
                twininfo[n_twin,2] = dist
                twininfo[n_twin,3] = P2
                twininfo[n_twin,4] = P2+W
                twininfo[n_twin,5] = S2
                twininfo[n_twin,6] = S2+W
                twininfo[n_twin,7] = -N
                twininfo[n_twin,8] = -N+W
                n_twin += 1
            

            P_winZ = trZ.slice(starttime=starttime_P,endtime=endtime_P)
            P_winR = trR.slice(starttime=starttime_P,endtime=endtime_P)
            P_winT = trT.slice(starttime=starttime_P,endtime=endtime_P)
            S_winZ = trZ.slice(starttime=starttime_S,endtime=endtime_S)
            S_winR = trR.slice(starttime=starttime_S,endtime=endtime_S)
            S_winT = trT.slice(starttime=starttime_S,endtime=endtime_S)
            N_winZ = trZ.slice(starttime=starttime_N,endtime=endtime_N)
            N_winR = trR.slice(starttime=starttime_N,endtime=endtime_N)
            N_winT = trT.slice(starttime=starttime_N,endtime=endtime_N)
            
            
            #scale and take RMS amplitude
            P_Z = np.mean((P_winZ.data*1e9)**2)
            P_R = np.mean((P_winR.data*1e9)**2)
            P_T = np.mean((P_winT.data*1e9)**2)
            S_Z = np.mean((S_winZ.data*1e9)**2)
            S_R = np.mean((S_winR.data*1e9)**2)
            S_T = np.mean((S_winT.data*1e9)**2)
            N_Z = np.mean((N_winZ.data*1e9)**2)
            N_R = np.mean((N_winR.data*1e9)**2)
            N_T = np.mean((N_winT.data*1e9)**2)
            
            #print((P_Z+P_R+P_T), (S_Z+S_R+S_T), (N_Z+N_R+N_T))


            P_sum = np.sqrt( (P_Z+P_R+P_T) - (N_Z+N_R+N_T) )
            S_sum = np.sqrt( (S_Z+S_R+S_T) - (N_Z+N_R+N_T) )
            #P_sum = np.sqrt( P_Z + P_R + P_T )
            #S_sum = np.sqrt( S_Z + S_R + S_T )
            N_sum = np.sqrt( N_Z + N_R + N_T )

            PS_ratio = P_sum / S_sum
            SNR = P_sum / N_sum
            
            if (np.isnan(PS_ratio)):
                print('PS_ratio=NaN for {}.{}'.format(net_code,sta_code))
                loginfo[iev,4] += 1
                continue
            
            if (np.isnan(SNR)):
                print('SNR=NaN for {}.{}'.format(net_code,sta_code))
                loginfo[iev,5] += 1
                continue
                
            if (not np.isnan(PS_ratio)) and (not np.isnan(SNR)):
                loginfo[iev,1] += 1

            #print(N_sum,S_sum)
            #print('PS_ratio, SNR: {}, {}'.format(PS_ratio,SNR))
            #print('\n')  # clduan

            SNRs.append(SNR)
            PS_ratios.append(PS_ratio)

            SNR_dict['{}.{}'.format(net_code,sta_code)] = SNR
            PS_ratio_dict['{}.{}'.format(net_code,sta_code)] = PS_ratio

        else:
            print('**************************************')
            print('Z, R, and T components not available')
            print(seis)
            print('**************************************\n')
            continue

    # output event-based parameters
    ds.add_auxiliary_data(data = np.array(PS_ratios), data_type = 'PS_ratios',
            path = '{}/f_{:2.2f}_{:2.2f}'.format(event_name,fmin,fmax), parameters = PS_ratio_dict)
    ds.add_auxiliary_data(data = np.array(SNRs), data_type = 'SNR',
            path = '{}/f_{:2.2f}_{:2.2f}'.format(event_name,fmin,fmax), parameters = SNR_dict)
    
    if TF_output_twin:
        df_twin = pd.DataFrame(twininfo[0:n_twin,:])
        df_twin.to_csv(out_twin_dir+'event_{}.csv'.format(iev+1), sep=' ', header=False, index=False)


df1 = pd.DataFrame(loginfo)
df1.columns = ["event", "success", "no_traveltimes", "bad_time_window", "NaN_PS_ratio", "NaN_SNR"]
df1.to_csv('log_psratio.csv', sep=' ', header=True, index=False)
