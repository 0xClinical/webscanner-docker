import torchvision
import torch
from PIL import Image
import torch.nn as nn
from torchvision import transforms
from torchvision import datasets
import torch.utils.data as data
import os

model_path = 'imagedetect/imagedetect.pth'
class AlexNet(nn.Module):
    def __init__(self,num_classes):
        super(AlexNet,self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3,96,kernel_size=11,stride=4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3,stride=2),
            nn.BatchNorm2d(96),
            nn.Conv2d(96,256,kernel_size=5,padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3,stride=2),
            nn.BatchNorm2d(256),
            nn.Conv2d(256,384,kernel_size=3,padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384,384,kernel_size=3,padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384,256,kernel_size=3,padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3,stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(256*6*6,4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096,4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096,num_classes),
        )
    def forward(self,x):
        x = self.features(x)
        x = x.view(x.size(0),256*6*6)
        x = self.classifier(x)
        return x
def getFileList(dir, Filelist, ext=None):
    newDir = dir
    if os.path.isfile(dir):
        if ext is None:
            Filelist.append(dir)
        else:
            if ext in dir[-3:]:
                Filelist.append(dir)

    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            getFileList(newDir, Filelist, ext)

    return Filelist

model = AlexNet(2)
model.load_state_dict(torch.load(model_path))
img_transforms = transforms.Compose([transforms.Resize([227, 227]),
                                      transforms.ToTensor()]
                                      )

#data_loader = data.DataLoader(data_test,batch_size=256)
#print(len(data_loader))
# 生成类标签
classes = { 0:'钓鱼图片',
            1:'无钓鱼问题',
            }




numClasses = 2
num = range(numClasses)
labels = []
for i in num:
    labels.append(str(i))
labels = sorted(labels)
for i in num:
    labels[i] = int(labels[i])
model.eval()

with torch.no_grad():
    imglist = getFileList("./test", [], 'jpg')
    for path in imglist:
        img = Image.open(path)
        img = img_transforms(img)
        img = img.resize(1, 3,227, 227)  # 转换图片为这种格式，为了让图片能够作为模型的输入
        pred_result = model(img)
        pred_softmax = torch.softmax(pred_result, dim=1)
        pred_probality, pred_tags = torch.max(pred_softmax, dim=1)
        pred_probality = pred_probality.cpu().numpy()
        pred_tags = pred_tags.cpu().numpy()
        pred_probality = pred_probality[0]
        pred_label = pred_tags[0]
        pred_label = labels[pred_label]
        pre_class = classes[pred_label]
        # 输出结果：类标签序号：识别结果[准确率]
        print(str(pred_label) + ":" + pre_class + "[" + str(pred_probality) +"]")