# https://blog.csdn.net/weixin_44769214/article/details/108188126

import torch
import models
import os
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from train import MyDataset


'''
将1.6版本的pth转换为1.2版本使用的pth
'''
# device = torch.device('cuda')
# net = models.Classification().to(device)
# net.load_state_dict(torch.load('Lenet.pth'))
# torch.save(net.state_dict(), 'Lenet_compatible.pth', _use_new_zipfile_serialization=False)


'''
将1.6 gpu版本的pth转换为1.2版本能使用的cpu版本pth'''
device = torch.device('cpu')
net = models.Classification().to(device)
net.load_state_dict(torch.load('Lenet_compatible.pth', map_location='cpu'))
torch.save(net.state_dict(), 'Lenet_compatible_cpu_1.pth', _use_new_zipfile_serialization=False)