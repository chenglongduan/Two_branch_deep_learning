import os
import obspy
import pyasdf
import numpy as np
from sys import argv
import seisbench.models as sbm
from scipy.interpolate import PchipInterpolator
from obspy.signal.invsim import cosine_taper


#read data
input_file = argv[1]
dataset_name = argv[2]
outdir_image = argv[3]
augment = argv[4].lower()=='true'
aug_type = "explosion" if argv[5] == "EX" else "earthquake" if argv[5] == "EQ" else "unknown"
dset_repeattimes = int(argv[6])

#make outdir if it doesn't exist
outdir_label = argv[7]
outdir_ascii = argv[8]
if not os.path.exists(outdir_image):
    os.makedirs(outdir_image)
if not os.path.exists(outdir_label):
    os.makedirs(outdir_label)
if not os.path.exists(outdir_ascii):
    os.makedirs(outdir_ascii)

#waveform characterisics
preset = 120.0
offset = 120.0
dist_max = 300.0
snr_min = 2.0
psr_max = 5.0
min_mag = 0.5
max_mag = 5.0
asdf_aux_f1 = 6.0
asdf_aux_f2 = 18.0

#phasenet characterisics
slice_waveform = True
time_before_P = 10.0
time_after_P = 80.0
sig_len = time_before_P + time_after_P
TF_filter = True
f_min = 1.0
f_max = 18.0

#count
n_good = 0
#-------------------------------------------------


ds = pyasdf.ASDFDataSet(input_file)

seisbench_model = sbm.PhaseNet.from_pretrained('stead')

labels = open(f"{outdir_label}/labels_phasenet_{dataset_name}.csv", 'w')

