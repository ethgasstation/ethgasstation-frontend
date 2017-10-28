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

query = ("SELECT * FROM snapstore")
cursor.execute(query)
head = cursor.column_names
predictData = pd.DataFrame(cursor.fetchall())
predictData.columns = head
cursor.close()

print ('cleaned transactions: ')
print (len(predictData))


predictData['failed'] = predictData['stillin_txpool'] == 1
predictData['minedBool'] = predictData['block_mined'].notnull().astype(int)

predictData = predictData.loc[predictData['chained']==0]

predictData = predictData.loc[(predictData['minedBool'] == 1) or (predictData['failed']==1)]

print(predictData)

quantiles= predictData['pctLimit'].quantile([.5, .75, .95, .98, .9])
print(quantiles)


predictData['gasCat2'] = ((predictData['pctLimit']>quantiles[.5]) & (predictData['pctLimit']<=quantiles[.75])).astype(int)
predictData['gasCat3'] = ((predictData['pctLimit']>quantiles[.75]) & (predictData['pctLimit']<=quantiles[.9])).astype(int)
predictData['gasCat4'] = (predictData['pctLimit']> quantiles[.9]).astype(int)

predictData['highGasOffered'] = (predictData['pctLimit'] > quantiles[.75]).astype(int)
predictData['highGasOffered2'] = (predictData['pctLimit'] > quantiles[.95]).astype(int)

predictData['dump'] = predictData['numFrom'].apply(lambda x: 1 if x>5 else 0)
predictData['ico'] = predictData['numTo'].apply(lambda x: 1 if x>100 else 0)

newSubmit = predictData[predictData['waitBlocks']==0]

y, X = dmatrices('minedBool ~ hashPowerAccepting + ico + highGasOffered + waitBlocks + txAtAbove', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.GLM(y, X, family=sm.families.Binomial())
results = model.fit()
print (results.summary())

predictData['predict'] = results.predict()

y1, X1 = dmatrices('mined ~ hashPowerAccepting + ico + highGasOffered2  + txAtAbove', data = newSubmit, return_type = 'dataframe')

model = sm.GLM(y1, X1, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

mined = predictData[predictData['minedBool']==1]
notMined = predictData[predictData['minedBool']==0]

print (mined['predict'].mean())
print (mined['predict'].quantile(.05))
print (mined['predict'].quantile(.95))

print ('notMined')
print (notMined['predict'].mean())
print (notMined['predict'].quantile(.05))
print (notMined['predict'].quantile(.95))

'''
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', 75):
    print notMined[['txHash', 'fromAddress', 'blockss', 'postedBlock']][notMined['predict']>.15]
'''

print(mined.loc[mined['predict']<.15, 'mined'])
print(len(notMined.loc[(notMined['waitBlocks']<10) & (notMined['highGasOffered']==0)]))

def calc (row):
    intercept = 1.2910
    hpa = .0321
    dp = 1.0845
    ic = -2.7234
    hgo = -4.4818
    wb = -0.0011

    sum1 = intercept + (row['hashPowerAccepting']*hpa) + (row['dump']*dp) + (row['ico']*ic) + (row['highGasOffered']*hgo) + (row['waitBlocks']*wb)

    factor = np.exp(-1*sum1)
    prob = 1 / (1+factor)
    return prob

predictData['calc'] = predictData.apply(calc, axis=1)
print (predictData.loc[:, ['calc', 'predict']])