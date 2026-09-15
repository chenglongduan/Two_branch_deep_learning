#!/bin/bash



#conda activate torch


N_bootstrap=20

for ((i=1; i<=N_bootstrap; i++)); do
    
    idx=$(printf "%04d" $i)
    echo "running ${idx}..."

    labels_file_test=./data_qc2/70_15_15_sixteen/${idx}/labels_test.csv

    MODEL_PATH=./model_qc2/70_15_15_sixteen_${idx}/preferred_model.pt

    out_file_predict=./predict_qc2/predict_70_15_15_sixteen_${idx}.dat
    out_file_accuracy=./predict_qc2/accuracy_70_15_15_sixteen_${idx}.dat



    python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}

done
