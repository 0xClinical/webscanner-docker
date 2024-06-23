import torch.optim as optim
import model as phishing_model
import load_data as data
import torch.nn as nn
import pickle
import torch
model_path = 'phishing/phishing_website.pth'

criterion = nn.BCELoss()
model = phishing_model.model
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in data.train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        # 确保 outputs 和 labels 的形状一致，并且 labels 在 [0, 1] 之间
        outputs = outputs.squeeze()
        labels = labels.squeeze()  # 将 labels 转换为一维
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * inputs.size(0)

    epoch_loss = running_loss / len(data.train_loader.dataset)
    print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {epoch_loss:.4f}')

model.eval()
correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in data.test_loader:
        outputs = model(inputs)
        predicted = (outputs.squeeze() > 0.5).float()
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = correct / total
print(f'Test Accuracy: {accuracy:.4f}')
torch.save(model.state_dict(), model_path)