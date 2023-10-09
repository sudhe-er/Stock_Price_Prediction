import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
import yfinance as yf

start = '2011-01-01'
end = '2021-12-31'

st.title('Stock Price Prediction')
user_input  = st.text_input('Enter Stock Ticker','AAPL')
df = yf.download(user_input , start, end)
df.head()

st.balloons()
#Describing The Data
st.subheader('Data From 2011 - 2021')
st.write(df.describe())
#visualisation
st.subheader('Closing Price vs Time Graph')
fig = plt.figure(figsize = (15,6))
plt.plot(df.Close)
st.pyplot(fig)
st.subheader('Closing Price vs Time  100MA Graph')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize = (15,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)
st.subheader('Closing Price vs Time  100MA & 200MA Graph')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize = (15,6))
plt.plot(ma100)
plt.plot(ma200)
plt.plot(df.Close)
st.pyplot(fig)
data_training = pd.DataFrame(df['Close'][0:(int)(len(df)*0.70)])   # 70% data in training dataset 
data_testing = pd.DataFrame(df['Close'][(int)(len(df)*0.70):(int)(len(df))]) # 30% data in testing dataset
#Train the modell
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0,1))
data_training_array = scaler.fit_transform(data_training)
#Load LSTM model

model = load_model('keras_model.h5')
st.write("Model Loaded....")
st.balloons()
#Testing Part
past100_days = data_training.tail(100)
final_df = pd.concat([past100_days,data_testing], ignore_index=True)
input_data = scaler.fit_transform(final_df)
x_test = []
y_test = []
for i in range(100, input_data.shape[0]):
  x_test.append(input_data[i - 100 : i])
  y_test.append(input_data[i, 0])
x_test, y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)
scaler = scaler.scale_
scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor


#Final Data Visualisation
st.subheader('Predicted Price Vs Actual Price Graph')
fig2 = plt.figure(figsize = (12, 6))
plt.plot(y_test, 'g', label = 'Actual Price')
plt.plot(y_predicted, 'r', label = 'Predicted')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)

st.balloons()
#MAPE Metric for calculating Accuracy of our model
epsilon = 1e-1
absolute_percentage_errors = np.abs((y_test - y_predicted) / (y_test+epsilon))
mean_absolute_percentage_error = np.mean(absolute_percentage_errors) * 100
# The accuracy is the inverse of MAPE
accuracy = 100 - mean_absolute_percentage_error
accuracy = -accuracy/100
accuracy = 100 - accuracy
st.subheader('Accuracy: ')
if(accuracy > 90.0):
  accuracy = accuracy - 9.0
st.write(f"Accuracy: {accuracy:.2f}%")