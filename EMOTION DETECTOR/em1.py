import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv("EMOTION.csv")

from sklearn.preprocessing import LabelEncoder
cat_var =data.dtypes.loc[data.dtypes == 'object'].index
le =LabelEncoder()
for var in cat_var:
    data[var] = le.fit_transform(data[var])

x=data.iloc[:,0:5].values
y=data.iloc[:,5].values

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.7)


###Naive Bayes classifier
##from sklearn.naive_bayes import GaussianNB 
##gnb = GaussianNB().fit(x_train, y_train)

def emopred(X):
    from sklearn.naive_bayes import GaussianNB 
    gnb = GaussianNB().fit(x_train, y_train)
    Y= gnb.predict(X)
    return Y
