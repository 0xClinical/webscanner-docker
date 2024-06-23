import time
import os
import torchvision
import torch as t
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import numpy as np
from tqdm.auto import trange
from typing import Optional, Tuple, Union, TYPE_CHECKING
#引用模型库
from art.estimators.classification import PyTorchClassifier
from art.attacks.evasion import ProjectedGradientDescent
'''
配置参数
'''
BATCH_SIZE = 16     # 训练批量：一批256个
learning_rate = 0.1  # 学习率
EPOCHS = 30   #学习30轮

#加载GTSRB数据集
#转换图像，变换成112*112，转换为张量
data_transforms = transforms.Compose([transforms.Resize([227, 227]), transforms.ToTensor()])

#训练集加载（43个文件夹，文件夹名就是分类序号）
train_data_path = '../input/GTSRB_jpg/Train'      #加载训练集

# 从路径加载图片，并将其转换为112*112大小
train_data = torchvision.datasets.ImageFolder(root = train_data_path, transform = data_transforms)

#训练集划分 为训练集和验证集（8-2分）
ratio = 0.8
n_train_examples = int(len(train_data) * ratio)
n_val_examples = len(train_data) - n_train_examples
train_data, val_data = data.random_split(train_data, [n_train_examples, n_val_examples])

trainloader = data.DataLoader(train_data, shuffle=True, batch_size=BATCH_SIZE)
valloader = data.DataLoader(val_data, shuffle=True, batch_size=BATCH_SIZE)

#加载模型
numClasses = 2
class NeuralNet(nn.Module):
    def __init__(self, output_dim):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, stride=2, padding=1),
            nn.MaxPool2d(kernel_size=2),
            nn.ReLU(inplace=True),

            nn.Conv2d(in_channels=64, out_channels=192, kernel_size=3, padding=1),
            nn.MaxPool2d(kernel_size=2),
            nn.ReLU(inplace=True),

            nn.Conv2d(in_channels=192, out_channels=384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(in_channels=384, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.MaxPool2d(kernel_size=2),
            nn.ReLU(inplace=True),
        )

        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 7 * 7, 1000),
            nn.ReLU(inplace=True),

            nn.Dropout(0.5),
            nn.Linear(in_features=1000, out_features=256),
            nn.ReLU(inplace=True),

            nn.Linear(256, output_dim)
        )

    def forward(self, x):
        x = self.features(x)
        h = x.view(x.shape[0], -1)
        x = self.classifier(h)
        return x
model=AlexNet(numClasses)
model.load_state_dict(t.load('./Model/pytorch_classification_alexnetTS.pth'))
model.cuda()

#SGD优化器
optimiser1 = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9, weight_decay=5e-4)
optimiser2 = optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=5e-4)
#损失函数
criterion = nn.CrossEntropyLoss()

