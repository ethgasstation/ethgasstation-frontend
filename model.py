#analysis:  Run poission regression models

import mysql.connector
import pandas as pd
import numpy as np 
import statsmodels.api as sm
import math
import sys
import os, subprocess, re
import urllib,json
from sqlalchemy import create_engine 
from patsy import dmatrices

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()
query = ("SELECT prediction1.*, minedtransactions.minedBlock, minedtransactions.gasused FROM prediction1 LEFT JOIN minedtransactions ON prediction1.txHash = minedtransactions.txHash")

cursor.execute(query)
head = cursor.column_names
predictData = pd.DataFrame(cursor.fetchall())
predictData.columns = head
cursor.close()

print('total transactions:')
print(len(predictData))
print('total confirmed transactions:')
print(predictData['minedBlock'].count())

predictData['confirmTime'] = predictData['minedBlock']-predictData['postedBlock']


print('zero/neg confirm times: ')
print(predictData[predictData['confirmTime']<=0].count())

predictData[predictData['confirmTime'] <= 0] = np.nan
predictData[predictData['confirmTime'] >= 500] = np.nan
predictData = predictData.dropna(how='any')

print ('cleaned transactions: ')
print (len(predictData))

print(predictData['confirmTime'].count())
#print(predictData)

predictData['logCTime'] = predictData['confirmTime'].apply(np.log)

predictData['transfer'] = predictData['gasOffered'].apply(lambda x: 1 if x ==21000 else 0) 
predictData['gasOffered'] = predictData['gasOffered'].apply(lambda x: x/4710000)
print(predictData['confirmTime'].min())
print(predictData['confirmTime'].max())
print(predictData['hashPowerAccepting'].min())
print(predictData['hashPowerAccepting'].max())

print('gas above mean: ')
print(predictData['pctLimitGasAbove'].mean())

print('gas at mean: ')
print(predictData['pctLimitGasAt'].mean())

print('tx above mean: ')
print(predictData['txAbove'].mean())

print('tx at mean: ')
print(predictData['txAt'].mean())



y, X = dmatrices('confirmTime ~ transfer + hashPowerAccepting + pctLimitGasAbove + pctLimitGasAt + gasOffered + txAbove + txAt', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.GLM(y, X, family=sm.families.Poisson())
results = model.fit()
print (results.summary())


y['predict'] = results.predict()
y['gasPrice'] = predictData['gasPrice']

y1, X1 = dmatrices('logCTime ~ transfer + hashPowerAccepting + pctLimitGasAbove + pctLimitGasAt + gasOffered + txAbove + txAt', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y1, X1)
results = model.fit()
print (results.summary())
y1['predict'] = results.predict()
y1['confirmTime'] = predictData['confirmTime']
y1['pctLimitGasAbove'] = predictData['pctLimitGasAbove']
y1['pctLimitGasAt'] = predictData['pctLimitGasAt']
y1['txAbove'] = predictData['txAbove']
y1['txAt'] = predictData['txAt']
y1['gasOffered'] = predictData['gasOffered']
y1['predictTime'] = y1['predict'].apply(lambda x: np.exp(x))

with pd.option_context('display.max_rows', 5000, 'display.max_columns', None):

    print(y.loc[y['gasPrice']==1000,:])
    print(y1)
 

'''
dep = pd.DataFrame()
indep = pd.DataFrame()
dep = predictData['confirmTime']
indep['const'] = predictData['const']

model = sm.Poisson(dep, indep)
results = model.fit()
print (results.summary())

indep['hashPowerAccepting'] = predictData['hashPowerAccepting']
model = sm.Poisson(dep, indep)
results = model.fit()
print (results.summary())

model = sm.Poisson(predictData['confirmTime'], [predictData['const'], predictData['hashPowerAccepting'], predictData['gasOffered']])
results = model.fit()
print (results.summary())

model = sm.Poisson(predictData['confirmTime'], [predictData['const'], predictData['hashPowerAccepting'], predictData['gasOffered'], predictData['pctLimitGasAbove']])
results = model.fit()
print (results.summary())

'''