import os
from network import HybridDataset, CNN_1D2D
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
from torchvision import datasets
from torchvision import transforms
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor,ToPILImage,Lambda
from sys import argv
import numpy as np


DEVICE = torch.device("cpu")
BATCHSIZE = 64
labels_file_test = argv[1]
MODEL_PATH = argv[2]
out_file_predict = argv[3]
out_file_accuracy = argv[4]


def get_data():
    test_data = HybridDataset(annotations_file=labels_file_test,transform=None,target_transform=Lambda(lambda y: torch.zeros(2, dtype=torch.float).scatter_(0, torch.tensor(y), value=1)))
    test_loader = DataLoader(test_data, batch_size=BATCHSIZE, shuffle=False)

    return test_loader


if __name__ == "__main__":
    
    # Load the model.
    model = CNN_1D2D().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()
    
    # Get the test dataset.
    test_loader = get_data()

    # Testing.
    fp_predict = open(out_file_predict, 'w')
    correct = 0
        
    with torch.no_grad():
            
        for batch_idx, data in enumerate(test_loader):
                
            scalogram, pick_prob, label, dist_km, evlo, evla, evdp, stlo, stla, psr, snr = data
            
            scalogram = scalogram.to(DEVICE)
            pick_prob = pick_prob.to(DEVICE)
            label = label.to(DEVICE)
            
            output = model(scalogram, pick_prob)
                
            # Get the index of the max probability.
            pred = output.argmax(dim=1)
            label_idx = label.argmax(dim=1)
            correct += (pred == label_idx).sum().item()
            
            # Probability
            prob = F.softmax(output, dim=1)
            
            # save
            for i in range(len(prob)):
                true_label = label_idx[i].item()
                pred_label = pred[i].item()
                prob_0 = prob[i,0].item()   # probability of class 0
                prob_1 = prob[i,1].item()   # probability of class 1
                fp_predict.write('{:5.3f} {:5.3f} {:5.3f} {:5.3f} {:5.3f} {:5.3f} {:5.3f} {:5.3f} {:1.0f} {:1.0f} {:2.2f} {:2.2f}\n'.format(
                         evlo[i],evla[i],evdp[i],stlo[i],stla[i],dist_km[i],psr[i],snr[i],true_label,pred_label,prob_0,prob_1))

    # calculate accuracy
    accuracy = (correct / len(test_loader.dataset)) * 100.0
    
    # report accuracy
    print(f"Accuracy: {accuracy:2.2f}%, N_correct: {correct}, N_total: {len(test_loader.dataset)}")
    np.savetxt(out_file_accuracy, [f"Accuracy: {accuracy:2.2f}%, N_correct: {correct}, N_total: {len(test_loader.dataset)}"], fmt="%s")
    

    fp_predict.close()




