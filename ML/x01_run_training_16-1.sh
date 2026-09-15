#!/bin/bash

#conda activate torch


echo "running ALCUDIA..."

labels_file_train=./data_qc2/test_alcudia/labels_train.csv
labels_file_valid=./data_qc2/test_alcudia/labels_valid.csv


output_loss_file=./loss_qc2/except_alcudia.dat
dir_output_model=./model_qc2/except_alcudia


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running BASE..."

labels_file_train=./data_qc2/test_base/labels_train.csv
labels_file_valid=./data_qc2/test_base/labels_valid.csv


output_loss_file=./loss_qc2/except_base.dat
dir_output_model=./model_qc2/except_base


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running ENAM..."

labels_file_train=./data_qc2/test_enam/labels_train.csv
labels_file_valid=./data_qc2/test_enam/labels_valid.csv


output_loss_file=./loss_qc2/except_enam.dat
dir_output_model=./model_qc2/except_enam


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running GASC..."

labels_file_train=./data_qc2/test_gasc/labels_train.csv
labels_file_valid=./data_qc2/test_gasc/labels_valid.csv


output_loss_file=./loss_qc2/except_gasc.dat
dir_output_model=./model_qc2/except_gasc


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running HLP..."

labels_file_train=./data_qc2/test_hlp/labels_train.csv
labels_file_valid=./data_qc2/test_hlp/labels_valid.csv


output_loss_file=./loss_qc2/except_hlp.dat
dir_output_model=./model_qc2/except_hlp


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running IDOR..."

labels_file_train=./data_qc2/test_idor/labels_train.csv
labels_file_valid=./data_qc2/test_idor/labels_valid.csv


output_loss_file=./loss_qc2/except_idor.dat
dir_output_model=./model_qc2/except_idor


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running ISJO..."

labels_file_train=./data_qc2/test_isjo/labels_train.csv
labels_file_valid=./data_qc2/test_isjo/labels_valid.csv


output_loss_file=./loss_qc2/except_isjo.dat
dir_output_model=./model_qc2/except_isjo


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running LARSE..."

labels_file_train=./data_qc2/test_larse/labels_train.csv
labels_file_valid=./data_qc2/test_larse/labels_valid.csv


output_loss_file=./loss_qc2/except_larse.dat
dir_output_model=./model_qc2/except_larse


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running MSH..."

labels_file_train=./data_qc2/test_msh/labels_train.csv
labels_file_valid=./data_qc2/test_msh/labels_valid.csv


output_loss_file=./loss_qc2/except_msh.dat
dir_output_model=./model_qc2/except_msh


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running RIFSIS..."

labels_file_train=./data_qc2/test_rifsis/labels_train.csv
labels_file_valid=./data_qc2/test_rifsis/labels_valid.csv


output_loss_file=./loss_qc2/except_rifsis.dat
dir_output_model=./model_qc2/except_rifsis


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running SFVF..."

labels_file_train=./data_qc2/test_sfvf/labels_train.csv
labels_file_valid=./data_qc2/test_sfvf/labels_valid.csv


output_loss_file=./loss_qc2/except_sfvf.dat
dir_output_model=./model_qc2/except_sfvf


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running SIMA..."

labels_file_train=./data_qc2/test_sima/labels_train.csv
labels_file_valid=./data_qc2/test_sima/labels_valid.csv


output_loss_file=./loss_qc2/except_sima.dat
dir_output_model=./model_qc2/except_sima


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running SPE1..."

labels_file_train=./data_qc2/test_spe1/labels_train.csv
labels_file_valid=./data_qc2/test_spe1/labels_valid.csv


output_loss_file=./loss_qc2/except_spe1.dat
dir_output_model=./model_qc2/except_spe1


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running SPE2..."

labels_file_train=./data_qc2/test_spe2/labels_train.csv
labels_file_valid=./data_qc2/test_spe2/labels_valid.csv


output_loss_file=./loss_qc2/except_spe2.dat
dir_output_model=./model_qc2/except_spe2


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running SSIP..."

labels_file_train=./data_qc2/test_ssip/labels_train.csv
labels_file_valid=./data_qc2/test_ssip/labels_valid.csv


output_loss_file=./loss_qc2/except_ssip.dat
dir_output_model=./model_qc2/except_ssip


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}


echo "running TIBET..."

labels_file_train=./data_qc2/test_tibet/labels_train.csv
labels_file_valid=./data_qc2/test_tibet/labels_valid.csv


output_loss_file=./loss_qc2/except_tibet.dat
dir_output_model=./model_qc2/except_tibet


python ./train_and_valid.py ${labels_file_train} ${labels_file_valid} ${output_loss_file} ${dir_output_model}



