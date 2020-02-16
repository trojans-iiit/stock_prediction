from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf # This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler

df=pd.read_csv("AAPL_10y.csv")
df

df=df.sort_values("Date")
df


plt.figure(figsize = (18,9))
plt.plot(range(df.shape[0]),(df['Low']+df['High'])/2.0)
plt.xticks(range(0,df.shape[0],500),df['Date'].loc[::500],rotation=45)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Mid Price',fontsize=18)
plt.show()
len(df)


high_prices = df.loc[:,'High'].as_matrix()
low_prices = df.loc[:,'Low'].as_matrix()
mid_prices = (high_prices+low_prices)/2.0
train_data = mid_prices[:2000]
test_data = mid_prices[2000:]
scaler = MinMaxScaler()
train_data = train_data.reshape(-1,1)
test_data = test_data.reshape(-1,1)
smoothing_window_size = 500
for di in range(0,1500,smoothing_window_size):
    scaler.fit(train_data[di:di+smoothing_window_size,:])
    train_data[di:di+smoothing_window_size,:] = scaler.transform(train_data[di:di+smoothing_window_size,:])
# print(len(train_data))
# You normalize the last bit of remaining data
scaler.fit(train_data[di+smoothing_window_size:,:])
train_data[di+smoothing_window_size:,:] = scaler.transform(train_data[di+smoothing_window_size:,:])
train_data = train_data.reshape(-1)

# Normalize test data
test_data = scaler.transform(test_data).reshape(-1)
EMA = 0.0
gamma = 0.1
# print("Train data at 166: ", train_data[166])
for ti in range(2000):
  EMA = gamma*train_data[ti] + (1-gamma)*EMA
  # if ti < 166:
    # print(EMA)
  train_data[ti] = EMA
  # print(train_data)

# Used for visualization and test purposes
all_mid_data = np.concatenate([train_data,test_data],axis=0)

# window_size = 100
# N = train_data.size
# std_avg_predictions = []
# std_avg_x = []
# mse_errors = []

# for pred_idx in range(window_size,N):

#     if pred_idx >= N:
#         date = dt.datetime.strptime(k, '%Y-%m-%d').date() + dt.timedelta(days=1)
#     else:
#         date = df.loc[pred_idx,'Date']

#     std_avg_predictions.append(np.mean(train_data[pred_idx-window_size:pred_idx]))
#     mse_errors.append((std_avg_predictions[-1]-train_data[pred_idx])**2)
#     std_avg_x.append(date)

# print('MSE error for standard averaging: %.5f'%(0.5*np.mean(mse_errors)))

window_size = 100
N = train_data.size

run_avg_predictions = []
run_avg_x = []

mse_errors = []

running_mean = 0.0
run_avg_predictions.append(running_mean)

decay = 0.5

for pred_idx in range(1,N):

    if pred_idx >= N:
        date = dt.datetime.strptime(k, '%Y-%m-%d').date() + dt.timedelta(days=1)
    else:
        date = df.loc[pred_idx,'Date']
    running_mean = running_mean*decay + (1.0-decay)*train_data[pred_idx-1]
    run_avg_predictions.append(running_mean)
    mse_errors.append((run_avg_predictions[-1]-train_data[pred_idx])**2)
    run_avg_x.append(date)

print('MSE error for EMA averaging: %.5f'%(0.5*np.mean(mse_errors)))


plt.figure(figsize = (18,9))
plt.plot(range(df.shape[0]),all_mid_data,color='b',label='True')
plt.plot(range(0,N),run_avg_predictions,color='orange', label='Prediction')
#plt.xticks(range(0,df.shape[0],50),df['Date'].loc[::50],rotation=45)
plt.xlabel('Date')
plt.ylabel('Mid Price')
plt.legend(fontsize=18)
plt.show()