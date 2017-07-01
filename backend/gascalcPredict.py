import mysql.connector
import pandas as pd
import numpy as np 
import statsmodels.api as sm
import math
import sys
import os, subprocess, re
import urllib,json

#connect to MySQL with start / end blocks

startBlock = sys.argv[1]
endBlock = sys.argv[2]


cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')

cursor = cnx.cursor()

# First Query to Determine Block TIme, and Estimate Miner Policies
query = ("SELECT txHash, minedGasPrice, toAddress, gasused, miner, tsMined, minedBlock, emptyBlock, minedGasPriceCat FROM minedtransactions WHERE minedBlock > %s AND minedBlock < %s ")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

txData = pd.DataFrame(cursor.fetchall())
txData.columns = head
cursor.close()

start100Block = int(endBlock)-100
endBlock = int(endBlock)


txData['minedGasPrice'] = txData['minedGasPrice'].apply(lambda x: x/1000)
txData['minedGasPrice'] = txData['minedGasPrice'].apply(lambda x: np.round(x, decimals=0) if x >=1 else np.round(x, decimals=3))

txData['txFee'] = txData['gasused']*txData['minedGasPrice']

#summary stats
post = {}
post2 = {}

totalTx = len(txData)
post2['latestblockNum'] = post['latestblockNum'] = int(endBlock)
post2['startSelect'] = post['startSelect'] = int(startBlock)
post['totalCatTx1'] = len(txData[txData['minedGasPriceCat']==1])
post['totalCatTx2'] = len(txData[txData['minedGasPriceCat']==2])
post['totalCatTx3'] = len(txData[txData['minedGasPriceCat']==3])
post['totalCatTx4'] = len(txData[txData['minedGasPriceCat']==4])
post['totalCatTx5'] = len(txData[txData['minedGasPriceCat']==5])
post['totalTx'] = int(totalTx)
post['totalTransfers'] = len(txData[txData['gasused']==21000])
post['totalConCalls'] = len(txData[txData['gasused']!=21000])
post['maxMinedGasPrice'] = int(txData['minedGasPrice'].max())
post['minMinedGasPrice'] = txData['minedGasPrice'].min()
post['minMinedGasPrice'] = int(post['minMinedGasPrice']*1000)
post['medianGasPrice']= int(txData['minedGasPrice'].quantile(.5))
post['avgGasUsed'] = int(txData['gasused'].mean())

post['cheapestTx'] = txData.loc[txData['gasused']==21000, 'txFee'].min()
temp = txData.loc[txData['txFee']==post['cheapestTx'], 'txHash'].reset_index()
post['cheapestTxID'] = temp.loc[0 , 'txHash']
post['cheapestTx'] = int(post['cheapestTx'])

post['dearestTx'] = txData.loc[txData['gasused']==21000, 'txFee'].max()
temp = txData.loc[txData['txFee']==post['dearestTx'], 'txHash'].reset_index()
post['dearestTxID'] = temp.loc[0 , 'txHash']
post['dearestTx'] = int(post['dearestTx'])

post['dearConTx'] = txData['txFee'].max()
temp = txData.loc[txData['txFee']==post['dearConTx'], 'txHash'].reset_index()
post['dearConTxID'] = temp.loc[0 , 'txHash']
post['dearConTx'] = int(post['dearConTx'])

post['avgTxFee'] = int(txData.loc[txData['gasused']==21000, 'txFee'].median())
post['avgContractFee'] = int(txData.loc[txData['gasused']>21000, 'txFee'].median())
post['avgContractGas']  = int(txData.loc[txData['gasused']>21000, 'gasused'].median())

post2['ethConsumedLast100'] = float(txData.loc[(txData['minedBlock']>=start100Block) & (txData['minedBlock']< endBlock), 'txFee'].sum())

# Calculate Each Miners Mininum Price
# First Identify all Unique Miners in list
txDataMiner = pd.DataFrame({'txCount':txData.groupby('miner').size()})
txDataTx = pd.DataFrame({'catCount':txData.groupby(by=['minedGasPriceCat','miner']).size()}).reset_index()
txDataPriceCat = txData.groupby('minedGasPriceCat').mean()
txDataPriceCat = txDataPriceCat.round()
txDataCat = pd.DataFrame({'count':txData.groupby('minedGasPriceCat').size()}).reset_index()
txDataPrice = pd.DataFrame({'count':txData.groupby('minedGasPrice').size()}).reset_index()

#require a price where at least 50 transactions have been mined 

txDataPrice['sum'] = txDataPrice['count'].cumsum()

for index, row in txDataPrice.iterrows():
    if row['sum'] > 12:
        minLow = row['minedGasPrice']
        break



# Next Find Each Miners Mininum Price of All Mined Transactions

minPricePd = txData.groupby('miner').min()
avgPricePd = txData.groupby('miner').mean()
minPricePd = minPricePd[['minedGasPrice', 'minedGasPriceCat']]
avgPricePd = avgPricePd[['minedGasPriceCat']].apply(np.floor)
avgPricePd.rename(columns = {'minedGasPriceCat':'avgCat'}, inplace = True)

txDataMiner = pd.concat([txDataMiner, minPricePd], axis = 1)
txDataMiner = pd.concat([txDataMiner, avgPricePd], axis = 1)

txDataMiner.reset_index(inplace=True)

