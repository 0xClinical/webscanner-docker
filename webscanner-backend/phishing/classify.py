import torch
import torch.nn as nn
import re
import numpy as np
from sklearn.preprocessing import StandardScaler
from . import load_data as data
from . import parse_url

model_path = 'phishing/phishing_website.pth'
class PhishingModel(nn.Module):
    def __init__(self):
        super(PhishingModel, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * data.X_train.shape[1], 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = x.unsqueeze(1)  # 添加通道维度
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = x.view(x.size(0), -1)  # 展平
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x


# 创建模型实例
model = PhishingModel()

# 加载模型状态字典
model.load_state_dict(torch.load(model_path))
model.eval()  # 切换模型到评估模式
print('Model loaded and ready to use')

# 标准化器
scaler = StandardScaler()
scaler.fit(data.X_train)  # 需要用训练时的数据拟合标准化器
'''
important_features = [
    'having_ip_address',
    'url_length',
    'shortining_service',
    'sslfinal_state',
    'domain_registration_length',
    'web_traffic'
]
'''
#定义特征
def extract_features(url):
    features = []
    features.append(len(url))  # URL 长度
    features.append(int('https' in url.lower()))  # 是否使用 HTTPS
    features.append(len(re.findall(r'\.', url)))  # 点的数量
    features.append(len(re.findall(r'/', url)))  # 斜杠的数量
    features.append(len(re.findall(r'\d', url)))  # 数字的数量
    features.append(len(re.findall(r'[-_]', url)))  # 特殊字符的数量
    return np.array(features).reshape(1, -1)

def url_detect(url):
    features = parse_url.get_important_features(url)
    features_scaled = scaler.transform(features)
    features_tensor = torch.tensor(features_scaled, dtype=torch.float32)
    output = model(features_tensor)
    prediction = (output.squeeze().item() > 0.5)
    return prediction