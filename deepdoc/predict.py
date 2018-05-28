from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn
import numpy as np
import config as cf
import torchvision
import os
import sys
import argparse
from sklearn.metrics import precision_score

from torchvision import datasets, models, transforms
from networks import *
from torch.autograd import Variable

parser = argparse.ArgumentParser(description='PyTorch Digital Mammography Training')
parser.add_argument('--lr', default=1e-3, type=float, help='learning rate')
parser.add_argument('--net_type', default='resnet', type=str, help='model')
parser.add_argument('--depth', default=152, type=int, help='depth of model')
parser.add_argument('--weight_decay', default=5e-4, type=float, help='weight decay')
parser.add_argument('--finetune', '-f', action='store_true', help='Fine tune pretrained model')
parser.add_argument('--addlayer','-a',action='store_true', help='Add additional layer in fine-tuning')
parser.add_argument('--resetClassifier', '-r', action='store_true', help='Reset classifier')
parser.add_argument('--testOnly', '-t', action='store_true', help='Test mode with the saved model')
args = parser.parse_args()
use_gpu = torch.cuda.is_available()
classes=['Advertising', 'Email','Form', 'Letter', 'Memo', 'News', 'Note',
'Report','Resume','Scientific']


data_transforms = {
    'train': transforms.Compose([
        transforms.RandomSizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(cf.mean, cf.std)
    ]),
    'val': transforms.Compose([
        transforms.Scale(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(cf.mean, cf.std)
    ]),
}

def getNetwork(args):
    if (args.net_type == 'alexnet'):
        net = models.alexnet(pretrained=args.finetune)
        file_name = 'alexnet'
    elif (args.net_type == 'vggnet'):
        if(args.depth == 11):
            net = models.vgg11(pretrained=args.finetune)
        elif(args.depth == 13):
            net = models.vgg13(pretrained=args.finetune)
        elif(args.depth == 16):
            net = models.vgg16(pretrained=args.finetune)
        elif(args.depth == 19):
            net = models.vgg19(pretrained=args.finetune)
        else:
            print('Error : VGGnet should have depth of either [11, 13, 16, 19]')
            sys.exit(1)
        file_name = 'vgg-%s' %(args.depth)
    elif (args.net_type == 'squeezenet'):
        net = models.squeezenet1_0(pretrained=args.finetune)
        file_name = 'squeeze'
    elif (args.net_type == 'resnet'):
        net = resnet(args.finetune, args.depth)
        file_name = 'resnet-%s' %(args.depth)
    else:
        print('Error : Network should be either [alexnet / squeezenet / vggnet / resnet]')
        sys.exit(1)

    return net, file_name

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

# Test only option
def predict():
    
    assert os.path.isdir('checkpoint'), 'Error: No checkpoint directory found!'
    _, file_name = getNetwork(args)
    
    checkpoint = torch.load('./checkpoint/dataset/'+file_name+'.t7')
    model = checkpoint['model']

    if use_gpu:
        model.cuda()
        # model = torch.nn.DataParallel(model, device_ids=range(torch.cuda.device_count()))
        # cudnn.benchmark = True

    model.eval()
    test_loss = 0
    correct = 0
    total = 0

    testsets = datasets.ImageFolder(cf.test_dir, data_transforms['val'])

    testloader = torch.utils.data.DataLoader(
        testsets,
        batch_size = 1,
        shuffle = False,
        num_workers=1
    )
    pred=np.zeros((1,879))
    gt=np.zeros((1,879))

    
    for batch_idx, (inputs, targets) in enumerate(testloader):#dset_loaders['val']):
        if use_gpu:
            inputs, targets = inputs.cuda(), targets.cuda()
        inputs, targets = Variable(inputs, volatile=True), Variable(targets)
        outputs = model(inputs)

        # print(outputs.data.cpu().numpy()[0])
        softmax_res = softmax(outputs.data.cpu().numpy()[0])

        _, predicted = torch.max(outputs.data, 1)
        #print(type(predicted.numpy()))
        total += targets.size(0)
        correct += predicted.eq(targets.data).cpu().sum()
        predicted=predicted.cpu()
        targetsdata=targets.data.cpu()

        #print(type(batch_idx))
        pred[0][batch_idx]=predicted.numpy()
        gt[0][batch_idx]=targetsdata.numpy()
        print(correct)
        print(classes[predicted.numpy()[0]],' The predicted class')
        print(classes[targetsdata.numpy()[0]], 'The ground truth')
        modelresult = ' The predicted class: ' + classes[predicted.numpy()[0]] 
   
    return modelresult
predict()
