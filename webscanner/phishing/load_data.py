from ucimlrepo import fetch_ucirepo
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

# 从 UCIMLRepo 获取数据集
phishing_websites = fetch_ucirepo(id=327)
X = phishing_websites.data.features
y = phishing_websites.data.targets

important_features = [
    'having_ip_address',
    'url_length',
    'shortining_service',
    'sslfinal_state',
    'domain_registration_length',
    'web_traffic'
]

# 打印列名以确保选择正确的特征名称
#print(X.columns)

X_important = X[important_features]
# 数据预处理
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_important)

# 将标签转换为整数
y = y.astype(int)

# 将标签 -1 转换为 0，将标签 1 保持为 1
y_transformed = np.where(y == -1, 0, y)

# 查看转换后的标签分布
unique, counts = np.unique(y_transformed, return_counts=True)
print("转换后的标签分布:", dict(zip(unique, counts)))

# 将数据拆分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_transformed, test_size=0.2, random_state=42)

print("训练集大小:", X_train.shape, y_train.shape)
print("测试集大小:", X_test.shape, y_test.shape)

# 将数据转换为Tensor
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

# 将数据转换为 PyTorch 数据集
class PhishingDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


train_dataset = PhishingDataset(X_train, y_train)
test_dataset = PhishingDataset(X_test, y_test)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
