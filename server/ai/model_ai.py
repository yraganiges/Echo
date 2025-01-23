import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertModel
import pandas as pd

# Загрузка токенизатора и модели BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
bert_model = BertModel.from_pretrained('bert-base-multilingual-cased')

# Загрузка данных из CSV-файла
data = pd.read_csv('server\\ai\\datasets\\danger_messages.csv')
texts = data['messages'].tolist()  # Столбец с сообщениями
labels = data['index'].tolist()  # Столбец с метками

# Разделение данных на тренировочные и тестовые
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Определяем модель
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.bert = bert_model
        self.fc = nn.Linear(self.bert.config.hidden_size, 2)  # 2 класса (опасное и неопасное)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        logits = self.fc(outputs.pooler_output)
        return logits

# Инициализация модели, оптимизатора и функции потерь
model = SimpleNN()
optimizer = optim.Adam(model.parameters(), lr=1e-5)
criterion = nn.CrossEntropyLoss()

# Переменные для хранения значений потерь и точности
losses = []
best_accuracy = 0
best_weights = None

# Обучение модели
for epoch in range(5):  # Количество эпох
    model.train()
    epoch_loss = 0
    
    for text, label in zip(X_train, y_train):
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']
        
        optimizer.zero_grad()
        
        outputs = model(input_ids, attention_mask)
        loss = criterion(outputs, torch.tensor([label]).unsqueeze(0))
        loss.backward()
        optimizer.step()
        
        epoch_loss += loss.item()
    
    losses.append(epoch_loss / len(X_train))
    
    # Оценка на тестовых данных
    model.eval()
    correct = 0
    
    with torch.no_grad():
        for text, label in zip(X_test, y_test):
            inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
            input_ids = inputs['input_ids']
            attention_mask = inputs['attention_mask']
            
            outputs = model(input_ids, attention_mask)
            _, predicted = torch.max(outputs.data, 1)
            correct += (predicted.item() == label)
    
    accuracy = correct / len(X_test)
    print(f'Epoch: {epoch + 1}, Loss: {epoch_loss / len(X_train)}, Accuracy: {accuracy}')
    
    # Сохранение лучших весов
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_weights = model.state_dict()

# Сохранение лучших весов модели
if best_weights is not None:
    torch.save(best_weights, 'best_model.pth')

print(f'Best Accuracy: {best_accuracy}')
