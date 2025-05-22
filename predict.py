import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import math
import time


def today_price():
    df=pd.read_csv('./utils/tsla_history.csv')
    df.info()
    print('read the csv file')

    close_price=np.array(df['Adj Close'])
    X_train=[]
    y_train=[]

    for i in range(60, len(close_price)-60):
        X_train.append(close_price[i-60:i])
        y_train.append(close_price[i])

    X_train=np.array(X_train) # shape: (n_samples, 60)
    y_train=np.array(y_train).reshape(-1,1) # shape: (n_samples, 1)


    # You should never fit on test data. 
    # Fitting is where the model "learns," and you want your test set to remain unseen and unbiased.
    X_test=np.array(close_price[len(close_price)-60:]).reshape(1, 60) # shape: (1, 60)


    X_scaler=MinMaxScaler(feature_range=(0,1))
    y_scaler=MinMaxScaler(feature_range=(0,1))

    X_scaler.fit(X_train)
    y_scaler.fit(y_train)

    # fit(train_data)	Learns min/max or mean/std from train_data
    # transform()	Applies formula using learned values

    print("X_Min:", X_scaler.data_min_)
    print("X_Max:", X_scaler.data_max_)
    print("y_Min:", y_scaler.data_min_)
    print("y_Max:", y_scaler.data_max_)


    X_train_scaled=X_scaler.transform(X_train)
    y_train_scaled=y_scaler.transform(y_train)
    X_test_scaled=X_scaler.transform(X_test)


    # (samples, timesteps) 3602, 60
    print(f'X_train.scaled.shape:{X_train_scaled.shape}')


    # LSTM 需要的輸入格式是：
    # (samples, timesteps, features)
    X_train_scaled=X_train_scaled.reshape(X_train_scaled.shape[0], X_train_scaled.shape[1], 1)
    print(f'X_train_scaled.shape:{X_train_scaled.shape}')
    # (3602, 60, 1)


    # input_shape=(時間步長, 特徵數)

    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(60,1)))
    model.add(Dropout(0.2))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    # Model Summary
    model.summary()


    history_1=model.fit(
            X_train_scaled, y_train_scaled,
            epochs=10,
            batch_size=32,
            validation_split=0.2,
            verbose=1
        )


    # LSTM 需要的輸入格式是：
    # (samples, timesteps, features)
    X_test_scaled=X_test_scaled.reshape(1,60,1)

    y_pred_scaled = model.predict(X_test_scaled)
    y_pred_real = y_scaler.inverse_transform(y_pred_scaled)

    return y_pred_real



# Here's code for using multiple features
# df=pd.read_csv('./utils/tsla_y.csv')
# df=df[::-1]
# df=df.reset_index(drop=True)
# def change(s):
#     return float(s.replace(',', ''))
# df['Volume']=df['Volume'].apply(change)
# df.info()
# data=df[df.columns[1:]]
# data
# train_data=np.array(data[:-60])
# test_data=np.array(data[-60:])
# train_data=train_data.reshape(-1,6)
# test_data=test_data.reshape(-1,6)
# adj_data=df['Adj Close']
# adj_data=np.array(adj_data)
# adj_data=adj_data.reshape(-1,1)
# adj_data.shape
# from sklearn.preprocessing import StandardScaler
# # (n_samples, n_features)
# scaler=StandardScaler()
# adj_scaler=StandardScaler()
# scaler.fit(train_data)
# adj_scaler.fit(adj_data)
# scaled_adj_data=adj_scaler.transform(adj_data)
# scaled_train=scaler.transform(train_data)
# scaled_test=scaler.transform(test_data)
# X_train=[]
# y_train=[]
# for i in range(60, len(scaled_train)):
#     X_train.append(scaled_train[i-60:i])
#     y_train.append(scaled_adj_data[i])
# X_train=np.array(X_train)
# y_train=np.array(y_train)
# X_train.shape
# model = Sequential()
# model.add(Bidirectional(LSTM(128, return_sequences=True), input_shape=(X_train.shape[1], X_train.shape[2])))
# model.add(Dropout(0.3))
# model.add(BatchNormalization())

# model.add(Bidirectional(LSTM(64, return_sequences=True)))
# model.add(Dropout(0.2))
# model.add(BatchNormalization())

# model.add(LSTM(32))
# model.add(Dropout(0.2))

# model.add(Dense(1))  # final output: predicted Adj Close

# model.compile(loss='mean_squared_error', optimizer='adam')
# model.summary()
# history = model.fit(
#     X_train, y_train,
#     # validation_data=(X_val, y_val),  # ✅ Required for val_loss
#     epochs=20,
#     batch_size=32,
#     # callbacks=[early_stop, checkpoint],
#     verbose=1
# )
# scaled_test=scaled_test.reshape(1, scaled_test.shape[0], scaled_test.shape[1])
# scaled_test.shape

# prediction=model.predict(scaled_test)
# adj_scaler.inverse_transform(prediction)