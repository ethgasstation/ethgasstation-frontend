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

'''
#run this the fist time to make complete dataset
query = ("SELECT prediction5.*, minedtransactions.minedBlock, minedtransactions.gasused FROM prediction5 LEFT JOIN minedtransactions ON prediction5.txHash = minedtransactions.txHash")
engine = create_engine('mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)


cursor.execute(query)
head = cursor.column_names
predictData = pd.DataFrame(cursor.fetchall())
predictData.columns = head

compStart = 0
compEnd = 20000
ints = int(len(predictData)/20000)
print ('ints ' + str(ints)) 
for x in range (0, ints):
    predict1 = pd.DataFrame(predictData.iloc[compStart:compEnd, :])
    predict1.to_sql(con=engine, name = 'prediction5complete', if_exists='append', index=True)
    compStart = compStart + 20000
    compEnd = compEnd + 20000
print('compEnd ' + str(compEnd))
predict1 = pd.DataFrame(predictData.iloc[compStart:, :])
predict1.to_sql(con=engine, name = 'prediction5complete', if_exists='append', index=True) 

'''
query = ("SELECT * FROM prediction5complete")
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
predictData['dump'] = predictData['numFrom'].apply(lambda x: 1 if x>5 else 0)
predictData.loc[predictData['confirmTime'] >= 500, 'confirmTime'] = 500
#predictData.loc[predictData['dump']==1, 'confirmTime'] = np.nan
predictData = predictData.dropna(how='any')

print ('cleaned transactions: ')
print (len(predictData))

meanBlock = predictData
meanBlock = meanBlock.drop('txHash', axis=1)
meanBlock = predictData.groupby('postedBlock').mean()

print('txpool mean transactions, median, 95%CI')

avgTxinTxPool = meanBlock['totalTxTxP'].mean()
avgGasLimit = predictData.loc[0, 'gasOffered'] / predictData.loc[0, 'gasOfferedPct']
medianGasOffered = predictData['gasOffered'].median()


print(avgTxinTxPool)
print(meanBlock['totalTxTxP'].quantile(.5))
print(meanBlock['totalTxTxP'].quantile(.05))
print(meanBlock['totalTxTxP'].quantile(.95))


predictData['txAtPctLimit'] = predictData['txAt'].apply(lambda x: x/avgGasLimit)
predictData['txAbovePctLimit'] = predictData['txAbove'].apply(lambda x: x/avgGasLimit)
predictData['totTxPctLimit'] = predictData['totalTxTxP'].apply(lambda x: x/avgGasLimit)



#print(predictData)

predictData['logCTime'] = predictData['confirmTime'].apply(np.log)
predictData['transfer'] = predictData['gasOffered'].apply(lambda x: 1 if x ==21000 else 0) 

print('avgGasLimit= ' + str(avgGasLimit))

transactionGas = float(21000)/avgGasLimit

quantiles= predictData['gasOfferedPct'].quantile([.5, .75, .9, 1])
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

print ('age at mean: ')
print(predictData['ageAt'].mean())


print ('mean confirm low gas price : ')
lowMean = predictData.loc[(predictData['dump']==0) & (predictData['gasPrice'] < 1000), 'confirmTime']
print(lowMean.mean())
print('count:')
print(lowMean.count())


y, X = dmatrices('confirmTime ~ hashPowerAccepting + txAt + dump', data = predictData, return_type = 'dataframe')

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
y['numTo'] = predictData['numTo']
y['numFrom'] = predictData['numFrom']
y['dump'] = predictData['dump']

print(y)

print (y.loc[(y['dump']==0) & (y['gasPrice'] < 1000), ['confirmTime', 'predict', 'gasPrice']])

a, B = dmatrices('confirmTime ~ hashPowerAccepting + txAt + txAbove + dump', data = predictData, return_type = 'dataframe')

print(a[:5])
print(B[:5])

model = sm.GLM(a, B, family=sm.families.Poisson())
results = model.fit()
print (results.summary())



y1, X1 = dmatrices('logCTime ~ hashPowerAccepting + txAt + dump', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y1, X1)
results = model.fit()
print (results.summary())
y1['predict'] = results.predict()
y1['confirmTime'] = predictData['confirmTime']
y1['predictTime'] = y1['predict'].apply(lambda x: np.exp(x))


y2, X2 = dmatrices('logCTime ~ hashPowerAccepting + txAt + txAbove + dump', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y2, X2)
results = model.fit()
print (results.summary())


y3, X3 = dmatrices('logCTime ~ hashPowerAccepting + txAt + txAbove + numFrom', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y3, X3)
results = model.fit()
print (results.summary())

'''
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

