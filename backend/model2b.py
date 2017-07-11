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

query = ("SELECT * FROM prediction2complete")
cursor.execute(query)
head = cursor.column_names
predictData = pd.DataFrame(cursor.fetchall())
predictData.columns = head
avgGasLimit2 = 6704158

predictData['dataset'] = 'a'
predictData['congestedCont'] = predictData['totalTxTxP'].apply(lambda x: x/avgGasLimit2)
predictData = predictData.drop_duplicates(subset = 'txHash')

query = ("SELECT * FROM prediction1complete")
cursor.execute(query)
head = cursor.column_names
predictData2 = pd.DataFrame(cursor.fetchall())
predictData2.columns = head
cursor.close()
predictData2['dataset'] = 'b'
avgGasLimit1 = 4710940
predictData2['congestedCont'] = predictData2['totalTxTxP'].apply(lambda x: x/avgGasLimit1)
predictData2 = predictData2.drop_duplicates(subset = 'txHash')


predictData = predictData.append(predictData2).reset_index(drop=True)





print('total transactions:')
print(len(predictData))
print('total confirmed transactions:')
print(predictData['minedBlock'].count())

predictData['confirmTime'] = predictData['minedBlock']-predictData['postedBlock']

print('zero/neg confirm times: ')
print(predictData[predictData['confirmTime']<=0].count())

predictData = predictData.drop(['gasOfferedPct', 'gasUsed', 'gasused', 'totalGasTxP'], axis=1)

predictData.loc[predictData['confirmTime'] <= 0, 'confirmTime'] = np.nan
predictData.loc[predictData['confirmTime'] >= 500, 'confirmTime'] = 500
predictData = predictData.dropna(how='any')

print ('cleaned transactions: ')
print (len(predictData))

meanBlock = predictData
meanBlock = meanBlock.drop('txHash', axis=1)
meanBlock = predictData.groupby('postedBlock').mean()

print('txpool mean transactions, median, 95%CI')

avgTxinTxPool = meanBlock['totalTxTxP'].mean()
#avgGasLimit = predictData.loc[0, 'gasOffered'] / predictData.loc[0, 'gasOfferedPct']
medianGasOffered = predictData['gasOffered'].median()

#predictData['congested'] = predictData['totalTxTxP'].apply(lambda x: 1 if x >= avgTxinTxPool else 0)


predictData['congestedcontXtxabove'] = predictData['congestedCont'] * predictData['txAbove']
#predictData['congestedXtxat'] = predictData['congested'] * predictData['txAt']
#predictData['congestedXpctLimitAbove'] = predictData['congested'] * predictData['pctLimitGasAbove']


print(avgTxinTxPool)
print(meanBlock['totalTxTxP'].quantile(.5))
print(meanBlock['totalTxTxP'].quantile(.05))
print(meanBlock['totalTxTxP'].quantile(.95))


#predictData['txAtPctLimit'] = predictData['txAt'].apply(lambda x: x/avgGasLimit)
#predictData['txAbovePctLimit'] = predictData['txAbove'].apply(lambda x: x/avgGasLimit)
#predictData['totTxPctLimit'] = predictData['totalTxTxP'].apply(lambda x: x/avgGasLimit)



#print(predictData)

predictData['logCTime'] = predictData['confirmTime'].apply(np.log)

predictData['transfer'] = predictData['gasOffered'].apply(lambda x: 1 if x ==21000 else 0) 


#print('avgGasLimit= ' + str(avgGasLimit1))

#transactionGas = float(21000)/avgGasLimit1

#quantiles= predictData['gasOfferedPct'].quantile([.5, .75, .9, 1])
#print (transactionGas)
#print(quantiles)

#dep['gasCat1'] = (txData2['gasused'] == 21000).astype(int)
#predictData['gasCat2'] = ((predictData['gasOfferedPct']>transactionGas) & (predictData['gasOfferedPct']<=quantiles[.75])).astype(int)
#predictData['gasCat3'] = ((predictData['gasOfferedPct']>quantiles[.75]) & (predictData['gasOfferedPct']<=quantiles[.9])).astype(int)
#predictData['gasCat4'] = (predictData['gasOfferedPct']> quantiles[.9]).astype(int)

#print('median gasOfferedPct')
#print(quantiles[.5])

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

print(predictData)


y, X = dmatrices('confirmTime ~ hashPowerAccepting + transfer + pctLimitGasAbove + pctLimitGasAt + totalTxTxP', data = predictData, return_type = 'dataframe')

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
#y['gasCat2'] = predictData['gasCat2']
#y['gasCat3'] = predictData['gasCat3']
#y['gasCat4'] = predictData['gasCat4']
#y['congested'] = predictData['congested']
y['congestedCont'] = predictData['congestedCont']

print(y)

'''
a, B = dmatrices('confirmTime ~ hashPowerAccepting + transfer + congestedXtxabove + txAbove + txAt + pctLimitGasAbove + congestedXpctLimitAbove + pctLimitGasAt', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.GLM(a, B, family=sm.families.Poisson())
results = model.fit()
print (results.summary())
'''


y1, X1 = dmatrices('logCTime ~ hashPowerAccepting + transfer  + pctLimitGasAbove + pctLimitGasAt + totalTxTxP', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y1, X1)
results = model.fit()
print (results.summary())
y1['predict'] = results.predict()
y1['confirmTime'] = predictData['confirmTime']
y1['predictTime'] = y1['predict'].apply(lambda x: np.exp(x))

'''

y2, X2 = dmatrices('logCTime ~ hashPowerAccepting + transfer + congestedCont + congested + txAbove + txAt', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y2, X2)
results = model.fit()
print (results.summary())

y3, X3 = dmatrices('logCTime ~ hashPowerAccepting + transfer + congestedCont + congestedXtxabove + txAbove + txAt', data = predictData, return_type = 'dataframe')

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

