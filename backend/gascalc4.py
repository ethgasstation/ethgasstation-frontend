import mysql.connector
import pandas as pd
import numpy as np 
import statsmodels.api as sm
import math
import sys
import os, subprocess, re
import urllib,json
from patsy import dmatrices

#connect to MySQL with start / end blocks

startBlock = sys.argv[1]
endBlock = sys.argv[2]


cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')

cursor = cnx.cursor()

# Get Data from MySql to process stats
query = ("SELECT transactions.txHash, gasPrice, postedBlock, tsPosted, gasOffered, minedtransactions.minedGasPrice, minedtransactions.toAddress, minedtransactions.gasused, minedtransactions.miner, minedtransactions.tsMined, minedtransactions.minedBlock FROM transactions LEFT JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE postedBlock > %s AND postedBlock < %s ")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

txData = pd.DataFrame(cursor.fetchall())
txData.columns = head


# Query to Determine Empty / Full Blokcs
query = ("SELECT speed, gasLimit, numTx, blockNum, miner FROM speedo2 WHERE blockNum > %s AND blockNum < %s AND main = 1 ")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

blockData = pd.DataFrame(cursor.fetchall())
blockData.columns = head
'''
query = ("SELECT * FROM txpool2")

cursor.execute(query)
head = cursor.column_names

txPoolData = pd.DataFrame(cursor.fetchall())
txPoolData.columns = head
'''

cursor.close()


#clean gas price
txData['minedGasPrice'] = txData['minedGasPrice'].apply(lambda x: x/1000)
txData['minedGasPrice'] = txData['minedGasPrice'].apply(lambda x: np.round(x, decimals=0) if x >=1 else np.round(x, decimals=3))

#--cleanGasPrice

#define new Values
txData['txFee'] = txData['gasused']*txData['minedGasPrice']
txData['gasCat1'] = (txData['minedGasPrice'] <= 1)
txData['gasCat2'] = (txData['minedGasPrice']>1) & (txData['minedGasPrice']<= 4)
txData['gasCat3'] = (txData['minedGasPrice']>4) & (txData['minedGasPrice']<= 20)
txData['gasCat4'] = (txData['minedGasPrice']>20) & (txData['minedGasPrice']<= 50)
txData['gasCat5'] = (txData['minedGasPrice']>50) 

blockData['emptyBlocks'] = (blockData['numTx']==0).astype(int)
txData['mined'] = txData['minedBlock'].notnull()


#summary stats
post = {}
gpRecs = {}
totalTx = len(txData)
post['totalCatTx1'] = txData['gasCat1'].sum()
post['totalCatTx2'] = txData['gasCat2'].sum()
post['totalCatTx3'] = txData['gasCat3'].sum()
post['totalCatTx4'] = txData['gasCat4'].sum()
post['totalCatTx5'] = txData['gasCat5'].sum()
post['latestblockNum'] = int(endBlock)
post['totalTx'] = int(totalTx)
post['totalTransfers'] = len(txData[txData['gasused']==21000])
post['totalConCalls'] = len(txData[txData['gasused']!=21000])
post['maxMinedGasPrice'] = int(txData['minedGasPrice'].max())
post['minMinedGasPrice'] = txData['minedGasPrice'].min()
post['minMinedGasPrice'] = int(post['minMinedGasPrice']*1000)
post['medianGasPrice']= int(txData['minedGasPrice'].quantile(.5))
post['avgGasUsed'] = int(txData['gasused'].mean())
post['cheapestTx'] = txData.loc[txData['gasused']==21000, 'txFee'].min()
post['cheapestTxID'] = txData.loc[txData['txFee']==post['cheapestTx'], 'txHash'].values[0]
post['cheapestTx'] = int(post['cheapestTx'])
post['dearestTx'] = txData.loc[txData['gasused']==21000, 'txFee'].max()
post['dearestTxID'] = txData.loc[txData['txFee']==post['dearestTx'], 'txHash'].values[0]
post['dearestTx'] = int(post['dearestTx'])

