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
import shutil
import numpy as np


DEVICE = torch.device("cpu")
BATCHSIZE = 64
EPOCHS = 50
N_STOP = 5
LR = 0.0009229826589705022
labels_file_train = argv[1]
labels_file_valid = argv[2]
output_loss_file = argv[3]
dir_output_model = argv[4]

os.makedirs(dir_output_model, exist_ok=True)
valid_loss_min = np.inf
fp_loss = open(output_loss_file, 'w')


def get_data():
    train_data = HybridDataset(annotations_file=labels_file_train,transform=None,target_transform=Lambda(lambda y: torch.zeros(2, dtype=torch.float).scatter_(0, torch.tensor(y), value=1)))
    train_loader = DataLoader(train_data, batch_size=BATCHSIZE, shuffle=True)
    
    valid_data = HybridDataset(annotations_file=labels_file_valid,transform=None,target_transform=Lambda(lambda y: torch.zeros(2, dtype=torch.float).scatter_(0, torch.tensor(y), value=1)))
    valid_loader = DataLoader(valid_data, batch_size=BATCHSIZE, shuffle=False)

    return train_loader, valid_loader


if __name__ == "__main__":
    
    # Generate the model.
    model = CNN_1D2D().to(DEVICE)
    
    total_params = sum(p.numel() for p in model.parameters())
    print(model)
    print(f"Total number of model parameters: {total_params}")
    print('\n')
    
    # Adam optim
    optimizer = optim.Adam(model.parameters(), lr=LR)
    
    # define loss function
    criterion = nn.BCEWithLogitsLoss()

    # Get the training/validation dataset.
    train_loader, valid_loader = get_data()

    # Training of the model.
    n_inc = 0
    for epoch in range(EPOCHS):
        
        print(f"Epoch {epoch}:")
        train_loss = 0
        valid_loss = 0
        
        model.train()
        
        for batch_idx, data in enumerate(train_loader):

            scalogram, pick_prob, label, dist_km, evlo, evla, evdp, stlo, stla, psr, snr = data
            
            scalogram = scalogram.to(DEVICE)
            pick_prob = pick_prob.to(DEVICE)
            label = label.to(DEVICE)

            optimizer.zero_grad()
            output = model(scalogram, pick_prob)
            loss = criterion(output, label)  # loss function
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()

        # Validation of the model.
        model.eval()
        correct = 0
        with torch.no_grad():
            
            for batch_idx, data in enumerate(valid_loader):
                
                scalogram, pick_prob, label, dist_km, evlo, evla, evdp, stlo, stla, psr, snr = data
                
                scalogram = scalogram.to(DEVICE)
                pick_prob = pick_prob.to(DEVICE)
                label = label.to(DEVICE)
                
                output = model(scalogram, pick_prob)
                
                # Loss
                loss = criterion(output, label)
                valid_loss += loss.item()
                
                # Get the index of the max probability.
                pred = output.argmax(dim=1)
                label_idx = label.argmax(dim=1)
                correct += (pred == label_idx).sum().item()

        # report accuracy for the current epoch
        accuracy = correct / len(valid_loader.dataset)
        
        # average loss per batch
        train_loss_mean = train_loss / len(train_loader)
        valid_loss_mean = valid_loss / len(valid_loader)
        
        # write loss
        fp_loss.write(f"{epoch} \t{train_loss_mean:.6f} \t{valid_loss_mean:.6f} \t{accuracy:.6f}\n")
        print(f"    train_loss: {train_loss_mean:.6f}, valid_loss: {valid_loss_mean:.6f}, accuracy: {accuracy:.6f}")
        
        # save model
        torch.save(model.state_dict(), f"{dir_output_model}/model_epoch{epoch}.pt")
        
        
        # save as preferred model if valid_loss decrease
        if valid_loss_mean < valid_loss_min:
            print(f"    valid_loss decreased ({valid_loss_min:.6f} -> {valid_loss_mean:.6f}).  Saving model...")
            
            shutil.copy(f"{dir_output_model}/model_epoch{epoch}.pt", f"{dir_output_model}/preferred_model.pt")
            
            valid_loss_min = valid_loss_mean
            n_inc = 0
        else:
            n_inc += 1

        if n_inc >= N_STOP:
            print(f"valid_loss not decrease for {n_inc} consecutive epochs. Stop training...")
            break
        
        

    fp_loss.close()




