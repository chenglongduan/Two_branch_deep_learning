#!/bin/bash

#conda activate base


# base
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/base/base_pars_6_18Hz.h5
dataset_name=base
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/base
augment=True
aug_type=EQ
dset_repeattimes=2
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# enam
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/enam/enam_pars_6_18Hz.h5
dataset_name=enam
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/enam
augment=True
aug_type=EX
dset_repeattimes=1
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# gasc
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/gasc/gasc_pars_6_18Hz.h5
dataset_name=gasc
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/gasc
augment=True
aug_type=EX
dset_repeattimes=5
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# hlp
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/hlp/hlp_pars_6_18Hz.h5
dataset_name=hlp
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/hlp
augment=False
aug_type=EX
dset_repeattimes=0
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# idor
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/idor/idor_pars_6_18Hz.h5
dataset_name=idor
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/idor
augment=True
aug_type=EX
dset_repeattimes=1
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# msh
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/msh/msh_pars_6_18Hz.h5
dataset_name=msh
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/msh
augment=True
aug_type=EX
dset_repeattimes=3
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# rifsis
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/rifsis/rifsis_pars_6_18Hz.h5
dataset_name=rifsis
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/rifsis
augment=True
aug_type=EX
dset_repeattimes=27
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# sima
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/sima/sima_pars_6_18Hz.h5
dataset_name=sima
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/sima
augment=True
aug_type=EX
dset_repeattimes=168
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# spe1
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/spe1/spe1_pars_6_18Hz.h5
dataset_name=spe1
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/spe1
augment=True
aug_type=EX
dset_repeattimes=24
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# spe2
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/spe2/spe2_pars_6_18Hz.h5
dataset_name=spe2
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/spe2
augment=True
aug_type=EX
dset_repeattimes=12
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# ssip
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/ssip/ssip_pars_6_18Hz.h5
dataset_name=ssip
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/ssip
augment=True
aug_type=EX
dset_repeattimes=1
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# Tibet
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/tibet/tibet_pars_6_18Hz.h5
dataset_name=tibet
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/tibet
augment=False
aug_type=EX
dset_repeattimes=1
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# SFVF
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/sfvf/sfvf_pars_6_18Hz.h5
dataset_name=sfvf
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/sfvf
augment=True
aug_type=EX
dset_repeattimes=3
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# isjo1
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/isjo1/isjo1_pars_6_18Hz.h5
dataset_name=isjo1
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/isjo1
augment=True
aug_type=EX
dset_repeattimes=180
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# alcudia
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/alcudia/alcudia_pars_6_18Hz.h5
dataset_name=alcudia
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/alcudia
augment=True
aug_type=EX
dset_repeattimes=8
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# larse
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/larse/larse_pars_6_18Hz.h5
dataset_name=larse
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/larse
augment=True
aug_type=EX
dset_repeattimes=12
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}


# isjo2
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/isjo2/isjo2_pars_6_18Hz.h5
dataset_name=isjo2
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/scalogram_zrt/isjo2
augment=False
aug_type=EX
dset_repeattimes=1
outdir_label=../label/scalogram_zrt
normalize=spec_max

python ./compute_scalograms.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${normalize}



