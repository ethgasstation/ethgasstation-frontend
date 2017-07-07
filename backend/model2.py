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
query = ("SELECT prediction2.*, minedtransactions.minedBlock, minedtransactions.gasused FROM prediction2 LEFT JOIN minedtransactions ON prediction2.txHash = minedtransactions.txHash")

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
predictData.loc[predictData['confirmTime'] >= 500, 'confirmTime'] = 500
predictData = predictData.dropna(how='any')

print ('cleaned transactions: ')
print (len(predictData))

print(predictData['confirmTime'].count())
#print(predictData)

predictData['logCTime'] = predictData['confirmTime'].apply(np.log)

predictData['transfer'] = predictData['gasOffered'].apply(lambda x: 1 if x ==21000 else 0) 

avgGasLimit = predictData.loc[0, 'gasOffered'] / predictData.loc[0, 'gasOfferedPct']
transactionGas = float(21000)/avgGasLimit

quantiles= predictData['pctGasOffered'].quantile([.5, .75, .9, 1])
print (transactionGas)
print(quantiles)

#dep['gasCat1'] = (txData2['gasused'] == 21000).astype(int)
predictData['gasCat2'] = ((predictData['gasOfferedPct']>transactionGas) & (predictData['gasOfferedPct']<=quantiles[.75])).astype(int)
predictData['gasCat3'] = ((predictData['gasOfferedPct']>quantiles[.75]) & (predictData['gasOfferedPct']<=quantiles[.9])).astype(int)
predictData['gasCat4'] = (predictData['gasOfferedPct']> quantiles[.9]).astype(int)

print('median gasOfferedPct')
print(transactionGas)
print(quantiles[.5])

print('confirmTImes')
print(predictData['confirmTime'].min())
print(predictData['confirmTime'].max())

print('hashPowerAccepting')
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



y, X = dmatrices('confirmTime ~ hashPowerAccepting + pctLimitGasAbove + pctLimitGasAt + gasCat2 + gasCat3 + gasCat4 + txAbove + txAt', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.GLM(y, X, family=sm.families.Poisson())
results = model.fit()
print (results.summary())


y['predict'] = results.predict()
y['gasPrice'] = predictData['gasPrice']
y['pctLimitGasAbove'] = predictData['pctLimitGasAbove']
y['pctLimitGasAt'] = predictData['pctLimitGasAt']
y['txAbove'] = predictData['txAbove']
y['txAt'] = predictData['txAt']
y['gasOffered'] = predictData['gasOffered']
y['transfer'] = predictData['transfer']
y['gasCat2'] = predictData['gasCat2']
y['gasCat3'] = predictData['gasCat3']
y['gasCat4'] = predictData['gasCat4']

print(y)

'''
y1, X1 = dmatrices('logCTime ~ transfer + hashPowerAccepting + pctLimitGasAbove + pctLimitGasAt + gasOffered + txAbove + txAt', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y1, X1)
results = model.fit()
print (results.summary())
y1['predict'] = results.predict()
y1['confirmTime'] = predictData['confirmTime']
y1['predictTime'] = y1['predict'].apply(lambda x: np.exp(x))


y2, X2 = dmatrices('logCTime ~ hashPowerAccepting + pctLimitGasAbove + pctLimitGasAt + gasCat2 + gasCat3 + gasCat4 + txAbove + txAt', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y2, X2)
results = model.fit()
print (results.summary())

y3, X3 = dmatrices('logCTime ~ hashPowerAccepting + pctLimitGasAbove + pctLimitGasAt + gasCat2 + gasCat3 + gasCat4 + totalTxTxP', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y3, X3)
results = model.fit()
print (results.summary())

y4, X4 = dmatrices('logCTime ~ hashPowerAccepting + gasOffered', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y4, X4)
results = model.fit()
print (results.summary())





with pd.option_context('display.max_rows', 500, 'display.max_columns', None):

    print(y.loc[(y['gasPrice']==1000) & (y['transfer']==1),:])
    print(y.loc[(y['gasPrice']>=50000) & (y['transfer']==1),:])
 
'''

