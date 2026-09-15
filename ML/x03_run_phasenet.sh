#!/bin/bash

#conda activate base


# base
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/base/base_pars_6_18Hz.h5
dataset_name=base
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/base
augment=True
aug_type=EQ
dset_repeattimes=2
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/base

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# enam
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/enam/enam_pars_6_18Hz.h5
dataset_name=enam
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/enam
augment=True
aug_type=EX
dset_repeattimes=1
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/enam

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# gasc
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/gasc/gasc_pars_6_18Hz.h5
dataset_name=gasc
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/gasc
augment=True
aug_type=EX
dset_repeattimes=5
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/gasc

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# hlp
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/hlp/hlp_pars_6_18Hz.h5
dataset_name=hlp
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/hlp
augment=False
aug_type=EX
dset_repeattimes=0
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/hlp

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# idor
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/idor/idor_pars_6_18Hz.h5
dataset_name=idor
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/idor
augment=True
aug_type=EX
dset_repeattimes=1
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/idor

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# msh
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/msh/msh_pars_6_18Hz.h5
dataset_name=msh
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/msh
augment=True
aug_type=EX
dset_repeattimes=3
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/msh

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# rifsis
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/rifsis/rifsis_pars_6_18Hz.h5
dataset_name=rifsis
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/rifsis
augment=True
aug_type=EX
dset_repeattimes=27
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/rifsis

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# sima
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/sima/sima_pars_6_18Hz.h5
dataset_name=sima
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/sima
augment=True
aug_type=EX
dset_repeattimes=168
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/sima

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# spe1
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/spe1/spe1_pars_6_18Hz.h5
dataset_name=spe1
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/spe1
augment=True
aug_type=EX
dset_repeattimes=24
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/spe1

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# spe2
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/spe2/spe2_pars_6_18Hz.h5
dataset_name=spe2
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/spe2
augment=True
aug_type=EX
dset_repeattimes=12
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/spe2

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# ssip
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/ssip/ssip_pars_6_18Hz.h5
dataset_name=ssip
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/ssip
augment=True
aug_type=EX
dset_repeattimes=1
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/ssip

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# Tibet
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/tibet/tibet_pars_6_18Hz.h5
dataset_name=tibet
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/tibet
augment=False
aug_type=EX
dset_repeattimes=1
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/tibet

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# SFVF
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/sfvf/sfvf_pars_6_18Hz.h5
dataset_name=sfvf
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/sfvf
augment=True
aug_type=EX
dset_repeattimes=3
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/sfvf

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# isjo1
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/isjo1/isjo1_pars_6_18Hz.h5
dataset_name=isjo1
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/isjo1
augment=True
aug_type=EX
dset_repeattimes=180
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/isjo1

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# alcudia
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/alcudia/alcudia_pars_6_18Hz.h5
dataset_name=alcudia
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/alcudia
augment=True
aug_type=EX
dset_repeattimes=8
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/alcudia

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# larse
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/larse/larse_pars_6_18Hz.h5
dataset_name=larse
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/larse
augment=True
aug_type=EX
dset_repeattimes=12
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/larse

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}


# isjo2
input_file=/data/Chenglong/AFRL/NEW_2025_2026/asdf/isjo2/isjo2_pars_6_18Hz.h5
dataset_name=isjo2
outdir_image=/data/Chenglong/AFRL/NEW_2025_2026/AI_JGR/feature/phasenet/isjo2
augment=False
aug_type=EX
dset_repeattimes=1
outdir_label=../label/phasenet
outdir_ascii=./ascii_wfm/isjo2

python ./compute_phasenet.py ${input_file} ${dataset_name} ${outdir_image} ${augment} ${aug_type} ${dset_repeattimes} ${outdir_label} ${outdir_ascii}



