#!/bin/bash

#conda activate torch


N_bootstrap=20


for ((i=1; i<=N_bootstrap; i++)); do

    idx=$(printf "%04d" $i)
    echo "running ${idx}..."

    labels_file_train=./data_qc2/70_15_15_sixteen/${idx}/labels_train.csv
    labels_file_valid=./data_qc2/70_15_15_sixteen/${idx}/labels_valid.csv


    output_loss_file=./loss_qc2/70_15_15_sixteen_${idx}.dat
    dir_output_model=./model_qc2/70_15_15_sixteen_${idx}

    
    python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}

done