for i_ev,event in enumerate(ds.events):

    origin = event.preferred_origin() or event.origins[0]
    event_name = '{}'.format(origin.time)
    evlo = origin.longitude
    evla = origin.latitude
    evdp = origin.depth

    if event.event_type == 'explosion':
        e_type = 1
    elif event.event_type == 'earthquake':
        e_type = 0
        e_mag = event.magnitudes[0].mag

    distances = ds.auxiliary_data.distances.distances[event_name].parameters
    ps_ratios = ds.auxiliary_data.PS_ratios['{}'.format(event_name)]['f_{:2.2f}_{:2.2f}'.format(asdf_aux_f1,asdf_aux_f2)].parameters
    snr = ds.auxiliary_data.SNR['{}'.format(event_name)]['f_{:2.2f}_{:2.2f}'.format(asdf_aux_f1,asdf_aux_f2)].parameters
    P_times = ds.auxiliary_data.travel_times.P_times[event_name].parameters
    S_times = ds.auxiliary_data.travel_times.S_times[event_name].parameters

    for station in ds.ifilter(ds.q.event == event):

        inv = station.StationXML
        stla = inv[0][0].latitude
        stlo = inv[0][0].longitude

        seis = station.processed
        net_code = seis[0].stats.network
        sta_code = seis[0].stats.station
        samprate = seis[0].stats.sampling_rate

        try:
            ps_here = ps_ratios['{}.{}'.format(net_code,sta_code)]
            dist_here = distances['{}.{}'.format(net_code,sta_code)]
            snr_here = snr['{}.{}'.format(net_code,sta_code)]
            P_time = P_times['{}.{}'.format(net_code,sta_code)]
            S_time = S_times['{}.{}'.format(net_code,sta_code)]
        except KeyError:
            print('missing auxiliary data for {}.{}'.format(net_code,sta_code))
            continue
        
        if snr_here >= snr_min and dist_here < dist_max:

            if slice_waveform:
                starttime = seis[0].stats.starttime
                new_start = starttime + preset + P_time - time_before_P
                new_end = new_start + sig_len

                noise_start = starttime
                noise_end = noise_start + sig_len

                signal = seis.copy().slice(starttime=new_start,endtime=new_end)
                noise = seis.copy().slice(starttime=noise_start,endtime=noise_end)

                if signal[0].stats.npts != noise[0].stats.npts:
                    print(f"sliced unequal npts for {net_code}.{sta_code} (dist={dist_here}): signal={signal[0].stats.npts}, noise={noise[0].stats.npts}")
                    continue

                #apply a random shift to whole trace
                #t_shift_max = 2.0
                #ind_shift_max = int(samprate * t_shift_max)
                #ind_shift = np.random.randint(-ind_shift_max,ind_shift_max) #if ind_shift_max > 0 else 0
                #for tr in signal:
                #    tr.data = np.roll(tr.data,ind_shift)

            #skip if not 3-C traces
            try:
                trz = signal.select(channel='*HZ')[0]
                trr = signal.select(channel='*HR')[0]
                trt = signal.select(channel='*HT')[0]

                nrz = noise.select(channel='*HZ')[0]
                nrr = noise.select(channel='*HR')[0]
                nrt = noise.select(channel='*HT')[0]
            except:
                print(f"no 3C traces for {net_code}.{sta_code}")
                continue

            # standard final
            npts = trz.stats.npts
            dt = trz.stats.delta
            datetime0 = trz.stats.starttime
            T_total = (npts-1)*dt
            
            # taper
            taper = cosine_taper(len(trz.data),0.1)
            trz.data *= taper
            trr.data *= taper
            trt.data *= taper
            
            #=======================
            tmp_sig = signal.copy()
            
            if TF_filter:
                tmp_sig.filter('bandpass', freqmin=f_min, freqmax=f_max, corners=2, zerophase=True)
            
            tmp_sig.resample(100.0, window='hann')
            try:
                seis_picks = seisbench_model.annotate(tmp_sig)
            except:
                print('seisbench not work for {}.{}'.format(net_code,sta_code))
                continue
            
            trP = seis_picks.select(component='P')[0]
            trS = seis_picks.select(component='S')[0]
            
            NT_picks = seis_picks[0].stats.npts
            NT_correct = int(T_total * 100.0) + 1
            array_P = np.zeros(NT_correct)
            array_S = np.zeros(NT_correct)
            t_delay = seis_picks[0].stats.starttime - datetime0
            it_delay = int(abs(t_delay) * 100.0)
        
            array_P[it_delay:it_delay+NT_picks] = trP.data
            array_S[it_delay:it_delay+NT_picks] = trS.data
            
            t = np.linspace(0, T_total, NT_correct)
            
            #interpolate onto new grid
            npts_t_new = 4000
            t_i = np.linspace(0, T_total, npts_t_new)
            
            PN_P = PchipInterpolator(t, array_P)(t_i)
            PN_S = PchipInterpolator(t, array_S)(t_i)
            #=======================

            #stack time series to single 2 x N array
            pickprob_2comp = np.array((PN_P,PN_S))
            
            print('{}.{} saved'.format(net_code,sta_code))
            n_good += 1
            outname1 = '{}_{:04d}'.format(dataset_name,n_good)
            
            #write pick probs
            np.save(f"{outdir_image}/{outname1}",np.abs(pickprob_2comp))

            #write labels
            labels.write('{}/{}.npy, {}, {}, {:6.4f}, {:6.4f}, {:6.4f}, {:6.4f}, {}, {}, {:6.4f}, {:6.4f}, {:6.4f}, {:6.4f}\n'.format(outdir_image,outname1,e_type,event_name,dist_here,evlo,evla,evdp,net_code,sta_code,stlo,stla,ps_here,snr_here))
            
            #write ascii files
            out_asc1 = np.column_stack((t,tmp_sig.select(channel="*HZ")[0].data[:NT_correct],tmp_sig.select(channel="*HR")[0].data[:NT_correct],tmp_sig.select(channel="*HT")[0].data[:NT_correct]))
            np.savetxt(f"{outdir_ascii}/wfm_{n_good:04d}.{net_code}.{sta_code}", out_asc1)

            
            #==========use data augmentation for the minority class=============
            if augment and event.event_type == aug_type:
                
                for j in range(0,dset_repeattimes):

                    data_z = trz.copy().data
                    data_r = trr.copy().data
                    data_t = trt.copy().data

                    noise_z = nrz.copy().data
                    noise_r = nrr.copy().data
                    noise_t = nrt.copy().data

                    noise_level = 1.
                    scale_max = np.random.random() * noise_level
                    noise_z *= scale_max
                    noise_r *= scale_max
                    noise_t *= scale_max

                    #apply a random shift to noise
                    t_shift_max_noise = sig_len
                    ind_shift_max_noise = int(samprate * t_shift_max_noise)
                    ind_shift_noise = np.random.randint(-ind_shift_max_noise,ind_shift_max_noise)
                    noise_z = np.roll(noise_z,ind_shift_noise)
                    noise_r = np.roll(noise_r,ind_shift_noise)
                    noise_t = np.roll(noise_t,ind_shift_noise)

                    data_z = data_z + noise_z[0:npts]
                    data_r = data_r + noise_r[0:npts]
                    data_t = data_t + noise_t[0:npts]

                    #apply a random shift to whole trace
                    #first, undo the intitial shift so it doesn't get shifted twice
                    #data_z = np.roll(data_z,-ind_shift)
                    #data_r = np.roll(data_r,-ind_shift)
                    #data_t = np.roll(data_t,-ind_shift)

                    #next, randomly shift by up to 2 s
                    #t_shift_max_2 = 2.0
                    #ind_shift_max_2 = int(samprate * t_shift_max_2)
                    #ind_shift_2 = np.random.randint(-ind_shift_max_2,ind_shift_max_2)
                    #data_z = np.roll(data_z,ind_shift_2)
                    #data_r = np.roll(data_r,ind_shift_2)
                    #data_t = np.roll(data_t,ind_shift_2)
                    
                    # taper
                    taper2 = cosine_taper(len(data_z),0.1)
                    data_z *= taper2
                    data_r *= taper2
                    data_t *= taper2

                    #make new stream
                    signal_aug = signal.copy()
                    signal_aug.select(channel="*HZ")[0].data = data_z
                    signal_aug.select(channel="*HR")[0].data = data_r
                    signal_aug.select(channel="*HT")[0].data = data_t
                    
                    #=======================
                    if TF_filter:
                        signal_aug.filter('bandpass', freqmin=f_min, freqmax=f_max, corners=2, zerophase=True)
                    
                    signal_aug.resample(100.0, window='hann')
                    try:
                        seis_picks_aug = seisbench_model.annotate(signal_aug)
                    except:
                        print('seisbench not work for {}.{}'.format(net_code,sta_code))
                        continue
            
                    trP_aug = seis_picks_aug.select(component='P')[0]
                    trS_aug = seis_picks_aug.select(component='S')[0]
                    
                    array_P_aug = np.zeros(NT_correct)
                    array_S_aug = np.zeros(NT_correct)
        
                    array_P_aug[it_delay:it_delay+NT_picks] = trP_aug.data
                    array_S_aug[it_delay:it_delay+NT_picks] = trS_aug.data
            
                    PN_P_aug = PchipInterpolator(t, array_P_aug)(t_i)
                    PN_S_aug = PchipInterpolator(t, array_S_aug)(t_i)
                    #=======================

                    #stack time series to single 2 x N array
                    pickprob_2comp_aug = np.array((PN_P_aug,PN_S_aug))
                    
                    print('{}.{} (augment) saved'.format(net_code,sta_code))
                    n_good += 1
                    outname2 = '{}_{:04d}_augmented'.format(dataset_name,n_good)
                    
                    #write pick probs
                    np.save(f"{outdir_image}/{outname2}",np.abs(pickprob_2comp_aug))

                    #write labels
                    labels.write('{}/{}.npy, {}, {}, {:6.4f}, {:6.4f}, {:6.4f}, {:6.4f}, {}, {}, {:6.4f}, {:6.4f}, {:6.4f}, {:6.4f}\n'.format(outdir_image,outname2,e_type,event_name,dist_here,evlo,evla,evdp,net_code,sta_code,stlo,stla,ps_here,snr_here))
                    
                    #write ascii files
                    #out_asc2 = np.column_stack((t,signal_aug.select(channel="*HZ")[0].data[:NT_correct],signal_aug.select(channel="*HR")[0].data[:NT_correct],signal_aug.select(channel="*HT")[0].data[:NT_correct]))
                    #np.savetxt(f"{outdir_ascii}/wfm_{n_good:04d}_aug.{net_code}.{sta_code}", out_asc2)

        else:
            print(f"{net_code}.{sta_code} not satisfy SNR,dist criteria")

labels.close()
