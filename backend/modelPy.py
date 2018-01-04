#analysis:  Run poission regression models
import matplotlib
matplotlib.use('Agg')
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


#predictData = predictData.combine_first(postedData)
predictData['confirmBlocks'] = predictData['block_mined']-predictData['block_posted']
print('num with confirm times')
print (predictData['confirmBlocks'].count())
print ('neg confirm time')
print (len(predictData.loc[predictData['confirmBlocks']<0]))
print ('zero confirm time')
print (len(predictData.loc[predictData['confirmBlocks']==0]))
print('pre-chained ' + str(len(predictData)))
predictData.loc[predictData['chained']==1, 'confirmBlocks']=np.nan
predictData = predictData.dropna(subset=['confirmBlocks'])
print('post-chained ' + str(len(predictData)))
predictData = predictData.loc[predictData['confirmBlocks']>0]
predictData = predictData.loc[predictData['tx_atabove']>0]
print ('cleaned transactions: ')
print (len(predictData))

predictData = predictData.dropna(subset=['hashpower_accepting2'])
print (len(predictData))

with pd.option_context('display.max_columns', None,):
    print(predictData)

print('gas offered data')
max_gasoffered = predictData['gas_offered'].max()
print('max :'+str(predictData['gas_offered'].max()))
print('delat at max')
print(predictData.loc[predictData['gas_offered'] == max_gasoffered, 'confirmBlocks'].values[0])
quantiles= predictData['gas_offered'].quantile([.5, .75, .95, .99])
print(quantiles)

#dep['gasCat1'] = (txData2['gasused'] == 21000).astype(int)
predictData['gasCat1'] = ((predictData['gas_offered']<=quantiles[.5])).astype(int)
predictData['gasCat2'] = ((predictData['gas_offered']>quantiles[.5]) & (predictData['gas_offered']<=quantiles[.75])).astype(int)
predictData['gasCat3'] = ((predictData['gas_offered']>quantiles[.75]) & (predictData['gas_offered']<=quantiles[.95])).astype(int)
predictData['gasCat4'] = ((predictData['gas_offered']>quantiles[.95]) & (predictData['gas_offered']<quantiles[.99])).astype(int)
predictData['gasCat5'] = (predictData['gas_offered']>=quantiles[.99]).astype(int)
predictData['hpa2'] = predictData['hashpower_accepting']*predictData['hashpower_accepting']


print ("violations: ")
predictData['violations'] = predictData['expectedWait'] / predictData['confirmBlocks']
predictData['viol2'] = ((predictData['violations']>2.5) & (predictData['confirmBlocks'] > 5) & (predictData['expectedWait'] < 500))

print (predictData['viol2'].sum())
print (predictData['viol2'].count())
print ('%violations = ' + str(predictData['viol2'].sum()/float(predictData['viol2'].count())))

'''
scatter = predictData.loc[(predictData['expectedWait'] < 300) & (predictData['confirmBlocks']<500) & (predictData['expectedWait'] > 2)]
scatter = scatter.sample(n=500)
scatter['actual_blocks_waited'] = scatter['confirmBlocks']
scatter['predicted_blocks_waited'] = scatter['expectedWait']
fig = scatter.plot.scatter(x='actual_blocks_waited', y='predicted_blocks_waited')
sfig = fig.get_figure()
sfig.savefig('scatter.pdf')
'''


#### First Model

y, X = dmatrices('confirmBlocks ~ hashpower_accepting + highgas2 + tx_atabove', data = predictData, return_type = 'dataframe')

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

y['diff'] = y['confirmBlocks'] / y['predict']
y['bad'] = ((y['diff'] > 2.5) & (y['confirmBlocks']>5) & (y['predict'] < 500))

y['too_high'] = ((y['diff'] < 0.25) & (y['predict'] > 5))
y['eligible'] = 1

print ('eligible = ' + str(y['eligible'].sum()))
print ('too high = ' + str(y['too_high'].sum()))
print ('%too high = ' + str(y['too_high'].sum()*100/y['eligible'].sum()))

print ('violations : ' + str(y['bad'].sum()))
print ('violations % = ' +str(y['bad'].sum()*100/float(len(y))))

# Print outliers
print('violations')
print(y.loc[y['bad']==1])


### Second model


predictData.loc[predictData['gp10th'] > 100, 'gp10th'] = 100


a, B = dmatrices('confirmBlocks ~ hashpower_accepting2 + highgas2 + tx_atabove', data = predictData, return_type = 'dataframe')

