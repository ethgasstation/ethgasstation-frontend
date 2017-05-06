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
txDataMiner['pctTot'] = txDataMiner['totBlocks']/totalBlocks*100
txDataMiner['pctEmp'] = txDataMiner['emptyBlocks']/txDataMiner['totBlocks']*100

#Distinguish between Empty blocks and those that contain Tx
txDataMiner['txBlocks'] = txDataMiner['totBlocks'] - txDataMiner['emptyBlocks']
totTxBlocks = txDataMiner['txBlocks'].sum()
txDataMiner['pctTxBlocks'] = txDataMiner['txBlocks']/totTxBlocks*100

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

print(priceTable)
#--cumulative columns

#get Initial Gas Price Recs based on % of blocks excluding empty blocks
gpRecs = {}

gpRecs['Cheapest'] = priceTable.loc[0, 'minPrice']

for x in range(len(priceTable)):
    if (priceTable.loc[x, 'cumPctTxBlocks']) >= 5:
        gpRecs['safeLow'] = priceTable.loc[x, 'minPrice']
        break
for x in range(len(priceTable)):
    if (priceTable.loc[x, 'cumPctTxBlocks']) >= 50:
        gpRecs['Average'] = priceTable.loc[x, 'minPrice']
        break
for x in range(len(priceTable)):
    if (priceTable.loc[x, 'cumPctTxBlocks']) >= 99:
        gpRecs['Fastest'] = priceTable.loc[x, 'minPrice']
        break

print(gpRecs)

url = "http://localhost/json/validated.json"
response = urllib.urlopen(url)
validation = json.loads(response.read())
response.close()

#findLowest validated status

validationTable = pd.DataFrame.from_dict(validation, orient='index')
validationTable.sort_index()
validationTable= validationTable.reset_index()
print(validationTable)


#Check if transactions are rejceted, is so, find one with higher gas price or one with lower gas price but mined later

rejected = validationTable.loc[validationTable['mined']==False, ['index', 'postedBlock']]

if not (rejected.empty):
    rejectedMaxgp = rejected['index'].max()
    rejMaxPostedBlock = rejected['postedBlock'].max()

    #check to see if there is an accepted gas price above the highest rejected
    acceptGp = validationTable.loc[(validationTable['mined'] == True) & (validationTable['index'] > rejectedMaxgp)]
    if not(acceptGp.empty):
        acceptGp = acceptGp['index'].min()
    else:
        acceptGp = None

    #check to see if there is an accepted gas price lower than rejected but mined later
    latestGp =  validationTable.loc[(validationTable['mined'] == True) & (validationTable['postedBlock'] > rejMaxPostedBlock)]
    if not (latestGp.empty):
        latestGp= latestGp['index'].min()
    else:
        latestGp = None
    
    print (acceptGp, latestGp)
    if ((acceptGp is not None) & (latestGp is not None)):
        acceptGp = int(acceptGp)
        latestGp = int(latestGp)
        gpRecs['safeLow']= min(acceptGp, latestGp)
    elif (acceptGp is not None):
        gpRecs['safeLow'] = acceptGp
    elif (latestGp is not None):
        gpRecs['safeLow'] = latestGp
    else:
        gpRecs['safeLow'] = gpRecs['Average']
    


print (gpRecs)


#Poisson Regression

cursor = cnx.cursor()
query = ("SELECT (minedtransactions.minedBlock - transactions.postedBlock) as delay, minedtransactions.gasused, transactions.gasOffered, minedtransactions.minedGasPrice FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock IS NOT NULL AND transactions.postedBlock > %s AND transactions.postedBlock < %s ORDER BY delay")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

txData = pd.DataFrame(cursor.fetchall())
txData.columns = head

txData['delay'] = pd.to_numeric(txData['delay'], errors='coerce')
txData[txData['delay']>1000] = np.nan
txData = txData.dropna()


#define gas predictors

dep = pd.DataFrame()
dep['priceCat1'] = (txData['minedGasPrice'] < gpRecs['Average']).astype(int)
dep['priceCat2'] = (txData['minedGasPrice'] == gpRecs['Average']).astype(int)
dep['priceCat3'] = ((txData['minedGasPrice'] > gpRecs['Average']) & (txData['minedGasPrice'] < gpRecs['Fastest'])).astype(int)
dep['priceCat4'] = (txData['minedGasPrice'] > gpRecs['Fastest']).astype(int)


# Define gasused cats

quantiles= txData['gasused'].quantile([.5, .75, .9, 1])

dep['gasCat1'] = (txData['gasused'] == 21000).astype(int)
dep['gasCat2'] = ((txData['gasused']>21000) & (txData['gasused']<=quantiles[.75])).astype(int)
dep['gasCat3'] = ((txData['gasused']>quantiles[.75]) & (txData['gasused']<=quantiles[.9])).astype(int)
dep['gasCat4'] = (txData['gasused']> quantiles[.9]).astype(int)

dep['cons'] = 1

indep = txData['delay']

model = sm.Poisson(indep, dep.loc[:,['priceCat1', 'priceCat3', 'priceCat4', 'gasCat1', 'gasCat3', 'gasCat4', 'cons']])

results = model.fit(disp=0)
dictResults = dict(results.params)
dep['predict'] = results.predict()


#check to see if really fastest
predictAverage = dep.loc[(dep['priceCat1']==2) & (dep['gasCat1']==1), 'predict'].mean()
predictFastest = dep.loc[(dep['priceCat1']==4) & (dep['gasCat1']==1), 'predict'].mean()

if (predictFastest > predictAverage):
    gpRecs['Fastest'] = gpRecs['Average']


quantiles = quantiles.reset_index(drop=True)
quantiles.rename({0: '50pct', 1: '75pct', 2: '90pct', 3: 'max'}, inplace=True)
quantiles = quantiles.to_dict()

dictResults.update(quantiles)
dictResults.update(blockTime)
mining = priceTable.to_json
watch = validationTable.to_json


parentdir = os.path.dirname(os.getcwd())
filepath_calc = parentdir + '/json/calc.json'
filepath_recs = parentdir + '/json/ethgasAPI.json'
filepath_mining = parentdir + '/json/mining.json'
filepath_watch = parentdir + 'json/watch.json'

with open(filepath_calc, 'w') as outfile:
    json.dump(dictResults, outfile)

with open(filepath_recs, 'w') as outfile:
    json.dump(gpRecs, outfile)

with open(filepath_mining, 'w') as outfile:
    outfile.write(mining)

with open(filepath_watch, 'w') as outfile:
    outfile.write(watch)

print (results.summary())
print (gpRecs)


'''

'''



#cursor.close()
cnx.close()
