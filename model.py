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
query = ("SELECT prediction1.*, minedtransactions.minedBlock, minedtransactions.gasused FROM prediction1 LEFT JOIN minedtransactions ON prediction1.txHash = minedtransactions.txHash where minedtransactions.minedBlock > 3930236 AND minedtransactions.minedBlock <= 3935650")

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





y, X = dmatrices('confirmTime ~ transfer + hashPowerAccepting + pctLimitGasAbove + pctLimitGasAt + gasOffered + txAbove + txAt', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.GLM(y, X, family=sm.families.Poisson())
results = model.fit()
print (results.summary())


y['predict'] = results.predict()

with pd.option_context('display.max_rows', 5000, 'display.max_columns', None):

    print(y)
 

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