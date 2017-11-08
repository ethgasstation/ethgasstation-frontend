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
engine = create_engine(
    'mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)

query = ("SELECT * FROM minedtx2")
cursor.execute(query)
head = cursor.column_names
predictData = pd.DataFrame(cursor.fetchall())
predictData.columns = head
cursor.close()

def check(row):
    if row['tx_atabove'] < row['tx_unchained']:
        return 1
    return 0

#predictData = predictData.combine_first(postedData)
predictData['confirmTime'] = predictData['block_mined']-predictData['block_posted']
print ('neg confirm time')
print (len(predictData.loc[predictData['confirmTime']<0]))
print ('zero confirm time')
print (len(predictData.loc[predictData['confirmTime']==0]))
print('pre-chained ' + str(len(predictData)))
predictData.loc[predictData['chained']==1, 'confirmTime']=np.nan
predictData = predictData.dropna(subset=['confirmTime', 'tx_unchained'])
print('post-chained ' + str(len(predictData)))
predictData = predictData.loc[predictData['confirmTime']>0]
print (len(predictData))
predictData = predictData.loc[predictData['tx_atabove']>0]
predictData['error'] = predictData.apply(check, axis=1)
print ('cleaned transactions: ')
print (len(predictData))
predictData = predictData.loc[predictData['error']==0]
print (len(predictData))
'''
#print(predictData)
avgGasLimit = predictData.loc[0, 'gasOffered'] / predictData.loc[0, 'gas_offered']
predictData.loc[predictData['gasOffered']>= (avgGasLimit/1.05), 'confirmTime'] = np.nan
predictData = predictData.dropna(how='any')

print ('cleaned transactions: ')
print (len(predictData))



print ('numTo median:')
print (predictData['numTo'].quantile(.5))

print ('numTo 75%')
print (predictData['numTo'].quantile(.95))

'''

print('gas offered data')
max_gasoffered = predictData['gas_offered'].max()
print('max :'+str(predictData['gas_offered'].max()))
print('delat at max')
print(predictData.loc[predictData['gas_offered'] == max_gasoffered, 'confirmTime'].values[0])
quantiles= predictData['gas_offered'].quantile([.5, .75, .95, .99])
print(quantiles)

#dep['gasCat1'] = (txData2['gasused'] == 21000).astype(int)
predictData['gasCat1'] = ((predictData['gas_offered']<=quantiles[.5])).astype(int)
predictData['gasCat2'] = ((predictData['gas_offered']>quantiles[.5]) & (predictData['gas_offered']<=quantiles[.75])).astype(int)
predictData['gasCat3'] = ((predictData['gas_offered']>quantiles[.75]) & (predictData['gas_offered']<=quantiles[.95])).astype(int)
predictData['gasCat4'] = ((predictData['gas_offered']>quantiles[.95]) & (predictData['gas_offered']<quantiles[.99])).astype(int)
predictData['gasCat5'] = (predictData['gas_offered']>=quantiles[.99]).astype(int)

predictData['hpa2'] = predictData['hashpower_accepting']*predictData['hashpower_accepting']



y, X = dmatrices('confirmTime ~ hashpower_accepting + highgas2 + tx_atabove + hgXhpa', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.GLM(y, X, family=sm.families.Poisson())
results = model.fit()
print (results.summary())


y['predict'] = results.predict()
y['round_gp_10gwei'] = predictData['round_gp_10gwei']
y['hashpower_accepting'] = predictData['hashpower_accepting']
y['tx_atabove'] = predictData['tx_atabove']
y['tx_unchained'] = predictData['tx_unchained']
y['highgas2'] = predictData['highgas2']


print(y)
'''
print (y.loc[(y['dump']==0) & (y['gasPrice'] < 1000), ['confirmTime', 'predict', 'gasPrice']])
'''

a, B = dmatrices('confirmTime ~ hashpower_accepting + highgas2 + tx_atabove + hpa2 + hgXhpa', data = predictData, return_type = 'dataframe')


model = sm.GLM(a, B, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

a['predict'] = results.predict()



a['predict'] = results.predict()
a['round_gp_10gwei'] = predictData['round_gp_10gwei']
a['hashpower_accepting'] = predictData['hashpower_accepting']
a['tx_atabove'] = predictData['tx_atabove']
a['tx_unchained'] = predictData['tx_unchained']
a['highgas2'] = predictData['highgas2']

print(a)



c, D = dmatrices('confirmTime ~ hashpower_accepting + gasCat2 + gasCat3 + gasCat4 + gasCat5 + tx_atabove', data = predictData, return_type = 'dataframe')



model = sm.GLM(c, D, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

c['predict'] = results.predict()
print(c[:15])
print(D[:15])


pdLowGas = predictData.loc[(predictData['round_gp_10gwei'] < 5) & (predictData['highgas2']==0)]
pdRegGas = predictData.loc[(predictData['round_gp_10gwei'] >= 5) & (predictData['round_gp_10gwei'] < 20) & (predictData['highgas2']==0)]
pdHighGas = predictData.loc[(predictData['round_gp_10gwei'] >=20) & (predictData['highgas2']==0)]
pdHgo = predictData.loc[predictData['highgas2'] == 1]

print('low Gp tx')
print(len(pdLowGas))
low_tx_count = len(pdLowGas)
pdRegGas = pdRegGas.sample(n=low_tx_count)
pdHighGas =pdHighGas.sample(n=low_tx_count)

weightedPd = pdLowGas.append(pdRegGas)
weightedPd = weightedPd.append(pdHighGas)
weightedPd = weightedPd.append(pdHgo)
print (len(weightedPd))


e, F = dmatrices('confirmTime ~ hashpower_accepting + highgas2 + hgXhpa+ tx_atabove + hgXhpa', data = weightedPd, return_type = 'dataframe')


model = sm.GLM(e, F, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

e['predict'] = results.predict()
print(e[:15])
print(F[:15])

response = input("save data (1=y) \n")
if int(response) == 1:
    weightedPd.to_sql(con=engine, name='storedPredict', if_exists='append', index=False)



'''



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
'''