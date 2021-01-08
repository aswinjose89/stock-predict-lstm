# Create your views here.
from stock_prediction.views import BaseView
from django.shortcuts import render
import pandas_datareader as pdr

import plotly.graph_objects as go
import plotly.offline as opy
import numpy as np
import io
import urllib, base64
from keras.models import load_model
import tensorflow as tf
import matplotlib.pyplot as plt
from django.conf import settings
from model_training.models import CompanyModelDtls

class StockPrediction:
    company_model_qs = CompanyModelDtls.objects.all()
    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), 0]  ###i=0, 0,1,2,3-----99   100
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    def load_model_file(self, company):
        model_name = "{}.h5".format(company)
        company_model_qs = self.company_model_qs.get(symbol=company)
        model_folder_path = '{}/trained_models/{}'.format(settings.MEDIA_ROOT, company_model_qs.country)
        full_model_path = '{}/{}'.format(model_folder_path, model_name)
        # model = load_model(full_model_path)
        model = tf.keras.models.load_model(full_model_path)
        return model
    def prediction_plot(self, dataset, X_train, X_test, company):
        model = self.load_model_file(company)
        ### Lets Do the prediction and check performance metrics
        train_predict = model.predict(X_train)
        test_predict = model.predict(X_test)

        ##Transformback to original form
        train_predict = self.scaler.inverse_transform(train_predict)
        test_predict = self.scaler.inverse_transform(test_predict)

        ### Plotting
        # shift train predictions for plotting
        look_back = 100
        trainPredictPlot = np.empty_like(dataset)
        trainPredictPlot[:, :] = np.nan
        trainPredictPlot[look_back:len(train_predict) + look_back, :] = train_predict
        # shift test predictions for plotting
        testPredictPlot = np.empty_like(dataset)
        testPredictPlot[:, :] = np.nan
        testPredictPlot[len(train_predict) + (look_back * 2) + 1:len(dataset) - 1, :] = test_predict
        # plot baseline and predictions
        plt.plot(self.scaler.inverse_transform(dataset))
        plt.plot(trainPredictPlot)
        plt.plot(testPredictPlot)
        plt.show()

    def future_prediction_plot(self, dataset, company, no_of_pred_days= 30):
        import pdb
        pdb.set_trace()
        model = self.load_model_file(company)
        # model = load_model('stock_prediction.h5')
        # demonstrate prediction for next 10 days
        lst_output = []
        n_steps = 100
        i = 0

        while (i < no_of_pred_days):
            if (len(temp_input) > 100):
                # print(temp_input)
                x_input = np.array(temp_input[1:])
                print("{} day input {}".format(i, x_input))
                x_input = x_input.reshape(1, -1)
                x_input = x_input.reshape((1, n_steps, 1))
                # print(x_input)
                yhat = model.predict(x_input, verbose=0)
                print("{} day output {}".format(i, yhat))
                temp_input.extend(yhat[0].tolist())
                temp_input = temp_input[1:]
                # print(temp_input)
                lst_output.extend(yhat.tolist())
                i = i + 1
            else:
                x_input = x_input.reshape((1, n_steps, 1))
                yhat = model.predict(x_input, verbose=0)
                print(yhat[0])
                temp_input.extend(yhat[0].tolist())
                print(len(temp_input))
                lst_output.extend(yhat.tolist())
                i = i + 1
        day_new = np.arange(1, 101)
        day_pred = np.arange(101, 131)
        pdb.set_trace()
        plt.plot(day_new, self.scaler.inverse_transform(dataset[1158:]))
        plt.plot(day_pred, self.scaler.inverse_transform(lst_output))
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format="jpeg")
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        # temp["layer_neurons"].append({"plot": uri, "weights": str(activations[i][0, :, :,val])})
        # temp["layer_neurons"].append({"plot": uri})
        return uri



class StockPredictionView(BaseView, StockPrediction):
    template_name = "stock_prediction.html"
    key = "4ebd09eedc8be62930e7100691539f1a4014f81f"

    def get_context_data(self, *args, **kwargs):
        context = super(StockPredictionView, self).get_context_data(*args, **kwargs)
        # dataset = self.load_dataset("A")

        # context['candle_stick_graph'] = self.candle_stick_chart(dataset)
        return context
    def load_dataset(self, company):
        ds = pdr.get_data_tiingo(company, api_key=self.key)
        filename= '{}.csv'.format(company)
        ds.to_csv(filename)
        return ds

    def candle_stick_chart(self, dataset):
        # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
        date= self.get_column_data(dataset, 'date')
        open = self.get_column_data(dataset, 'open')
        high = self.get_column_data(dataset, 'high')
        low = self.get_column_data(dataset, 'low')
        close = self.get_column_data(dataset, 'close')
        # fig = go.Figure(data=[go.Candlestick(x=df['Date'],
        #                                      open=df['AAPL.Open'],
        #                                      high=df['AAPL.High'],
        #                                      low=df['AAPL.Low'],
        #                                      close=df['AAPL.Close'])])
        fig = go.Figure(data=[go.Candlestick(x=date,
                                             open=open,
                                             high=high,
                                             low=low,
                                             close=close)])
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div
    def get_column_data(self, ds, col= 'close'):
        ds1 = ds.reset_index()[col]
        return ds1

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        get_data = request.GET
        import pdb
        pdb.set_trace()
        trainedCompanies = get_data.getlist('trainedCompanies') if get_data.getlist('trainedCompanies') else []
        no_of_pred_days = int(get_data.get('pred_days')) if get_data.get('pred_days') else 30
        if trainedCompanies:
            candle_stick = []
            pred_plot_list = []
            for company in trainedCompanies:
                dataset = self.load_dataset(company)
                closed_stock = self.get_column_data(dataset)
                train_data, test_data = self.data_processing(closed_stock)
                time_step = 100
                # X_train, y_train = self.create_dataset(train_data, time_step)
                # X_test, ytest = self.create_dataset(test_data, time_step)

                # self.prediction_plot(closed_stock, X_train, X_test)
                pred_plot= self.future_prediction_plot(closed_stock, company, no_of_pred_days)
                pred_plot_list.append({"pred_plot": pred_plot})
                # candle_stick_chart= self.candle_stick_chart(dataset)
                # candle_stick.append(candle_stick_chart)
            context['pred_plot_list'] = pred_plot_list
            context['candle_stick_graph'] = candle_stick
        return render(request, self.template_name, context)






