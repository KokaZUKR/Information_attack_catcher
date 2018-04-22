import warnings

warnings.simplefilter("ignore")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


def stat_hypothesis_test(X):
    result = adfuller(X)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))
    return 0


def plot_predicted(predicted, actual):  # plot builder
    plt.plot(actual, color='orange', label='actual')
    plt.plot(predicted, color='black', label='predicted')
    plt.legend()
    plt.show()
    return 0


def rmse_test(predicted, actual, to_plot=1):  # root mean squared error
    predicted = np.array(predicted)
    actual = np.array(actual)
    result = np.sqrt(((predicted - actual) ** 2).mean())
    return result


def arima_prediction(history, test, p=5, d=1, q=0, start_ar_lags=13):  # full implementation of ARIMA algorithm
    pred = []
    for t in range(len(test)):
        model = ARIMA(history, order=(int(p), int(d), int(q)))
        output = model.fit(disp=0).forecast()
        pred.append(output[0])
        history.append(test[t])
    return pred


def timeseries_to_supervised(data, lag=1):
    df = pd.DataFrame(data)
    columns = [df.shift(i) for i in range(1, lag + 1)]
    columns.append(df)
    df = pd.concat(columns, axis=1)
    df.fillna(0, inplace=True)
    return df


def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return pd.Series(diff)


def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]


def scale(train, test):
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler = scaler.fit(train)
    train = train.reshape(train.shape[0], train.shape[1])
    train_scaled = scaler.transform(train)
    test = test.reshape(test.shape[0], test.shape[1])
    test_scaled = scaler.transform(test)
    return scaler, train_scaled, test_scaled


def invert_scale(scaler, X, value):
    new_row = [x for x in X] + [value]
    array = np.array(new_row)
    array = array.reshape(1, len(array))
    inverted = scaler.inverse_transform(array)
    return inverted[0, -1]


def fit_lstm(train, batch_size, nb_epoch, neurons):
    X, y = train[:, 0:-1], train[:, -1]
    X = X.reshape(X.shape[0], 1, X.shape[1])
    model = Sequential()
    model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    for i in range(nb_epoch):
        print('Iteration:', i + 1, 'out of:', nb_epoch)
        model.fit(X, y, epochs=1, batch_size=batch_size, verbose=2, shuffle=False)
        model.reset_states()
    return model


def forecast_lstm(model, batch_size, X):
    X = X.reshape(1, 1, len(X))
    yhat = model.predict(X, batch_size=batch_size)
    return yhat[0, 0]


def get_prediction(data, days_ahead=5):
    X = data.title.values
    stat_hypothesis_test(X)

    plt.plot(data.title, color='blue', label='Original')
    plt.plot(pd.rolling_mean(data.title, window=12), color='red', label='Rolling Mean')
    plt.plot(pd.rolling_std(data.title, window=12), color='black', label='Rolling Std')
    plt.plot(pd.ewma(data.title, halflife=12), color='green', label='Weighted moving average')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    history = [x for x in X]
    predicted_arima_5_days_ahead = arima_prediction(history, range(5))
    print('Predicted 5 days ahead values with ARIMA:\n')
    print(predicted_arima_5_days_ahead)
    plt.plot(predicted_arima_5_days_ahead)
    plt.show()

    raw_values = data.title.values
    diff_values = difference(raw_values, 1)
    supervised = timeseries_to_supervised(diff_values, 1)
    supervised_values = supervised.values
    train, test = supervised_values, np.zeros((5, 2))
    scaler, train_scaled, test_scaled = scale(train, test)
    lstm_model = fit_lstm(train_scaled, 1, 5, 4)
    train_reshaped = train_scaled[:, 0].reshape(len(train_scaled), 1, 1)
    lstm_model.predict(train_reshaped, batch_size=1)

    predicted_lstm = []
    for i in range(len(test_scaled)):
        X, y = test_scaled[i, 0:-1], test_scaled[i, -1]
        yhat = forecast_lstm(lstm_model, 1, X)
        yhat = invert_scale(scaler, X, yhat)
        yhat = inverse_difference(raw_values, yhat, len(test_scaled) + 1 - i)
        predicted_lstm.append(yhat)

    print('Predicted 5 days ahead values with LSTM:\n')
    print(predicted_lstm)
    plt.plot(predicted_lstm)
    plt.show()

    raw_values = data.title.values
    diff_values = difference(raw_values, 1)
    supervised = timeseries_to_supervised(diff_values, 1)
    supervised_values = supervised.values
    train, test = supervised_values[:int(len(raw_values) * 0.8)], supervised_values[int(len(raw_values) * 0.8):]
    print('Train set length:\n')
    print(len(train))
    print('Test set length:\n')
    print(len(test))
    scaler, train_scaled, test_scaled = scale(train, test)
    lstm_model = fit_lstm(train_scaled, 1, 5, 4)  # 1, 3000, 4
    train_reshaped = train_scaled[:, 0].reshape(len(train_scaled), 1, 1)
    lstm_model.predict(train_reshaped, batch_size=1)

    predicted_lstm = []
    for i in range(len(test_scaled)):
        X, y = test_scaled[i, 0:-1], test_scaled[i, -1]
        yhat = forecast_lstm(lstm_model, 1, X)
        yhat = invert_scale(scaler, X, yhat)
        yhat = inverse_difference(raw_values, yhat, len(test_scaled) + 1 - i)
        predicted_lstm.append(yhat)

    actuals = raw_values[-len(predicted_lstm):-1]
    predicted_lstm = predicted_lstm[1:]
    print('LSTM RMSE', rmse_test(actuals, predicted_lstm))
    plot_predicted(predicted_lstm, actuals)
    return 0


df_pravda = pd.read_csv('../saved_data/pravda_light_df_all_dates.csv')
print(df_pravda.head())
get_prediction(df_pravda)
