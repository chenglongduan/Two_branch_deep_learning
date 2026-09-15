# Pre-process the data using the workflow in README file
# Input: (1) raw ASDF data, (2) filename of the output file
# Output: (1) processed ASDF data, (2) auxiliary data: distance, (3) processing log file
# Author: Ross Maguire, modified by Chenglong Duan, 2023
# Revision history:
# 6/19/2023: do tapering on the whole raw data normally to avoid any FFT artifacts;
#            after that, truncate to exclude the tapering parts at both ends (because tapering part may lead to fake waveform attributes)
# 1/15/2024: add "try...except..." in detrend part after removing instrument response.
# 1/17/2024: add final RTZ rotation check to make sure the data only have R,T,Z three components


import pyasdf
import numpy as np
from sys import argv
from obspy.geodetics import gps2dist_azimuth
import pandas as pd

input_file = argv[1]
output_file = argv[2]

ds = pyasdf.ASDFDataSet(input_file)
ds_out = pyasdf.ASDFDataSet(output_file)

#================================
pre_filt = (0.005,0.01,18.0,20.0)
sample_rate_new = 40.0
taper_percent = 0.05
preset = 120.0  #10.0
offset = 120.0  #110.0
#================================

req_time = preset+offset
npts = int(req_time*sample_rate_new)

n_events = len(ds.events)
loginfo = np.zeros((n_events, 9),dtype=int)


for iev,event in enumerate(ds.events):

    print('working on {} ({}/{})'.format(event,iev+1,n_events))    
    
    loginfo[iev,0] = iev+1

    origin = event.preferred_origin() or event.origins[0]
    event_latitude = origin.latitude
    event_longitude = origin.longitude
    starttime = origin.time - preset

    distance_dict = {}
    distances = []

    ds_out.add_quakeml(event)

    for station in ds.ifilter(ds.q.event == event):

        inv = station.StationXML
        if inv is None:
            print('NO STATION INVENTORY... skip')
            loginfo[iev,2] += 1
            continue
        
        station_latitude = station.coordinates['latitude']
        station_longitude = station.coordinates['longitude']

        seis = station.raw_recording
        print('***RAW seis***')
        print(seis)
        
        if len(seis) < 3:
            print('LESS THAN 3 COMPONENTS... skip')
            loginfo[iev,3] += 1
            continue
        elif seis[1].stats.sampling_rate != seis[0].stats.sampling_rate or seis[2].stats.sampling_rate != seis[0].stats.sampling_rate:
            print('TRACES HAVE DIFFERENT SAMPLE RATE... skip')
            loginfo[iev,4] += 1
            continue

        # pre-processing starts from here...
        seis.detrend('linear')
        seis.detrend('demean')
        seis.taper(max_percentage=taper_percent,type='hann')
        seis.attach_response(inv)

        try:
            seis.remove_response(output="DISP", pre_filt=pre_filt, zero_mean=False, taper=False)
        except:
            print('CANNOT REMOVE RESPONSE... skip')
            loginfo[iev,5] += 1
            continue

        try:
            seis.detrend('linear')
            seis.detrend('demean')
            #seis.taper(max_percentage=taper_percent,type='hann')
        except:
            loginfo[iev,8] += 1
            continue
        
        #seis.filter('bandpass',freqmin=bpfmin,freqmax=bpfmax,zerophase=True)
        
        seis.resample(sample_rate_new,window='hann')
        try:
            seis.interpolate(sampling_rate=sample_rate_new, starttime=starttime, npts=npts)
        except:
            print('WARNING: interpolation failed for {}... skip'.format(seis[0].stats.station))
            loginfo[iev,6] += 1
            continue
        
        print('===RESAMPLED seis===')
        print(seis)
        
        if len(seis) > 3:
            try:
                seis.merge()
                assert(len(seis) == 3)
                print('===MERGED seis===')
                print(seis)
            except:
                try:
                    seis = seis.select(location="01")
                    assert(len(seis) == 3)
                    print('===SELECTED seis===')
                    print(seis)
                except:
                    print('----------------------------')
                    print('WARNING: len > 3 but cannot merge... skip')
                    print('----------------------------')
                    loginfo[iev,7] += 1
                    continue
        

        #calculate distance and rotate
        dist_m, baz, az = gps2dist_azimuth(station_latitude,
                                           station_longitude,
                                           event_latitude,
                                           event_longitude)
        
        components = [tr.stats.channel[-1] for tr in seis]
        
        if "N" in components and "E" in components:
            seis.rotate(method="NE->RT", back_azimuth=baz)

        elif "1" in components and "2" in components:
            seis.rotate(method="->ZNE",inventory=inv)
            seis.rotate(method="NE->RT",back_azimuth=baz)

        # final check
        comp_rot = [tr.stats.channel[-1] for tr in seis]
        if "R" in comp_rot and "T" in comp_rot and "Z" in comp_rot:
            print('===ROTATED seis===')
            print(seis)
            loginfo[iev,1] += 1
        else:
            print('LESS THAN 3 COMPONENTS(RTZ rotation fail)... skip')
            loginfo[iev,3] += 1
            continue
        
        
        #add station
        ds_out.add_stationxml(inv)
        
        #add processed waveform
        ds_out.add_waveforms(seis,event_id=event,tag='processed')
        
        #build distance dict
        for tr in seis:
            tr.stats.distance = dist_m / 1000.0
            print('distance {} km'.format(tr.stats.distance))

        print('\n')
        
        distance_dict['{}.{}'.format(tr.stats.network,tr.stats.station)] = dist_m / 1000.0
        distances.append(dist_m / 1000.)

    
    ds_out.add_auxiliary_data(data = np.array(distances), data_type='distances', path = 'distances/{}'.format(origin.time), parameters = distance_dict)


df1 = pd.DataFrame(loginfo)
df1.columns = ["event", "success", "no_inventory", "comp_less_3", "different_rate", "fail_resp", "fail_interp", "fail_merge3C", "fail_detrend"]
df1.to_csv('log_process.csv', sep=' ', header=True, index=False)