model = sm.GLM(a, B, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

a['predict'] = results.predict()
a['round_gp_10gwei'] = predictData['round_gp_10gwei']
a['hashpower_accepting'] = predictData['hashpower_accepting']
a['tx_atabove'] = predictData['tx_atabove']
a['highgas2'] = predictData['highgas2']
a['gp10th'] = predictData['gp10th']
print(a)

a['diff'] = a['confirmBlocks'] / a['predict']
a['bad'] = ((a['diff'] > 2.5) & (a['confirmBlocks']>5) & (a['predict'] < 500))

a['too_high'] = ((a['diff'] < 0.25) & (a['predict'] > 5))
a['eligible'] = 1

print ('eligible = ' + str(a['eligible'].sum()))
print ('too high = ' + str(a['too_high'].sum()))
print ('%too high = ' + str(a['too_high'].sum()*100/a['eligible'].sum()))


print ('violations : ' + str(a['bad'].sum()))
print ('violations % = ' +str(a['bad'].sum()*100/float(len(a))))

print('violations')
print(a.loc[a['bad']==1])

### High gas offerred model

c, D = dmatrices('confirmBlocks ~ hashpower_accepting + gasCat2 + gasCat3 + gasCat4 + gasCat5 + tx_atabove', data = predictData, return_type = 'dataframe')


model = sm.GLM(c, D, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

c['predict'] = results.predict()
print(c[:15])
print(D[:15])


### Select transactions for long term storage

pdLowGas = predictData.loc[(predictData['hashpower_accepting'] <= 50) & (predictData['highgas2']==0)]
pdRegGas = predictData.loc[(predictData['hashpower_accepting'] > 50) & (predictData['highgas2']==0)]
pdHgo = predictData.loc[predictData['highgas2'] == 1]

print('low Gp tx')
print(len(pdLowGas))
low_tx_count = len(pdLowGas)
pdRegGas = pdRegGas.sample(n=low_tx_count)

weightedPd = pdLowGas.append(pdRegGas)
weightedPd = weightedPd.append(pdHgo)
print (len(weightedPd))

### model with sampled transactions

e, F = dmatrices('confirmBlocks ~ hashpower_accepting + highgas2 + tx_atabove', data = weightedPd, return_type = 'dataframe')

model = sm.GLM(e, F, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

e['predict'] = results.predict()
print(e[:15])
print(F[:15])

response = input("save data? \n")
if int(response) == 1:
    weightedPd.to_sql(con=engine, name='storedPredict', if_exists='append', index=False)


cursor = cnx.cursor()
query = ("SELECT * FROM storedPredict")
cursor.execute(query)
head = cursor.column_names
predictData = pd.DataFrame(cursor.fetchall())
predictData.columns = head
cursor.close()

predictData['waiting1'] = (predictData['s5mago'] > 0)
predictData['waiting2'] = (predictData['s1hago'] > 0)
predictData['waiting3'] = ((predictData['waiting1']==1) | (predictData['waiting2']==1))

y, X = dmatrices('confirmBlocks ~ hashpower_accepting + highgas2 + tx_atabove', data = predictData, return_type = 'dataframe')

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
y = y.loc[y['round_gp_10gwei'] > 0]
y = y.sort_values('hashpower_accepting')

#with pd.option_context('display.max_rows', None,):

print(y)

a, B = dmatrices('confirmBlocks ~ hashpower_accepting + highgas2 + tx_atabove + waiting1', data = predictData, return_type = 'dataframe')

model = sm.GLM(a, B, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

a['predict'] = results.predict()
a['round_gp_10gwei'] = predictData['round_gp_10gwei']
a['hashpower_accepting'] = predictData['hashpower_accepting']
a['tx_atabove'] = predictData['tx_atabove']
a['highgas2'] = predictData['highgas2']

print(a)

a, B = dmatrices('confirmBlocks ~ hashpower_accepting + highgas2 + tx_atabove + waiting2', data = predictData, return_type = 'dataframe')

model = sm.GLM(a, B, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

a['predict'] = results.predict()
a['round_gp_10gwei'] = predictData['round_gp_10gwei']
a['hashpower_accepting'] = predictData['hashpower_accepting']
a['tx_atabove'] = predictData['tx_atabove']
a['highgas2'] = predictData['highgas2']

print(a)

a, B = dmatrices('confirmBlocks ~ hashpower_accepting + highgas2 + tx_atabove + waiting3', data = predictData, return_type = 'dataframe')

model = sm.GLM(a, B, family=sm.families.Poisson())
results = model.fit()
print (results.summary())

a['predict'] = results.predict()
a['round_gp_10gwei'] = predictData['round_gp_10gwei']
a['hashpower_accepting'] = predictData['hashpower_accepting']
a['tx_atabove'] = predictData['tx_atabove']
a['highgas2'] = predictData['highgas2']

print(a)

'''
y1, X1 = dmatrices('logCTime ~ hashPowerAccepting  + highGasOffered + dump + ico', data = predictData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y1, X1)
results = model.fit()
print (results.summary())
y1['predict'] = results.predict()
y1['confirmBlocks'] = predictData['confirmBlocks']
y1['predictTime'] = y1['predict'].apply(lambda x: np.exp(x))


y2, X2 = dmatrices('logCTime ~ hashPowerAccepting + txAtAbove + dump + ico', data = pdValidate, return_type = 'dataframe')

print(y[:5])
print(X[:5])
'''