#学习率衰减
def adjust_learning_rate(optimizer, epoch, lr):
    if(epoch == EPOCHS//2):
        return 0.01
    if(epoch == 3*EPOCHS//4):
        return 0.001


if t.cuda.is_available():
    model = model.cuda()
    criterion = criterion.cuda()

# 分类器
classifier = PyTorchClassifier(
    model=model,
    clip_values=(0.0, 1.0),
    loss=criterion,
    optimizer=optimiser2,
    input_shape=(3, 112, 112),
    nb_classes=numClasses,
)

# PGD攻击
attack = ProjectedGradientDescent(
    classifier,
    norm=np.inf,
    eps=8.0 / 255.0,
    eps_step=2.0 / 255.0,
    max_iter=15,
    targeted=False,
    num_random_init=5,
    batch_size=BATCH_SIZE,
)

# 准确度：衡量最终训练结果
def calculate_accuracy(y_pred, y):
    top_pred = y_pred.argmax(1, keepdim = True)
    correct = top_pred.eq(y.view_as(top_pred)).sum()
    acc = correct.float() / y.shape[0]
    return acc

# 训练函数
def train(model, loader, opt, criterion):
    epoch_loss = 0
    epoch_acc = 0

    # Train the model
    model.train()

    for (images, labels) in loader:
        images = images.cuda()
        labels = labels.cuda()

        output = model(images)
        # output, _ = model(images)
        loss = criterion(output, labels)

        # Training pass
        opt.zero_grad()

        # Backpropagation
        loss.backward()

        # Calculate accuracy
        acc = calculate_accuracy(output, labels)

        # Optimizing weights
        opt.step()

        epoch_loss += loss.item()
        epoch_acc += acc.item()

    return epoch_loss / len(loader), epoch_acc / len(loader)

# 评估函数
def evaluate(model, loader, opt, criterion):
    epoch_loss = 0
    epoch_acc = 0

    # evaluate the model
    model.eval()

    with t.no_grad():
        for (images, labels) in loader:

            output = model(images)
            # output, _ = model(images)
            loss = criterion(output, labels)

            acc = calculate_accuracy(output, labels)

            epoch_loss += loss.item()
            epoch_acc += acc.item()

    return epoch_loss / len(loader), epoch_acc / len(loader)

# 开始训练-----------------------------------------
train_loss_list = [0]*EPOCHS    #每轮训练的损失值
train_acc_list = [0]*EPOCHS     #每轮训练的准确率
val_loss_list = [0]*EPOCHS      #每轮使用验证集验证的损失值
val_acc_list = [0]*EPOCHS       #每轮使用验证集验证的准确率

for epoch in range(EPOCHS):    #训练EPOCHS轮
    print("Epoch {}: ".format(epoch))
    learning_rate = adjust_learning_rate(optimiser1, epoch, learning_rate)
    valloader = data.DataLoader(val_data, shuffle=True, batch_size=BATCH_SIZE)

    if (epoch %10 == 0):#每十轮重新加载数据集也就是重置数据集的扰动
        print("重置扰动周期")
        trainloader = data.DataLoader(train_data, shuffle=True, batch_size=BATCH_SIZE)
    for image_train, _ in trainloader:
        #迭代PGD攻击
        img_train_attack = attack.generate(image_train.cpu().numpy())#生成对抗样本
        img_train_attack = t.from_numpy(img_train_attack)#numpy数据类型转tensor
        image_train = img_train_attack#修改trainloader的数据
        image_train = image_train.cuda()#转在gpu上处理图片
    for image, _ in valloader:#加载测试集
        img_val_attack = attack.generate(image.cpu().numpy())
        img_val_attack = t.from_numpy(img_val_attack)
        image = img_val_attack
        image = image.cuda()

    train_start_time = time.monotonic()
    train_loss, train_acc= train(model, trainloader, optimiser1, criterion)
    train_end_time = time.monotonic()

    val_start_time = time.monotonic()
    val_loss, val_acc = evaluate(model, valloader, optimiser1, criterion)
    val_end_time = time.monotonic()

    train_loss_list[epoch] = train_loss
    train_acc_list[epoch] = train_acc
    val_loss_list[epoch] = val_loss
    val_acc_list[epoch] = val_acc
    #精度骤降,结束循环
    if(val_acc_list[epoch] < val_acc_list[epoch - 1] - 0.3):
        break

    print("Training: Loss = %.4f, Accuracy = %.4f, Time = %.2f seconds" %(train_loss, train_acc, train_end_time-train_start_time))
    print("Validation: Loss = {}, Accuracy = {}, Time = {} seconds".format(val_loss, val_acc, val_end_time - val_start_time))
    print("")

# 训练结束后，保存模型（这里只保存了模型参数）
MODEL_FOLDER = "./Model"
if not os.path.isdir(MODEL_FOLDER):
    os.mkdir(MODEL_FOLDER)

PATH_TO_MODEL = MODEL_FOLDER + "/adversarial_training_SPPGD_alexnetTS.pth"
if os.path.exists(PATH_TO_MODEL):
    os.remove(PATH_TO_MODEL)
t.save(model.state_dict(), PATH_TO_MODEL)  # 保存模型参数
print("Model saved at %s" % (PATH_TO_MODEL))