post['dearConTx'] = txData['txFee'].max()
post['dearConTxID'] = txData.loc[txData['txFee']==post['dearConTx'], 'txHash'].values[0]
post['dearConTx'] = int(post['dearConTx'])

post['avgTxFee'] = int(txData.loc[txData['gasused']==21000, 'txFee'].median())
post['avgContractFee'] = int(txData.loc[txData['gasused']>21000, 'txFee'].median())
post['avgContractGas']  = int(txData.loc[txData['gasused']>21000, 'gasused'].median())


post['emptyBlocks'] =  len(blockData[blockData['speed']==0])
post['fullBlocks'] = len(blockData[blockData['speed']>=.95])
post['totalBlocks'] = len(blockData)

#get ETH Prices
url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR,GBP,CNY"
response = urllib.urlopen(url)
pricesRaw = json.loads(response.read())
response.close()
ethPricesTable = pd.DataFrame.from_dict(pricesRaw, orient='index')

post['ETHpriceUSD'] = int(ethPricesTable.loc['USD', 0])
post['ETHpriceEUR'] = int(ethPricesTable.loc['EUR', 0])
post['ETHpriceCNY'] = int(ethPricesTable.loc['CNY', 0])
post['ETHpriceGBP'] = int(ethPricesTable.loc['GBP', 0])

#--prices

#--summary stats

#Calculate Block Time
blockTime = txData[['tsMined', 'minedBlock']]
blockTime = blockTime.sort_values('minedBlock')
print(blockTime)
blockTime2 = blockTime.groupby('minedBlock', as_index=False).mean()
blockTime2 = blockTime2.diff()
#delete if not consecutive blocks
blockTime2.loc[blockTime2['minedBlock'] > 1, ['tsMined', 'minedBlock']] = np.nan
blockTime2.loc[blockTime2['tsMined']< 0, 'tsMined'] = np.nan
blockInterval = blockTime2['tsMined'].mean()

gpRecs['blockInterval'] = blockInterval

#-- Calculate Block Time

# Calculate Each Miners Mininum Price
# First Identify all Unique Miners in list


txDataMiner = txData[['txHash', 'miner']].groupby('miner').count()
txDataPrice = txData[['txHash', 'minedGasPrice']].groupby('minedGasPrice').count()

#require a price where at least 50 transactions have been mined 

txDataPrice['sum'] = txDataPrice['txHash'].cumsum()
minLowSeries = txDataPrice[txDataPrice['sum']>50].index
gpRecs['minLow'] = minLowSeries.min()

# Next Find Each Miners Mininum Price of All Mined Transactions

minPricePd = txData[['miner', 'minedGasPrice']].groupby('miner').min()
minPricePd = minPricePd.rename(columns={"minedGasPrice": 'minGasPrice'})
avgPricePd = txData[['miner', 'minedGasPrice']].groupby('miner').mean()
avgPricePd = avgPricePd.rename(columns={"minedGasPrice": 'avgGasPrice'})
txDataMiner = pd.concat([txDataMiner, minPricePd], axis = 1)
txDataMiner = pd.concat([txDataMiner, avgPricePd], axis = 1)
gasUsedbyMiner = txData[['miner', 'gasused', 'txFee']].groupby('miner').sum()
gasUsedbyMiner['weightedAvgGP'] = gasUsedbyMiner['txFee'] / gasUsedbyMiner['gasused']
txDataMiner = pd.concat([txDataMiner, gasUsedbyMiner], axis = 1)

print (txDataMiner)


# lowGasPriceWatchList
recent = int(endBlock) - 150
#with pd.option_context('display.max_columns', None):
#   print(txData)

lowPrice = txData.loc[(txData['gasPrice'] < 1000) & (txData['postedBlock'] < recent), ['gasPrice', 'txHash', 'postedBlock', 'mined', 'minedBlock' ]]
lowPrice = lowPrice.sort_values(['gasPrice'], ascending = True).reset_index()

