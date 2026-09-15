import os
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torchvision
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.io import read_image
from torchvision.transforms import ToTensor,ToPILImage,Lambda
import torch.optim as optim
from torchvision import transforms
import torch.nn.functional as F
from sys import argv


class HybridDataset(Dataset):

    def __init__(self, annotations_file, transform=None, target_transform=None):
        self.feature_labels = pd.read_csv(annotations_file, header=None)
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.feature_labels)

    def __getitem__(self, idx):
        specgram_path = self.feature_labels.iloc[idx,0]
        specgram = np.load(specgram_path)
        specgram = torch.from_numpy(specgram).float()
        
        phasenet_path = self.feature_labels.iloc[idx,1]
        phasenet = np.load(phasenet_path)
        phasenet = torch.from_numpy(phasenet).float()

        label = self.feature_labels.iloc[idx, 2]
        dist_km = self.feature_labels.iloc[idx,4]
        evlo = self.feature_labels.iloc[idx,5]
        evla = self.feature_labels.iloc[idx,6]
        evdp = self.feature_labels.iloc[idx,7]
        stlo = self.feature_labels.iloc[idx,10]
        stla = self.feature_labels.iloc[idx,11]
        psr = self.feature_labels.iloc[idx,12]
        snr = self.feature_labels.iloc[idx,13]

        if self.transform:
            specgram = self.transform(specgram)
        
        if self.target_transform:
            label = self.target_transform(label)
        
        return specgram, phasenet, label, dist_km, evlo, evla, evdp, stlo, stla, psr, snr



class CNN_1D2D(nn.Module):
    def __init__(self):
        super().__init__()

        self.scalo_branch = nn.Sequential(
            nn.Conv2d(3, 53, 3, stride=1, dilation=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(53, 25, 3, stride=1, dilation=2),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(25, 46, 3, stride=1, dilation=2),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        
        self.scalo_dim = 46*3*46
        
        self.pick_branch = nn.Sequential(
            nn.Conv1d(2, 28, 9, stride=4),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Conv1d(28, 24, 13, stride=3),
            nn.ReLU(),
            nn.MaxPool1d(2)
        )
        
        self.pick_dim = 24*81
        
        self.classifier = nn.Sequential(
            nn.Linear(self.scalo_dim+self.pick_dim, 286),
            nn.ReLU(),
            nn.Dropout(p=0.3068468262995954),
            nn.Linear(286, 2)
        )

    def forward(self, scalogram, pick_prob):
        x1 = self.scalo_branch(scalogram)
        x1 = torch.flatten(x1, 1)

        x2 = self.pick_branch(pick_prob)
        x2 = torch.flatten(x2, 1)

        x12 = torch.cat([x1, x2], dim=1)
        x = self.classifier(x12)
        
        return x



