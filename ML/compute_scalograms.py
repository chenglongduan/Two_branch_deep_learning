import os
import obspy
import pyasdf
import numpy as np
from sys import argv
from obspy.signal.tf_misfit import cwt
#from scipy.interpolate import interp2d
from scipy.interpolate import RectBivariateSpline
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
if not os.path.exists(outdir_image):
    os.makedirs(outdir_image)
if not os.path.exists(outdir_label):
    os.makedirs(outdir_label)

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

#scalogram characterisics
slice_scalogram = True
normalize = argv[8]  # 'spec_max' (default), 'acorr', 'xcorr', 'zcorr'
time_before_P = 10.0
time_after_P = 80.0
sig_len = time_before_P + time_after_P
f_min = 2.0
f_max = 18.0

#count
n_good = 0

debug=False
#-------------------------------------------------


ds = pyasdf.ASDFDataSet(input_file)
labels = open(f"{outdir_label}/labels_scalogram_{dataset_name}.csv", 'w')

for i_ev,event in enumerate(ds.events):

    if debug:
        #print('working in debug mode... exit after 1 event')
        if i_ev > 0:
            break

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
        #if e_mag < min_mag or e_mag > max_mag:
        #    print('skipping event... magnitude {} is outside range {} - {}'.format(e_mag,min_mag,max_mag))

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

            if slice_scalogram:
                starttime = seis[0].stats.starttime
                new_start = starttime + preset + P_time - time_before_P
                new_end = new_start + sig_len

                noise_start = starttime
                noise_end = noise_start + sig_len

                noise = seis.copy().slice(starttime=noise_start,endtime=noise_end)
                signal = seis.copy().slice(starttime=new_start,endtime=new_end)
                noise.taper(0.05)
                signal.taper(0.05)

                if signal[0].stats.npts != noise[0].stats.npts:
                    print(f"sliced unequal npts for {net_code}.{sta_code}: signal={signal[0].stats.npts}, noise={noise[0].stats.npts}")
                    continue

                #apply a random shift to whole trace
                t_shift_max = 2.0
                ind_shift_max = int(samprate * t_shift_max)
                ind_shift = np.random.randint(-ind_shift_max,ind_shift_max) #if ind_shift_max > 0 else 0
                for tr in signal:
                    tr.data = np.roll(tr.data,ind_shift)

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

            npts = trz.stats.npts
            dt = trz.stats.delta
            #print(npts*dt)

            #apply cosine taper to shifted data before scalogram calculation
            taper = cosine_taper(len(trz.data),0.1)
            trz.data *= taper
            trr.data *= taper
            trt.data *= taper

            scalogram_z = cwt(trz.data, dt, 8, f_min, f_max)
            scalogram_r = cwt(trr.data, dt, 8, f_min, f_max)
            scalogram_t = cwt(trt.data, dt, 8, f_min, f_max)

            t = np.linspace(0, (npts-1)*dt, npts)
            f = np.linspace(f_min, f_max, scalogram_z.shape[0])

            #interpolate onto new grid
            npts_t_new = 400
            npts_f_new = 50
            t_i = np.linspace(0, (npts-1)*dt, npts_t_new)
            f_i = np.linspace(f_min, f_max, npts_f_new)
            
            func_z = RectBivariateSpline(f, t, np.abs(scalogram_z))
            func_r = RectBivariateSpline(f, t, np.abs(scalogram_r))
            func_t = RectBivariateSpline(f, t, np.abs(scalogram_t))
            
            scalogram_z = func_z(f_i, t_i)
            scalogram_r = func_r(f_i, t_i)
            scalogram_t = func_t(f_i, t_i)

            if normalize == 'zcorr':
                scalogram_z_norm = scalogram_z / np.max(scalogram_z)
                xcc_zr = scalogram_z * scalogram_r
                xcc_zt = scalogram_z * scalogram_t
                scalogram_r_norm = xcc_zr / np.max(xcc_zr)
                scalogram_t_norm = xcc_zt / np.max(xcc_zt)
            elif normalize == 'acorr':
                acc_zz = scalogram_z * scalogram_z
                acc_rr = scalogram_r * scalogram_r
                acc_tt = scalogram_t * scalogram_t
                scalogram_z_norm = acc_zz / np.max(acc_zz)
                scalogram_r_norm = acc_rr / np.max(acc_rr)
                scalogram_t_norm = acc_tt / np.max(acc_tt)
            elif normalize == 'xcorr':
                xcc_zr = scalogram_z * scalogram_r
                xcc_zt = scalogram_z * scalogram_t
                xcc_rt = scalogram_r * scalogram_t
                scalogram_z_norm = xcc_zr / np.max(xcc_zr)
                scalogram_r_norm = xcc_zt / np.max(xcc_zt)
                scalogram_t_norm = xcc_rt / np.max(xcc_rt)
            else:
                scalogram_z_norm = scalogram_z / np.max(scalogram_z)
                scalogram_r_norm = scalogram_r / np.max(scalogram_r)
                scalogram_t_norm = scalogram_t / np.max(scalogram_t)

            #stack images to single 3 x N x M array
            scalogram_3comp = np.array((scalogram_z_norm,scalogram_r_norm,scalogram_t_norm))
            
            print('{}.{} saved'.format(net_code,sta_code))
            n_good += 1
            outname1 = '{}_{:04d}'.format(dataset_name,n_good)
            
            #write scalograms
            np.save(f"{outdir_image}/{outname1}",np.abs(scalogram_3comp))

            #write labels
            labels.write('{}/{}.npy, {}, {}, {:6.4f}, {:6.4f}, {:6.4f}, {:6.4f}, {}, {}, {:6.4f}, {:6.4f}, {:6.4f}, {:6.4f}\n'.format(outdir_image,outname1,e_type,event_name,dist_here,evlo,evla,evdp,net_code,sta_code,stlo,stla,ps_here,snr_here))

            
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
                    data_z = np.roll(data_z,-ind_shift)
                    data_r = np.roll(data_r,-ind_shift)
                    data_t = np.roll(data_t,-ind_shift)

                    #next, randomly shift by up to 2 s
                    t_shift_max_2 = 2.0
                    ind_shift_max_2 = int(samprate * t_shift_max_2)
                    ind_shift_2 = np.random.randint(-ind_shift_max_2,ind_shift_max_2)
                    data_z = np.roll(data_z,ind_shift_2)
                    data_r = np.roll(data_r,ind_shift_2)
                    data_t = np.roll(data_t,ind_shift_2)

                    #apply cosine taper to shifted data before scalogram calculation
                    taper2 = cosine_taper(len(data_z),0.1)
                    data_z *= taper2
                    data_r *= taper2
                    data_t *= taper2

                    scalogram_z_aug = cwt(data_z, dt, 8, f_min, f_max)
                    scalogram_r_aug = cwt(data_r, dt, 8, f_min, f_max)
                    scalogram_t_aug = cwt(data_t, dt, 8, f_min, f_max)
                    
                    func_z_aug = RectBivariateSpline(f, t, np.abs(scalogram_z_aug))
                    func_r_aug = RectBivariateSpline(f, t, np.abs(scalogram_r_aug))
                    func_t_aug = RectBivariateSpline(f, t, np.abs(scalogram_t_aug))
            
                    scalogram_z_aug = func_z_aug(f_i, t_i)
                    scalogram_r_aug = func_r_aug(f_i, t_i)
                    scalogram_t_aug = func_t_aug(f_i, t_i)
                    
                    if normalize == 'zcorr':
                        scalogram_z_aug_norm = scalogram_z_aug / np.max(scalogram_z_aug)
                        xcc_zr_aug = scalogram_z_aug * scalogram_r_aug
                        xcc_zt_aug = scalogram_z_aug * scalogram_t_aug
                        scalogram_r_aug_norm = xcc_zr_aug / np.max(xcc_zr_aug)
                        scalogram_t_aug_norm = xcc_zt_aug / np.max(xcc_zt_aug)
                    elif normalize == 'acorr':
                        acc_zz_aug = scalogram_z_aug * scalogram_z_aug
                        acc_rr_aug = scalogram_r_aug * scalogram_r_aug
                        acc_tt_aug = scalogram_t_aug * scalogram_t_aug
                        scalogram_z_aug_norm = acc_zz_aug / np.max(acc_zz_aug)
                        scalogram_r_aug_norm = acc_rr_aug / np.max(acc_rr_aug)
                        scalogram_t_aug_norm = acc_tt_aug / np.max(acc_tt_aug)
                    elif normalize == 'xcorr':
                        xcc_zr_aug = scalogram_z_aug * scalogram_r_aug
                        xcc_zt_aug = scalogram_z_aug * scalogram_t_aug
                        xcc_rt_aug = scalogram_r_aug * scalogram_t_aug
                        scalogram_z_aug_norm = xcc_zr_aug / np.max(xcc_zr_aug)
                        scalogram_r_aug_norm = xcc_zt_aug / np.max(xcc_zt_aug)
                        scalogram_t_aug_norm = xcc_rt_aug / np.max(xcc_rt_aug)
                    else:
                        scalogram_z_aug_norm = scalogram_z_aug / np.max(scalogram_z_aug)
                        scalogram_r_aug_norm = scalogram_r_aug / np.max(scalogram_r_aug)
                        scalogram_t_aug_norm = scalogram_t_aug / np.max(scalogram_t_aug)

                    #stack images to single 3 x N x M array
                    scalogram_3comp_aug = np.array((scalogram_z_aug_norm,scalogram_r_aug_norm,scalogram_t_aug_norm))
                    
                    print('{}.{} (augment) saved'.format(net_code,sta_code))
                    n_good += 1
                    outname2 = '{}_{:04d}_augmented'.format(dataset_name,n_good)
                    
                    #write scalograms
                    np.save(f"{outdir_image}/{outname2}",np.abs(scalogram_3comp_aug))

                    #write labels
                    labels.write('{}/{}.npy, {}, {}, {:6.4f}, {:6.4f}, {:6.4f}, {:6.4f}, {}, {}, {:6.4f}, {:6.4f}, {:6.4f}, {:6.4f}\n'.format(outdir_image,outname2,e_type,event_name,dist_here,evlo,evla,evdp,net_code,sta_code,stlo,stla,ps_here,snr_here))

        else:
            print(f"{net_code}.{sta_code} not satisfy SNR,dist criteria")

labels.close()
