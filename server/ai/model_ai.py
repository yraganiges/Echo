import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

from typing import List


class NeuralNetwork:
    def __init__(
        self,
        path_dataset_csv: str, 
        columns_dataset: List[str],
        test_size: float = 0.2,
        random_state: int = 42
    ) -> None:
        # Загрузка данных
        self.df = pd.read_csv(path_dataset_csv)

        # Токенизация текста
        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts(self.df[columns_dataset[0]])
        self.X = self.tokenizer.texts_to_sequences(self.df[columns_dataset[0]])
        self.X = pad_sequences(self.X)

        # Определение меток
        self.y = self.df[columns_dataset[1]].values

        # Разделение данных на обучающую и тестовую выборки
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        # Создание модели нейронной сети
        self.model = Sequential()
        self.model.add(Embedding(input_dim=len(self.tokenizer.word_index) + 1, output_dim=128))
        self.model.add(SpatialDropout1D(0.2))
        self.model.add(LSTM(100))

        self.model.add(Dense(1, activation='sigmoid'))

        # Компиляция модели
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def train(self, epochs: int, batch_size: int) -> None:
        self.model.fit(
            self.X_train, self.y_train,
            epochs = epochs, batch_size = batch_size,
            validation_data=(
                self.X_test, self.y_test
            )
        ) # Обучение модели

    #оценка модели
    def get_accursary(self) -> float:
        return self.model.evaluate(self.X_test, self.y_test)
    
    def __proccesing_text(self, text: str) -> str:
        chars ='#$%&"()*+,-./:;<=>?@[]^_{|}~`'
        output = ""
        
        for index in text.strip().lower():
            if index not in chars:
                output += index
                
        return output

    def predict(self, text: str) -> float:
        # Шаг 1: Токенизация
        sequences = self.tokenizer.texts_to_sequences([self.__proccesing_text(text)])
        # Шаг 2: Паддинг
        padded_sequence = pad_sequences(sequences, maxlen=self.X.shape[1])
        # Шаг 3: Предсказание
        return self.model.predict(padded_sequence)[0]
    
if __name__ == "__main__": 
    nn = NeuralNetwork(
        path_dataset_csv = "server\\ai\\datasets\\danger_messages.csv",
        columns_dataset = ["messages", "index"],
        test_size = 0.2
    )
    nn.train(epochs = 13, batch_size = 5) #default: epochs = 10, batch_size = 5
    print(accursary := round(nn.get_accursary()[1], 4)) 
    print(nn.predict(text = "Артём оракл"))
    
  # accursary: float = 0.0
    
    # while accursary < 0.7:      