print (lowPrice)

#-- Miner Min PRice

# Calculate Each Miners % Empty and Total Blocks
txBlocks = blockData[['miner','emptyBlocks','blockNum']].groupby('miner').agg({'emptyBlocks':'sum', 'blockNum':'count'})
txDataMiner = pd.concat([txDataMiner, txBlocks], axis = 1)
txDataMiner.reset_index(inplace=True)
txDataMiner = txDataMiner.rename(columns={'index':'miner'})
txDataMiner = txDataMiner.rename(columns = {'blockNum':'totBlocks', 'txHash':'totTx'})


#Convert to percentages
totalBlocks = txDataMiner['totBlocks'].sum()
txDataMiner['pctTot'] = txDataMiner['totBlocks']/totalBlocks*100
txDataMiner['pctEmp'] = txDataMiner['emptyBlocks']/txDataMiner['totBlocks']*100
txDataMiner['txBlocks'] = txDataMiner['totBlocks'] - txDataMiner['emptyBlocks']
totTxBlocks = txDataMiner['txBlocks'].sum()
txDataMiner['pctTxBlocks'] = txDataMiner['txBlocks']/totTxBlocks*100
pctTxBlocks = totTxBlocks/totalBlocks

txDataMiner  = txDataMiner.sort_values(['minGasPrice','totBlocks'], ascending = [True, False])
print(txDataMiner)


#Make Table with Key Miner Stats

topMiners = txDataMiner.sort_values('totBlocks', ascending=False)
topMiners = topMiners.loc[:,['miner','minGasPrice','weightedAvgGP', 'pctTot']].head(10)
topMiners = topMiners.sort_values(['minGasPrice','weightedAvgGP'], ascending = [True, True]).reset_index(drop=True)



priceTable = txDataMiner[['pctTxBlocks', 'minGasPrice']].groupby('minGasPrice').sum().reset_index()
priceTable['pctTotBlocks'] = priceTable['pctTxBlocks']*pctTxBlocks
priceTable['cumPctTxBlocks'] = priceTable['pctTxBlocks'].cumsum()
priceTable['cumPctTotBlocks'] = priceTable['pctTotBlocks'].cumsum()

print(priceTable)


#--Key Miner Stats

#gas guzzler table

gasGuzz = txData.groupby('toAddress').sum()
gasGuzz = gasGuzz.sort_values('gasused', ascending = False)
totgas = gasGuzz['gasused'].sum()
gasGuzz['pcttot'] = gasGuzz['gasused']/totgas*100

gasGuzz = gasGuzz.head(n=10)
gg = {
    '0x6090a6e47849629b7245dfa1ca21d94cd15878ef': 'ENS registrar',
    '0xcd111aa492a9c77a367c36e6d6af8e6f212e0c8e': 'Acronis',
    '0x209c4784ab1e8183cf58ca33cb740efbf3fc18ef': 'Poloniex',
    '0xece701c76bd00d1c3f96410a0c69ea8dfcf5f34e': 'Etheroll',
    '0xa74476443119a942de498590fe1f2454d7d4ac0d': 'Golem',
    '0xedce883162179d4ed5eb9bb2e7dccf494d75b3a0': 'Bittrex',
    '0x70faa28a6b8d6829a4b1e649d26ec9a2a39ba413': 'Shapeshift',
    '0xff1f9c77a0f1fd8f48cfeee58b714ca03420ddac': 'e4row',
    '0x8d12a197cb00d4747a1fe03395095ce2a5cc6819': 'Etherdelta',
    '0xe94b04a0fed112f3664e45adb2b8915693dd5ff3': 'Bittrex Safe Split',
    '0xace62f87abe9f4ee9fd6e115d91548df24ca0943': 'Monaco',
    '0xb9e7f8568e08d5659f5d29c4997173d84cdf2607': 'Swarm City'


}
for index, row in gasGuzz.iterrows():
    if index in gg.keys():
        gasGuzz.loc[index, 'ID'] = gg[index]
    else:
        gasGuzz.loc[index, 'ID'] = ''

