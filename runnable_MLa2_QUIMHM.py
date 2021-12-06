# -*- coding: utf-8 -*-
"""MLa2_QUIMHM.ipynb

Automatically generated by Colaboratory. (AND ADAPTED TO RUN ON A LOCAL ENVIRONMENT)

Original file is located at
    https://colab.research.google.com/drive/10z2ddq9q3nHDsoVqoLBRwcSr9tVuCSK6

# **ML ASSIGNMENT 2: LOVEY DOVEY DATA**
by QUIM DE LAS HERAS MOLINS (21123349)
"""

#IMPORTS AND NEEDED LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve,roc_auc_score

import tensorflow as tf
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier

"""**IMPORTING** OF THE DATASET (EDITABLE TO CHANGE INPUT SOURCE ACCORDINGLY)"""

# Load dataset
dataset = pd.read_csv('/train-io.txt', sep=' ', header=None)

# Inspect data and check correct reading 
dataset.head()

"""DATA **INSPECTION**"""

# Print Dataframe information summary (100000 samples, no nulls, 10 features and 1 binary output label, different ranges for each feature)
print(dataset.describe())
print(dataset.info())

"""DATA **PREPARATION**"""

# Separate features and labels into X and y
X, y = dataset.iloc[:, 0: 10].values, dataset.iloc[:,10].values

# Split into train and test sets (to check against overfitting, 0.8-0.2 rate chosen, could be 0.66-0.33 etc)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 69)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# Input X features normalized, scaled to 0-1 range
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""MODEL **CONFIGURATION**"""

col_count = X.shape[1]
activator = 'relu'
nodes = 1000 
max_layers = 2  #3
max_epochs = 50 #25#100#250#500#1000
max_batch = 256 #32#64#128#512#1000
loss_funct = 'binary_crossentropy' #binary classifier
last_act = 'sigmoid' #binary classifier
adam = tf.keras.optimizers.Adam(learning_rate=0.001)

def baseline_model():
    # create model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(nodes, input_dim=col_count, activation=activator)) #input layer with 10 input_dim
    for x in range(0, max_layers):
        #model.add(tf.keras.layers.Dropout(0.2)) #tried in order to mitigate overfiting but discarded due to lack of results (and solid knowledge about)
        model.add(tf.keras.layers.Dense(nodes, input_dim=nodes, activation=activator)) #hidden layers(2) with 1000 input_dim   
    model.add(tf.keras.layers.Dense(1, activation=last_act)) 
    # Compile model
    model.compile(loss=loss_funct, optimizer=adam, metrics=['accuracy'])
    return model

"""MODEL **TRAINING**"""

estimator = KerasClassifier(build_fn=baseline_model, epochs=max_epochs, batch_size=max_batch)
estimator.fit(X_train,y_train)

"""ESTIMATOR **EVALUATION**"""

y_pred = estimator.predict(X_test)

#using confusion matrix
cm = confusion_matrix(y_test, y_pred)
score = np.sum(cm.diagonal())/float(np.sum(cm))
print(score)

#by hand (accuracy on X_test)
sum=0
total=0
for y1,y2 in zip(y_test,y_pred):
  if y1==y2: sum+=1
  total+=1
print(sum, sum/total)

#by hand (accuracy on X_train, higher than X_test's -> some overfitting)
y_pred = estimator.predict(X_train)
sum=0
total=0
for y1,y2 in zip(y_train,y_pred):
  if y1==y2: sum+=1
  total+=1
print(sum, sum/total)

"""# test-i **PREDICTION** AND **WRITING** TO test-o"""

X_assessment = pd.read_csv('/test-i.txt', sep=' ', header=None)
X_assessment = sc.transform(X_assessment)
y_pred = estimator.predict(X_assessment)
print(y_pred)

np.savetxt("/test-o.txt", y_pred, delimiter="\n",fmt='%d')

"""# **MIXTURE** OF EXPERTS (NAIVE LOW-LEVEL _bad_ IMPLEMENTATION)"""
"""
n_e = 3
experts = []
max_epochs = 75
max_batch = 256
nodes = 1000//n_e
for i in range(n_e):
  inputX = X_train[i*len(X_train)//n_e:((i+1)*len(X_train)//n_e)-1] #non-overlaying segments of X_train used for different experts
  inputY = y_train[i*len(y_train)//n_e:((i+1)*len(y_train)//n_e)-1]
  experts.append(KerasClassifier(build_fn=baseline_model, epochs=max_epochs, batch_size=max_batch))
  experts[i].fit(inputX,inputY)

y1 = experts[0].predict(X_test)
y2 = experts[1].predict(X_test)
y3 = experts[2].predict(X_test)
y_pred = (y1+y2+y3>1.5) #"gating function"

sum=0
total=0
for y1,y2 in zip(y_test,y_pred):
  if y1==y2: sum+=1
  total+=1
print(sum, sum/total) # the final accuracy on X_test isn't better
"""
