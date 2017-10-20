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
query = ("SELECT * FROM postedtx2")
cursor.execute(query)
head = cursor.column_names
postedData = pd.DataFrame(cursor.fetchall())
postedData.columns = head
'''
query = ("SELECT * FROM minedtx2")
cursor.execute(query)
head = cursor.column_names
predictData = pd.DataFrame(cursor.fetchall())
predictData.columns = head
cursor.close()

#predictData = predictData.combine_first(postedData)
predictData['confirmTime'] = predictData['block_mined']-predictData['block_posted']
print('pre-chained ' + str(len(predictData)))
predictData.loc[predictData['chained']==1, 'confirmTime']=np.nan
predictData = predictData.dropna(subset=['confirmTime'])
print('post-chained ' + str(len(predictData)))
print ('cleaned transactions: ')
print (len(predictData))
'''
#print(predictData)
avgGasLimit = predictData.loc[0, 'gasOffered'] / predictData.loc[0, 'gasOfferedPct']
predictData.loc[predictData['gasOffered']>= (avgGasLimit/1.05), 'confirmTime'] = np.nan
predictData = predictData.dropna(how='any')

print ('cleaned transactions: ')
print (len(predictData))



print ('numTo median:')
print (predictData['numTo'].quantile(.5))

print ('numTo 75%')
print (predictData['numTo'].quantile(.95))




avgGasLimit = predictData.loc[0, 'gasOffered'] / predictData.loc[0, 'gasOfferedPct']
transactionGas = float(21000)/avgGasLimit


quantiles= predictData['gasOfferedPct'].quantile([.5, .75, .9, 1])
print (transactionGas)
print(quantiles)

#dep['gasCat1'] = (txData2['gasused'] == 21000).astype(int)
predictData['gasCat2'] = ((predictData['gasOfferedPct']>transactionGas) & (predictData['gasOfferedPct']<=quantiles[.75])).astype(int)
predictData['gasCat3'] = ((predictData['gasOfferedPct']>quantiles[.75]) & (predictData['gasOfferedPct']<=quantiles[.9])).astype(int)
predictData['gasCat4'] = (predictData['gasOfferedPct']> quantiles[.9]).astype(int)

quantiles2 = predictData['numTo'].quantile([.5, .75, .95])
print('quantiles2')
print(quantiles2)
predictData['numToCat1'] = (predictData['numTo'] <= quantiles2[.5]).astype(int)
predictData['numToCat2'] = ((predictData['numTo'] >quantiles2[.5]) & (predictData['numTo'] <= quantiles2[.75])).astype(int)
predictData['numToCat3'] = ((predictData['numTo'] >quantiles2[.75]) & (predictData['numTo'] <= quantiles2[.95])).astype(int)
predictData['numToCat4'] = (predictData['numTo'] >quantiles2[.95]).astype(int)
predictData.loc[predictData['numTo']==np.nan,'ico']=np.nan
predictData = predictData.dropna(how='any')


print('median gasOfferedPct')
print(transactionGas)
print(quantiles[.5])

predictData['highGasOffered'] = (predictData['gasOfferedPct'] > 0.022).astype(int)

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

print ('mean confirm low gas price : ')
lowMean = predictData.loc[(predictData['dump']==0) & (predictData['gasPrice'] < 1000), 'confirmTime']
print(lowMean.mean())
print('count:')
print(lowMean.count())

predictData['gp1'] = predictData['gasPrice'].apply(lambda x: 1 if x <500 else 0)
predictData['gp2'] = predictData['gasPrice'].apply(lambda x: 1 if (x >=500 and x<1000) else 0)
predictData['gp3'] = predictData['gasPrice'].apply(lambda x: 1 if (x >=1000 and x<4000) else 0)
predictData['gp4'] = predictData['gasPrice'].apply(lambda x: 1 if (x >=4000 and x<23000) else 0)
predictData['gp5'] = predictData['gasPrice'].apply(lambda x: 1 if x >=23000 else 0)
 
pdGp3 = predictData[predictData['gp3']==1]
pdGp4 = predictData[predictData['gp4']==1]
pdGp5 = predictData[predictData['gp5']==1]

