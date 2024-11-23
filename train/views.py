from django.shortcuts import redirect, render
from .models import *
from django.http import HttpResponse
import pickle 
import pandas as pd 
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Create your views here.
def train(req):
    return render(req, 'index.html')

def add_train(req):
    if req.method == 'POST':
        data = req.POST
        departure = data.get('departure')
        destination = data.get('destination')
        train_name = data.get('train_name')
        departure_time = data.get('departure_time')
        train_image = req.FILES.get('train_image')

        Train.objects.create(
            departure = departure,
            destination = destination,
            train_name = train_name,
            departure_time = departure_time,
            train_image = train_image
        )

        return redirect('add_train')

        # print(departure)
        # print(destination)
        # print(train_name)
        # print(departure_time)
        # print(train_image)

    return render(req, 'add_train.html')

def search_train(req):
    departure_list = set()
    destination_list = set()

    train_list = Train.objects.all()
    
    for train in train_list:
        departure_list.add(train.departure)
        destination_list.add(train.destination)
    

    if req.method == 'POST':
        data = req.POST
        departure = data.get('departure')
        destination = data.get('destination')

        train_list = Train.objects.filter(departure=departure, destination=destination)

        # print(train_list)

        context = {'departure': departure, 'destination': destination, 'departure_list': departure_list, 'destination_list': destination_list, 'train_list': train_list}

        return render(req, 'search_train.html', context=context)
    
    context = {'departure': 'All', 'destination': 'All','departure_list': departure_list, 'destination_list': destination_list, 'train_list': train_list}
    
    return render(req, 'search_train.html', context=context)

def delete_train(req, id):
    queryset = Train.objects.get(id = id)
    queryset.delete()
    return redirect('search_train')

def update_train(req, id):
    queryset = Train.objects.get(id = id)

    if req.method == 'POST':
        data = req.POST
        departure = data.get('departure')
        destination = data.get('destination')
        train_name = data.get('train_name')
        departure_time = data.get('departure_time')
        train_image = req.FILES.get('train_image')

        queryset.departure = departure
        queryset.destination = destination
        queryset.train_name = train_name
        
        if departure_time:
            queryset.departure_time = departure_time

        if train_image:
            queryset.train_image = train_image

        queryset.save()

        return redirect('search_train')

    return render(req, 'update_train.html', context={'train': queryset})

def load_prediction(req):
    if req.method == 'POST':
        data = req.POST
        departure = data.get('departure')
        destination = data.get('destination')
        date = data.get('date').split('-')

        with open('train/ML/column_transformer.pkl', 'rb') as file: 
            transformer = pickle.load(file)

        with open('train/ML/regression_model.pkl', 'rb') as file: 
            regressor = pickle.load(file)

        date = [int(element) for element in date]

        X_test = pd.DataFrame([departure, destination] + date[::-1]).T

        X_test = transformer.transform(X_test)

        X_test = X_test.toarray()

        predicted_value = regressor.predict(X_test)

        return render(req, 'prediction.html', context={'result': int(predicted_value), 'departure': departure, 'destination': destination, 'date': data.get('date')})

    return render(req, 'load_prediction.html')