import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import math
import sys
import os, subprocess, re
import urllib,json

#connect to MySQL with start / end blocks

startBlock = sys.argv[1]
endBlock = sys.argv[2]
cnx = mysql.connector.connect(user='jake', password='dopamine', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

# First Query to Determine Block TIme, and Estimate Miner Policies
query = ("SELECT minedGasPrice, miner, tsMined, minedBlock, emptyBlock FROM minedtransactions WHERE minedBlock > %s AND minedBlock < %s ")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

txData = pd.DataFrame(cursor.fetchall())
txData.columns = head
cursor.close()

#Calculate Block Time
blockTime = txData[['tsMined', 'minedBlock']]
blockTime = blockTime.sort_values('minedBlock')
blockTime2 = blockTime.groupby('minedBlock', as_index=False).mean()
blockTime2 = blockTime2.diff()
#delete if not consecutive blocks
blockTime2.loc[blockTime2['minedBlock'] > 1, ['tsMined', 'minedBlock']] = np.nan
blockInterval = blockTime2['tsMined'].mean()

blockTime = {
    'blockInterval':blockInterval
}
#-- Calculate Block Time

# Calculate Each Miners Mininum Price
# First Identify all Unique Miners in list
txDataMiner = pd.DataFrame({'count':txData.groupby('miner').size()}).reset_index()
txDataMiner = txDataMiner.sort_values('count', ascending=False).reset_index(drop=True)

# Next Find Each Miners Mininum Price of All Mined Transactions
for x in range(len(txDataMiner)):
    minerName = txDataMiner.loc[x,'miner']
    minP = txData.loc[txData['miner'] == txDataMiner.loc[x,'miner'], 'minedGasPrice']
    txDataMiner.loc[x,'minPrice'] = minP.min()

#-- Miner Min PRice

# Calculate Each Miners % Empty and Total Blocks
txBlocks = txData[['miner','emptyBlock','minedBlock']].groupby(['minedBlock','miner', 'emptyBlock']).size().reset_index()

totalBlocks = len(txBlocks)

for x in range(len(txDataMiner)):
    totMinerBlocks = len(txBlocks[txBlocks['miner']==txDataMiner.loc[x,'miner']])
    txDataMiner.loc[x,'totBlocks']= totMinerBlocks
    totEmptyBlocks = len(txBlocks[(txBlocks['miner']==txDataMiner.loc[x,'miner']) & (txBlocks['emptyBlock']==1)])
    txDataMiner.loc[x,'emptyBlocks'] = totEmptyBlocks


#Convert to percentages
txDataMiner['pctTot'] = txDataMiner['totBlocks']/totalBlocks
txDataMiner['pctEmp'] = txDataMiner['emptyBlocks']/txDataMiner['totBlocks']

#Distinguish between Empty blocks and those that contain Tx
txDataMiner['txBlocks'] = txDataMiner['totBlocks'] - txDataMiner['emptyBlocks']
totTxBlocks = txDataMiner['txBlocks'].sum()
txDataMiner['pctTxBlocks'] = txDataMiner['txBlocks']/totTxBlocks

pctTxBlocks = totTxBlocks/totalBlocks

#Make Table with Key Miner Stats
priceTable = txDataMiner[['pctTxBlocks', 'minPrice']].groupby('minPrice').sum().reset_index()
priceTable['pctTotBlocks'] = priceTable['pctTxBlocks']*pctTxBlocks


#make cumulative columns to see hashpower abover given minimum price
y=0
for x in range(len(priceTable)):
    if (y==0):
      priceTable.loc[x,'cumPctTxBlocks'] = priceTable.loc[x,'pctTxBlocks']
    else:
        priceTable.loc[x,'cumPctTxBlocks'] = priceTable.loc[x-1,'cumPctTxBlocks'] + priceTable.loc[x,'pctTxBlocks']
    y=y+1

y=0

for x in range(len(priceTable)):
    if (y==0):
      priceTable.loc[x, 'cumPctTotBlocks'] = priceTable.loc[x, 'pctTotBlocks']
    else:
        priceTable.loc[x, 'cumPctTotBlocks'] = priceTable.loc[x-1, 'cumPctTotBlocks'] + priceTable.loc[x, 'pctTotBlocks']
    y=y+1

#--cumulative columns

#get Initial Gas Price Recs based on % of blocks excluding empty blocks
gpRecs = {}

for x in range(len(priceTable)):
    if (priceTable.loc[x, 'cumPctTxBlocks']) >= .05:
        gpRecs['safeLow'] = priceTable.loc[x, 'minPrice']
        break
for x in range(len(priceTable)):
    if (priceTable.loc[x, 'cumPctTxBlocks']) >= .50:
        gpRecs['Average'] = priceTable.loc[x, 'minPrice']
        break
for x in range(len(priceTable)):
    if (priceTable.loc[x, 'cumPctTxBlocks']) >= .99:
        gpRecs['Fastest'] = priceTable.loc[x, 'minPrice']
        break

print(gpRecs)

url = "http://localhost/backend/validated.json"
response = urllib.urlopen(url)
validation = json.loads(response.read())
response.close()

#findLowest validated status

validationTable = pd.DataFrame.from_dict(validation, orient='index')
validationTable.sort_index()
validationTable= validationTable.reset_index()
print(validationTable)

for x in range(len(validationTable)):
    lowestMined = validationTable[validationTable.loc[x,'mined']==True, 'minedBlock']
    break

print (lowestMined)

for x in range(len(validationTable)):
    lowestRejected = validationTable[validationTable.loc[x,'mined']==False, 'index']
    break

if (lowestRejected):
    print('hi')
    for x in range(len(validationTable)):
        lowestMined = validationTable[(validationTable.loc[x,'mined']=='True') & (validationTable.loc[x,'index']>lowestRejected), 'index']
        break

if (lowestRejected):
    if (lowestMined > gpRecs['safeLow']):
        gpRecs['safeLow'] = lowestMined

print (gpRecs)
print (lowestRejected)




#Poisson Regression

cursor = cnx.cursor()
query = ("SELECT (minedtransactions.minedBlock - transactions.postedBlock) as delay, minedtransactions.gasused, transactions.gasOffered, minedtransactions.minedGasPrice FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock IS NOT NULL AND transactions.postedBlock > %s AND transactions.postedBlock < %s ORDER BY delay")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

txData = pd.DataFrame(cursor.fetchall())
txData.columns = head

txData['delay'] = pd.to_numeric(txData['delay'], errors='coerce')
txData = txData.dropna()


#define gas predictors

dep = pd.DataFrame()
dep['priceCat1'] = (txData['minedGasPrice'] < gpRecs['Average']).astype(int)
dep['priceCat2'] = (txData['minedGasPrice'] == gpRecs['Average']).astype(int)
dep['priceCat3'] = ((txData['minedGasPrice'] > gpRecs['Average']) & (txData['minedGasPrice'] < gpRecs['Fastest'])).astype(int)
dep['priceCat4'] = (txData['minedGasPrice'] > gpRecs['Fastest']).astype(int)


# Define gasused cats

quantiles= txData['gasused'].quantile([.5, .75, .9, 1])


dep['gasCat2'] = ((txData['gasused']>21000) & (txData['gasused']<=quantiles[.75])).astype(int)
dep['gasCat3'] = ((txData['gasused']>quantiles[.75]) & (txData['gasused']<=quantiles[.9])).astype(int)
dep['gasCat4'] = (txData['gasused']> quantiles[.9]).astype(int)

dep = sm.add_constant(dep)

indep = txData['delay']

model = sm.Poisson(indep, dep.iloc[:,[0,1,3,4,5,6,7]])


results = model.fit(disp=0)
dictResults = dict(results.params)


quantiles = quantiles.reset_index(drop=True)
quantiles.rename({0: '50pct', 1: '75pct', 2: '90pct', 3: 'max'}, inplace=True)
quantiles = quantiles.to_dict()

dictResults.update(quantiles)
dictResults.update(blockTime)
dictResults.update(gpRecs)

parentdir = os.path.dirname(os.getcwd())
filepath_calc = parentdir + '/json/calc.html'

with open(filepath_calc, 'w') as outfile:
    json.dump(dictResults, outfile)

print (results.summary())
print (gpRecs)


'''
dep['predict'] = results.predict()
dep['delay'] = indep
print(dep)
'''



#cursor.close()
cnx.close()