pdValidate = pd.DataFrame(predictData.loc[predictData['prediction']>0,:])
pdValidate.loc[pdValidate['hashPowerAccepting'] < 1, 'confirmTime']= np.nan
pdValidate = pdValidate.dropna(how='any')
'''

y, X = dmatrices('confirmTime ~ hashpower_accepting + ico + highgas2 + tx_atabove', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.GLM(y, X, family=sm.families.Poisson())
results = model.fit()
print (results.summary())


y['predict'] = results.predict()
y['round_gp_10gwei'] = predictData['round_gp_10gwei']
y['hashpower_accepting'] = predictData['hashpower_accepting']
y['tx_atabove'] = predictData['tx_atabove']
y['highgas2'] = predictData['highgas2']


print(y)
'''
print (y.loc[(y['dump']==0) & (y['gasPrice'] < 1000), ['confirmTime', 'predict', 'gasPrice']])

a, B = dmatrices('confirmTime ~ hashPowerAccepting + dump + numToCat4 + gasCat4 + txAtAbove', data = predictData, return_type = 'dataframe')


model = sm.GLM(a, B, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

a['predict'] = results.predict()
print(a[:15])
print(B[:15])


a['predict'] = results.predict()
a['gasPrice'] = predictData['gasPrice']
a['hashPowerAccepting'] = predictData['hashPowerAccepting']
a['txAbove'] = predictData['txAbove']
a['txAt'] = predictData['txAt']
a['numFrom'] = predictData['numFrom']
a['dump'] = predictData['dump']

print(a)

print (a.loc[(a['dump']==0) & (a['gasPrice'] < 1000), ['confirmTime', 'predict', 'gasPrice']])



c, D = dmatrices('confirmTime ~ dump + ico + txAtAbove', data = pdGp5, return_type = 'dataframe')



model = sm.GLM(c, D, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

c['predict'] = results.predict()
print(c[:15])
print(D[:15])

e, F = dmatrices('confirmTime ~ gp1+ gp2+ gp3 + gp4 + dump + ico + txAtAbove', data = predictData, return_type = 'dataframe')



model = sm.GLM(e, F, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

e['predict'] = results.predict()
print(e[:15])
print(F[:15])


y1, X1 = dmatrices('logCTime ~ hashPowerAccepting  + highGasOffered + dump + ico', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y1, X1)
results = model.fit()
print (results.summary())
y1['predict'] = results.predict()
y1['confirmTime'] = predictData['confirmTime']
y1['predictTime'] = y1['predict'].apply(lambda x: np.exp(x))


y2, X2 = dmatrices('logCTime ~ hashPowerAccepting + txAtAbove + dump + ico', data = pdValidate, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y2, X2)
results = model.fit()
print (results.summary())

pdValidate['outlier'] = pdValidate['confirmTime'] / pdValidate['prediction']
pdValidate['outlier2'] = pdValidate['outlier'].apply(lambda x: 1 if x>2.5 else 0)
#pdValidate.loc[(pdValidate['outlier']<=3) & (pdValidate['gasPrice']<4000), 'outlier2'] = 0
pdValidate['normalTx']= (pdValidate['ico']==0) & (pdValidate['dump']==0)
pdValidate['lowGPnormal'] = (pdValidate['normalTx']==1) & (pdValidate['gasPrice']<4000) & (pdValidate['gasPrice']>=1000)


print ('mean diff')
print (pdValidate['outlier'].mean())

print ('>2.5 diff')
print (pdValidate['outlier2'].sum())

print ('>2.5 diff no dump no ico')
print (pdValidate.loc[pdValidate['normalTx']==1, 'outlier2'].sum())

print ('total no dump no ico')
print (pdValidate['normalTx'].sum())

print ('total no dump no ico low gas price outliers')
print (pdValidate.loc[pdValidate['lowGPnormal']==1, 'outlier2'].sum())

print ('total no dump no ico low gas price')
print (pdValidate['lowGPnormal'].sum())


#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #print(pdValidate.loc[pdValidate['lowGPnormal']==1, ['prediction', 'confirmTime', 'outlier2']])

print ('total validation')
print (len(pdValidate))




y3, X3 = dmatrices('logCTime ~ hashPowerAccepting + txAtAbove + dump', data = predictData, return_type = 'dataframe')

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