gasGuzz = gasGuzz.reset_index()
print(gasGuzz)


#Regression Model for Calculator



txData['delay'] = txData['minedBlock'] - txData['postedBlock']
txData['delay2'] = txData['tsMined'] - txData['tsPosted']
txData[txData['delay'] <= 0] = np.nan
txData[txData['delay2'] <= 0] = np.nan

#create Summary Stats

post['maxMineDelay'] = int(txData['delay'].max())
post['minMineDelay'] = int(txData['delay'].min())
post['medianDelay'] = int(txData['delay'].quantile(.5))
post['delay95'] = int(txData['delay'].quantile(.95))
post['delay5'] = int(txData['delay'].quantile(.05))
post['medianDelayTime'] = int(txData['delay2'].quantile(.5))
post['delay95time'] = int(txData['delay2'].quantile(.95))
post['delay5time'] = int(txData['delay2'].quantile(.05))


#summary delay table


priceWait = txData.loc[:, ['minedGasPrice', 'delay']]
priceWait.loc[priceWait['minedGasPrice']>=40, 'minedGasPrice'] = 40
priceWait = priceWait.loc[(priceWait['minedGasPrice']<=10) | (priceWait['minedGasPrice']==20) | (priceWait['minedGasPrice'] == 40), ['minedGasPrice', 'delay']]
priceWait.loc[priceWait['minedGasPrice']<1, 'minedGasPrice'] = 0
priceWait = priceWait.groupby('minedGasPrice').median()
priceWait.reset_index(inplace=True)
priceWait['delay'] = priceWait['delay']*blockInterval/float(60)


print(priceWait)
#define gas predictors
gpRecs['gasLimit'] = blockData['gasLimit'].mean()
print (gpRecs)


priceTable = priceTable.to_json(orient = 'records')
priceWait = priceWait.to_json(orient = 'records')
miningTable = txDataMiner.to_json(orient = 'records')
topMinerTable = topMiners.to_json(orient = 'records')
gasGuzzTable = gasGuzz.to_json(orient = 'records')
lowGasTable = lowPrice.to_json(orient = 'records')

parentdir = os.path.dirname(os.getcwd())
if not os.path.exists(parentdir + '/json'):
    os.mkdir(parentdir + '/json')
filepath_calc = parentdir + '/json/calc.json'
filepath_recs = parentdir + '/json/ethgas.json'
filepath_pricetable = parentdir + '/json/price.json'
filepath_predictTable = parentdir + '/json/price3.json'
filepath_miners = parentdir + '/json/miners.json'
filepath_gasguzz = parentdir + '/json/gasguzz.json'
filepath_topMiners = parentdir + '/json/topMiners.json'
filepath_priceWait = parentdir + '/json/priceWait.json'
filepath_txData10k = parentdir + '/json/txData10k.json'
filepath_lowgas = parentdir + '/json/validated.json'


with open(filepath_recs, 'w') as outfile:
    json.dump(gpRecs, outfile)

with open(filepath_pricetable, 'w') as outfile:
    outfile.write(priceTable)

with open(filepath_miners, 'w') as outfile:
    outfile.write(miningTable)

with open(filepath_gasguzz, 'w') as outfile:
    outfile.write(gasGuzzTable)

with open(filepath_topMiners, 'w') as outfile:
    outfile.write(topMinerTable)

with open(filepath_priceWait, 'w') as outfile:
    outfile.write(priceWait)

with open(filepath_lowgas, 'w') as outfile:
    outfile.write(lowGasTable)

with open(filepath_txData10k, 'w') as outfile:
    json.dump(post, outfile)

print(post)

