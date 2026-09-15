#!/bin/bash



#conda activate torch


echo "running ALCUDIA..."

labels_file_test=./data_qc2/test_alcudia/labels_test.csv

MODEL_PATH=./model_qc2/except_alcudia/preferred_model.pt

out_file_predict=./predict_qc2/predict_alcudia.dat
out_file_accuracy=./predict_qc2/accuracy_alcudia.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running BASE..."

labels_file_test=./data_qc2/test_base/labels_test.csv

MODEL_PATH=./model_qc2/except_base/preferred_model.pt

out_file_predict=./predict_qc2/predict_base.dat
out_file_accuracy=./predict_qc2/accuracy_base.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running ENAM..."

labels_file_test=./data_qc2/test_enam/labels_test.csv

MODEL_PATH=./model_qc2/except_enam/preferred_model.pt

out_file_predict=./predict_qc2/predict_enam.dat
out_file_accuracy=./predict_qc2/accuracy_enam.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running GASC..."

labels_file_test=./data_qc2/test_gasc/labels_test.csv

MODEL_PATH=./model_qc2/except_gasc/preferred_model.pt

out_file_predict=./predict_qc2/predict_gasc.dat
out_file_accuracy=./predict_qc2/accuracy_gasc.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running HLP..."

labels_file_test=./data_qc2/test_hlp/labels_test.csv

MODEL_PATH=./model_qc2/except_hlp/preferred_model.pt

out_file_predict=./predict_qc2/predict_hlp.dat
out_file_accuracy=./predict_qc2/accuracy_hlp.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running IDOR..."

labels_file_test=./data_qc2/test_idor/labels_test.csv

MODEL_PATH=./model_qc2/except_idor/preferred_model.pt

out_file_predict=./predict_qc2/predict_idor.dat
out_file_accuracy=./predict_qc2/accuracy_idor.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running ISJO..."

labels_file_test=./data_qc2/test_isjo/labels_test.csv

MODEL_PATH=./model_qc2/except_isjo/preferred_model.pt

out_file_predict=./predict_qc2/predict_isjo.dat
out_file_accuracy=./predict_qc2/accuracy_isjo.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running LARSE..."

labels_file_test=./data_qc2/test_larse/labels_test.csv

MODEL_PATH=./model_qc2/except_larse/preferred_model.pt

out_file_predict=./predict_qc2/predict_larse.dat
out_file_accuracy=./predict_qc2/accuracy_larse.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running MSH..."

labels_file_test=./data_qc2/test_msh/labels_test.csv

MODEL_PATH=./model_qc2/except_msh/preferred_model.pt

out_file_predict=./predict_qc2/predict_msh.dat
out_file_accuracy=./predict_qc2/accuracy_msh.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running RIFSIS..."

labels_file_test=./data_qc2/test_rifsis/labels_test.csv

MODEL_PATH=./model_qc2/except_rifsis/preferred_model.pt

out_file_predict=./predict_qc2/predict_rifsis.dat
out_file_accuracy=./predict_qc2/accuracy_rifsis.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running SFVF..."

labels_file_test=./data_qc2/test_sfvf/labels_test.csv

MODEL_PATH=./model_qc2/except_sfvf/preferred_model.pt

out_file_predict=./predict_qc2/predict_sfvf.dat
out_file_accuracy=./predict_qc2/accuracy_sfvf.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running SIMA..."

labels_file_test=./data_qc2/test_sima/labels_test.csv

MODEL_PATH=./model_qc2/except_sima/preferred_model.pt

out_file_predict=./predict_qc2/predict_sima.dat
out_file_accuracy=./predict_qc2/accuracy_sima.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running SPE1..."

labels_file_test=./data_qc2/test_spe1/labels_test.csv

MODEL_PATH=./model_qc2/except_spe1/preferred_model.pt

out_file_predict=./predict_qc2/predict_spe1.dat
out_file_accuracy=./predict_qc2/accuracy_spe1.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running SPE2..."

labels_file_test=./data_qc2/test_spe2/labels_test.csv

MODEL_PATH=./model_qc2/except_spe2/preferred_model.pt

out_file_predict=./predict_qc2/predict_spe2.dat
out_file_accuracy=./predict_qc2/accuracy_spe2.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running SSIP..."

labels_file_test=./data_qc2/test_ssip/labels_test.csv

MODEL_PATH=./model_qc2/except_ssip/preferred_model.pt

out_file_predict=./predict_qc2/predict_ssip.dat
out_file_accuracy=./predict_qc2/accuracy_ssip.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}


echo "running TIBET..."

labels_file_test=./data_qc2/test_tibet/labels_test.csv

MODEL_PATH=./model_qc2/except_tibet/preferred_model.pt

out_file_predict=./predict_qc2/predict_tibet.dat
out_file_accuracy=./predict_qc2/accuracy_tibet.dat


python ./test_only.py ${labels_file_test} ${MODEL_PATH} ${out_file_predict} ${out_file_accuracy}

