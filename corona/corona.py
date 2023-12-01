
import matplotlib as plt
import pandas as pd
import datetime as dt
import numpy as np
data =pd.read_csv("case_time_series.csv")
data['Date'] = pd.to_datetime(data['Date'])
data['Date']=data['Date'].map(dt.datetime.toordinal)
y =data['Daily Confirmed']
X = data['Date']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

X_train= X_train.values.reshape(-1, 1)
X_test= X_test.values.reshape(-1, 1)
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X_train, y_train) #create linear regression object
accuracy = model.score(X_test,y_test)

print('Accuracy:',accuracy*100,'%')

##print ('Coefficient: \n', model.coef_)
##print ('Intercept: \n', model.intercept_) 

n='2020-05-30'
n=input("Enter a date in form yy-mo-day :")
ye,mo,da=map(int,n.split('-'))

ts = pd.Timestamp(year = ye, month = mo, day = da)  
t=np.array(ts.toordinal())
t=t.reshape(-1, 1)
y=model.predict(t)
print("No of cases that might admit on",n,'is',int(y))
