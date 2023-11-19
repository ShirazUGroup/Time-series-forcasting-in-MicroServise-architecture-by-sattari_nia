# -*- coding: utf-8 -*-
"""prediction_time_series_final_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NAN70eemyTNCjPk5-BsYRfbNBEWla4Fn

## **import libraries**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from sklearn import preprocessing
import random
import pandas as pd
from matplotlib.colors import Sequence
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization, Conv1D, Flatten
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler

"""### **read main dataset**"""

data = pd.read_csv('/content/drive/MyDrive/dataset/original_result.csv')
data.head()
main_dataframe = data.transpose()
main_dataframe.head()
column_name = main_dataframe.iloc[0]
main_dataframe = main_dataframe[1:]
main_dataframe.columns = column_name
main_dataframe

"""### **change form of Dataset**"""

indexes = [item for item in range(0,5760)]
main_dataframe.index=indexes
main_dataframe = main_dataframe.astype(float)
main_dataframe.head()

"""# **normalise Data in Dataset**"""

scaler = MinMaxScaler()
for column in main_dataframe.columns:
  main_dataframe[column] =  scaler.fit_transform(main_dataframe[[column]])

main_dataframe.head()

"""## **add Lag for target columns**"""

main_dataframe['future']=main_dataframe['post_storage_read_posts_server'].shift(-1)
main_dataframe.dropna(inplace = True)
main_dataframe.head()

"""# function Preparing input data for LSTM model"""

def preprocessing(df , batch_size):
  # every i is one row of data
  sequense=[]
  prev_items = deque(maxlen=batch_size)
  for i in df.values:
    prev_items.append([n for n in i[:-1]])
    if len(prev_items) == batch_size :
      sequense.append([np.array(prev_items),i[-1]])

  # random.shuffle(sequense)
  # len(sequense)
  # print('first sequence  ',len(sequense[0]))
  # print('last  sequence  ',len(sequense[-1]))

  x = []
  y = []
  for seq , target in sequense:
    x.append(seq)
    y.append(target)
  return np.array(x) , np.array(y)

"""# Tesat And Train Data"""

train_data = main_dataframe.iloc[:5000, :]
test_data = main_dataframe.iloc[5000:, :]
batch_size = 32

train_X , train_y = preprocessing(main_dataframe, 32)
print('train_x:' , train_X.shape ,'train_y:',train_y.shape )
test_X , test_y = preprocessing(test_data,batch_size=batch_size)
print('test_x:' , test_X.shape ,'test_y:',test_y.shape )

"""# Design recurrent Neural network Model"""

model = Sequential()

model.add(LSTM(128, input_shape=(train_X.shape[1:]), return_sequences=True))

model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(LSTM(64 , activation='tanh'))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(Dense(1, activation="relu"))
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

"""# execute Model"""

history = model.fit(train_X, train_y, batch_size=64,epochs=500, validation_data=(test_X, test_y) )

"""# show result of Prediction"""

predictions = model.predict(test_X)

# Plot the predictions and real values
plt.figure(figsize=(12, 6))
plt.plot(test_y, label='Real Values', color='blue')
plt.plot(predictions, label='Predictions', color='red')
plt.xlabel('Time Steps')
plt.ylabel('Value')
plt.title('Real vs. Predicted Values')
plt.legend()
plt.show()