txDataMiner = txDataMiner.merge(txDataTx, how='left', on=['miner','minedGasPriceCat'])
txDataMiner.rename(columns = {'minedGasPrice': 'minPrice', 'minedGasPriceCat':'minCat'}, inplace = True)

txDataMiner.loc[txDataMiner['minCat']==1, 'catTotal'] = txDataCat.loc[txDataCat['minedGasPriceCat']==1, 'count'].values[0]
txDataMiner.loc[txDataMiner['minCat']==2, 'catTotal'] = txDataCat.loc[txDataCat['minedGasPriceCat']==2, 'count'].values[0]
txDataMiner.loc[txDataMiner['minCat']==3, 'catTotal'] = txDataCat.loc[txDataCat['minedGasPriceCat']==3, 'count'].values[0]
txDataMiner.loc[txDataMiner['minCat']==4, 'catTotal'] = txDataCat.loc[txDataCat['minedGasPriceCat']==4, 'count'].values[0]
txDataMiner.loc[txDataMiner['minCat']==5, 'catTotal'] = txDataCat.loc[txDataCat['minedGasPriceCat']==5, 'count'].values[0]



def getPctCat(cat, minP):
    catTotal = txDataCat.loc[txDataCat['minedGasPriceCat']==cat, 'count'].values[0]
    numAboveMinP = len(txData.loc[(txData['minedGasPriceCat']==cat) & (txData['minedGasPrice']>=minP)])
    x= float(numAboveMinP)/catTotal
    return x

txDataMiner = txDataMiner.dropna()
txDataMiner.reset_index(inplace=True)

for index, row in txDataMiner.iterrows():
    txDataMiner.loc[index, 'pctCat'] = getPctCat(row['minCat'], row['minPrice'])


txDataMiner['pctTotTxMiner'] = txDataMiner['txCount']/float(totalTx)
txDataMiner['expected'] = txDataMiner['catTotal']*txDataMiner['pctCat']*txDataMiner['pctTotTxMiner']
txDataMiner['oeRatio'] = txDataMiner['catCount']/txDataMiner['expected']

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

#Adjust miner's min gas price if they mine < 20% of the expected number of transactions in their low gas price category
#Assign to average price in category


txDataMiner['adjustedMinP'] = txDataMiner['minPrice']
txDataMiner['adjustedMinPCat'] = txDataMiner['minCat']
txDataMiner.loc[txDataMiner['oeRatio'] < 0.2, 'adjustedMinPCat'] = txDataMiner['avgCat']
txDataMiner.loc[(txDataMiner['oeRatio'] <0.2) & (txDataMiner['adjustedMinPCat']==2), 'adjustedMinP'] = txDataPriceCat.loc[2,'minedGasPrice']
txDataMiner.loc[(txDataMiner['oeRatio'] <0.2) & (txDataMiner['adjustedMinPCat']==3), 'adjustedMinP'] = txDataPriceCat.loc[3,'minedGasPrice']
txDataMiner.loc[(txDataMiner['oeRatio'] <0.2) & (txDataMiner['adjustedMinPCat']==4), 'adjustedMinP'] = txDataPriceCat.loc[4,'minedGasPrice']
txDataMiner.loc[(txDataMiner['oeRatio'] <0.2) & (txDataMiner['adjustedMinPCat']==5), 'adjustedMinP'] = txDataPriceCat.loc[5,'minedGasPrice']

txDataMiner  = txDataMiner.sort_values(['adjustedMinP','totBlocks'], ascending = [True, False])

print(txDataMiner)

#Make Table with Key Miner Stats

topMiners = txDataMiner.sort_values('totBlocks', ascending=False)
topMiners = topMiners.loc[:,['miner','adjustedMinP','pctEmp', 'pctTot']].head(10)
topMiners = topMiners.sort_values(['adjustedMinP','pctEmp'], ascending = [True, True]).reset_index(drop=True)



priceTable = txDataMiner[['pctTxBlocks', 'adjustedMinP']].groupby('adjustedMinP').sum().reset_index()
priceTable['pctTotBlocks'] = priceTable['pctTxBlocks']*pctTxBlocks
priceTable['cumPctTxBlocks'] = priceTable['pctTxBlocks'].cumsum()
priceTable['cumPctTotBlocks'] = priceTable['pctTotBlocks'].cumsum()

print(priceTable)

#--Key Miner Stats

#get Initial Gas Price Recs based on % of blocks excluding empty blocks
gpRecs = {}

gpRecs['Cheapest'] = priceTable.loc[0, 'adjustedMinP']
gpRecs['safeLow'] = priceTable.loc[priceTable['cumPctTxBlocks']>=2, 'adjustedMinP'].min()
gpRecs['Average'] = priceTable.loc[priceTable['cumPctTxBlocks']>=50, 'adjustedMinP'].min()
gpRecs['Fastest'] = priceTable.loc[priceTable['cumPctTxBlocks']>=98.5, 'adjustedMinP'].min()

if (gpRecs['Fastest'] <post['medianGasPrice']):
    gpRecs['Fastest'] = post['medianGasPrice']+1


print(gpRecs)


priceTable = priceTable.to_json(orient = 'records')


parentdir = os.path.dirname(os.getcwd())
if not os.path.exists(parentdir + '/json'):
    os.mkdir(parentdir + '/json')

filepath_pricetable = parentdir + '/json/price2.json'

with open(filepath_pricetable, 'w') as outfile:
    outfile.write(priceTable)


cursor.close()
cnx.close()
