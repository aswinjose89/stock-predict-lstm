from django.shortcuts import render
import os
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

### Create the Stacked LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from datetime import datetime
from django.utils import timezone
from stock_prediction.views import BaseView
from django.conf import settings

from .models import CompanyModelDtls, CompanyModelDtlsHstry

class ModelTraining:
    key = "4ebd09eedc8be62930e7100691539f1a4014f81f"
    scaler = MinMaxScaler(feature_range=(0, 1))
    company_model_qs= CompanyModelDtls.objects.all()
    company_model_hstry_qs = CompanyModelDtlsHstry.objects.all()

    def load_dataset(self, company):
        ds = pdr.get_data_tiingo(company, api_key=self.key)
        filename= '{}.csv'.format(company)
        ds.to_csv(filename)
        return ds

    def get_column_data(self, ds, col= 'close'):
        ds1 = ds.reset_index()[col]
        return ds1

    def data_processing(self, ds):
        df1 = self.scaler.fit_transform(np.array(ds).reshape(-1, 1))
        ##splitting dataset into train and test split
        percentage_of_data= 0.65 #65% percentage of data to be in training dataset
        training_size = int(len(df1) * percentage_of_data)
        test_size = len(df1) - training_size
        train_data, test_data = df1[0:training_size, :], df1[training_size:len(df1), :1]
        return train_data, test_data

    # convert an array of values into a dataset matrix
    def create_dataset(self, dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), 0]  ###i=0, 0,1,2,3-----99   100
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    def stock_training(self, X_train, y_train, X_test, ytest, **kwargs):
        # reshape input to be [samples, time steps, features] which is required for LSTM
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
        company = kwargs["company"]
        epoch = kwargs["epoch"]
        time_step = kwargs["time_step"]
        batch_size = kwargs["batch_size"]
        model_loss = kwargs["model_loss"]
        model_optimizer = kwargs["model_optimizer"]
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
        model.add(LSTM(50, return_sequences=True))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(loss=model_loss, optimizer=model_optimizer)
        model.fit(X_train, y_train, validation_data=(X_test, ytest), epochs=epoch, batch_size=batch_size, verbose=1)
        dt = datetime.now()
        # trained_model_time = dt.strftime('%d.%m.%Y %H:%M:%S')
        model_name = "{}.h5".format(company)
        company_model_qs = self.company_model_qs.get(symbol=company)
        model_folder_path = '{}/trained_models/{}'.format(settings.MEDIA_ROOT, company_model_qs.country)
        if not(os.path.exists(model_folder_path)):
            os.makedirs(model_folder_path)
        full_model_path = '{}/{}'.format(model_folder_path, model_name)
        model.save(full_model_path)
        model_summaryList = []
        model.summary(print_fn=lambda x: model_summaryList.append(x))
        short_model_summary = "\n".join(model_summaryList)
        company_model_qs.model_name= model_name
        company_model_qs.model_summary= short_model_summary
        company_model_qs.file_path = model_folder_path
        company_model_qs.model_loss = model_loss
        company_model_qs.model_optimizer = model_optimizer
        company_model_qs.epoch = epoch
        company_model_qs.batch_size = batch_size
        company_model_qs.days = time_step
        company_model_qs.is_trained = True
        current_time = datetime.now(tz=timezone.utc)
        company_model_qs.trained_on = current_time
        company_model_qs.save()
        # Trained Model History
        company_model_hstry_obj = {
            "company": company_model_qs,
            "model_loss": model_loss,
            "model_optimizer": model_optimizer,
            "epoch": epoch,
            "batch_size": batch_size,
            "days": time_step,
        }
        self.company_model_hstry_qs.create(**company_model_hstry_obj)
        return model_summaryList

class StockModelTrainingView(BaseView, ModelTraining):
    template_name = "model_training.html"

    def get_context_data(self, *args, **kwargs):
        context = super(StockModelTrainingView, self).get_context_data(*args, **kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        get_data = request.GET
        companies = get_data.getlist('companies') if get_data.getlist('companies') else []
        epoch = int(get_data.get('epoch')) if get_data.get('epoch') else None
        batchsize = int(get_data.get('batchsize')) if get_data.get('batchsize') else None
        model_loss = get_data.get('model_loss') if get_data.get('model_loss') else None
        model_optimizer = get_data.get('model_optimizer') if get_data.get('model_optimizer') else None
        # time_step = int(get_data.get('days')) if get_data.get('days') else None
        for company in companies:
            dataset = self.load_dataset(company)
            closed_stock = self.get_column_data(dataset)
            train_data, test_data = self.data_processing(closed_stock)
            time_step = 100 #100 days timestep for next prediction.Means every prediction values evaluated based on last 100 days timestep
            X_train, y_train = self.create_dataset(train_data, time_step)
            X_test, ytest = self.create_dataset(test_data, time_step)
            kwargs = {
                "company": company,
                "epoch": epoch,
                "time_step": time_step,
                "batch_size": batchsize,
                "model_loss": model_loss,
                "model_optimizer": model_optimizer,
            }
            stock_training_dtls = self.stock_training(X_train, y_train, X_test, ytest, **kwargs)
            context['stock_training_dtls'] = stock_training_dtls
        return render(request, self.template_name, context)


