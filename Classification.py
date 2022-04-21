from __future__ import absolute_import, division, print_function

import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
import numpy as np
import pandas as pd
import string
import nltk
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
#LOADING DATA FROM CSV FILE
data_url = 'https://storage.googleapis.com/logicai/ds-recruitment-challenge/data.csv'
data = pd.read_csv(data_url)

#DIVIDING INTO LABELS AND FEATURES
(y, x) = (data.language, data.file_body)

#Removing Comments
xx = []
count = []
xx.clear()
count.clear()
for a in x:
    
    f = open("a.txt", "w")
    f.write("%s" % a)
    f.close()
    f = open("a.txt", "r")
    ff = open("b.txt", "w")
    
    selectedwords = []
    all_lines = f.readlines()   
    
    for one_line in all_lines:
        ff.write("\n")
        words = one_line.split()
        if selectedwords == True:
            newline = " ".join(selectedwords)
            ff.write("%s" % newline)
            selectedwords.clear()
        
        for i in words:
            if selectedwords == True:
                newline = " ".join(selectedwords)
                ff.write("%s" % newline)
                selectedwords.clear()
            if "//" not in i and "#" not in i:
                selectedwords.append(i)
            else:
                newline = " ".join(selectedwords)
                ff.write("%s" % newline)
                selectedwords.clear()
                break
        
        newline = " ".join(selectedwords)
        ff.write("%s" % newline)
        selectedwords.clear() 


    f.close()
    ff.close()
    ff = open("b.txt", "r")
    newcode = ff.read()
    ff.close() 
    os.remove("a.txt")
    os.remove("b.txt")
    b = newcode.split()
    xx.append(b)
    count.append(len(b))

tt = []
tx = []
for t in xx:
    flag = 0
    
    for i in t:
        if '/*' in i:
            flag = 1
        if '*/' in i:
            flag = 0
        if flag == 0:
            if '*/' not in i:
                tt.append(i)
    newline = " ".join(tt)
    tx.append(newline.split())
    tt.clear()

#Padding
bb = []
nx = []
for a in tx:
    bb.clear()
    lena = len(a)
    for i in range(0,250):
        if i < lena:
            c = a[i]
            bb.append(c)
        else:
            c = '0'
            bb.append(c)
    newline = " ".join(bb)
    nx.append(newline.split())

#spliting the data set into test and training data
x_train, x_test, y_train, y_test = train_test_split(nx,y,test_size = 0.4)
train_data = (x_train, y_train)
validation_data = (x_test, y_test)

model = keras.Sequential()
model.add(keras.layers.Embedding(10000, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(19, activation=tf.nn.softmax))
model.summary()

model.compile(optimizer="adam",
              loss="binary_crossentropy",
              metrics=["acc"])


history = model.fit(train_data,
                    validation_data,
                    batch_size = 512,
                    epochs = 40,
                    verbose = 1)

results = model.evaluate(x_test, y_test)

print(results)