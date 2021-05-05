# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_d5FR1zvkSO0xyijwiAJsk-T6MDlNKj_
"""

import numpy as np
import numpy.random
import sklearn.preprocessing
from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt

def helper():
    mnist = fetch_openml('mnist_784')
    data = mnist['data']
    labels = mnist['target']

    neg, pos = "0", "8"
    train_idx = numpy.random.RandomState(0).permutation(np.where((labels[:60000] == neg) | (labels[:60000] == pos))[0])
    test_idx = numpy.random.RandomState(0).permutation(np.where((labels[60000:] == neg) | (labels[60000:] == pos))[0])

    train_data_unscaled = data[train_idx[:6000], :].astype(float)
    train_labels = (labels[train_idx[:6000]] == pos) * 2 - 1

    validation_data_unscaled = data[train_idx[6000:], :].astype(float)
    validation_labels = (labels[train_idx[6000:]] == pos) * 2 - 1

    test_data_unscaled = data[60000 + test_idx, :].astype(float)
    test_labels = (labels[60000 + test_idx] == pos) * 2 - 1

    # Preprocessing
    train_data = sklearn.preprocessing.scale(train_data_unscaled, axis=0, with_std=False)
    validation_data = sklearn.preprocessing.scale(validation_data_unscaled, axis=0, with_std=False)
    test_data = sklearn.preprocessing.scale(test_data_unscaled, axis=0, with_std=False)
    return train_data, train_labels, validation_data, validation_labels, test_data, test_labels

def sign(val):
    if val >= 0:
        return 1
    return -1

def perceptron(data, labels):
    """	returns: nd array of shape (data.shape[1],) or (data.shape[1],1) representing the perceptron classifier """
    w = np.zeros(784)
    x = sklearn.preprocessing.normalize(data)
    for i in range(len(data)):
        y = sign(np.dot(x[i], w))
        if y != labels[i]:
            w = w + x[i] * labels[i]
    return w

def calc_accuracy(w, test_data, test_labels):
    n =len(test_data)
    x = sklearn.preprocessing.normalize(test_data)
    err_count = 0
    for  i in range(n):
        y = predict(np.dot(x[i], w))   
        if(y != test_labels[i]):    
            err_count += 1
    return 1-(err_count/n)

def question_A(train_data, train_labels, test_data, test_labels):
    cell_val=[]
    size_list = [5, 10, 50, 100, 500, 1000, 5000]
    
    for sample_size in size_list:
        data_labels_sample = np.column_stack((train_data[:sample_size] ,  train_labels[:sample_size]))  
        accuracy = []
        for i in range(100):    #run perceprton 100 times
            np.random.shuffle(data_labels_sample)
            w = perceptron(data_labels_sample[:,0:784], data_labels_sample[:,784])
            accuracy.append(calc_accuracy(w , test_data, test_labels))
        test_result = [np.percentile(accuracy,5) , np.percentile(accuracy,95),np.mean(accuracy)]
        cell_val.append(np.round(test_result,4)) 
    columns = [' 5% ', ' 95% ', ' mean ']
    rows = [' n= 5  ', ' n= 10  ', ' n= 50  ', ' n= 100  ', ' n= 500  ', ' n= 1000  ', ' n= 5000  ']
    table = plt.table(cellText=cell_val, rowLabels=rows, colLabels=columns, loc='top')
    table.auto_set_font_size(False)
    table.set_fontsize(20)
    table.scale(2, 2)
    plt.show()

def question_B(train_data, train_labels):
    w = perceptron(train_data, train_labels)
    plt.imshow(np.reshape(w, (28, 28)), interpolation='nearest')

def question_C(train_data,train_labels,test_data,test_labels):
    w = perceptron(train_data, train_labels)
    print(calc_accuracy(w,test_data,test_labels))

def question_D(train_data,train_labels,test_data,test_labels):
    w = perceptron(train_data, train_labels)
    n =len(test_data)
    err_list=[]
    x = sklearn.preprocessing.normalize(test_data)
    for  i in range(n):
        y = predict(np.dot(x[i], w))   
        if(y != test_labels[i]):    
            err_list.append(i)
    plt.imshow(np.reshape(test_data[np.random.choice(err_list)], (28, 28)), interpolation='nearest')

train_data, train_labels, validation_data, validation_labels, test_data, test_labels = helper()
question_A(train_data, train_labels, test_data, test_labels)

train_data, train_labels, validation_data, validation_labels, test_data, test_labels = helper()
question_B(train_data, train_labels)

question_C(train_data,train_labels,test_data,test_labels)

question_D(train_data,train_labels,test_data,test_labels)