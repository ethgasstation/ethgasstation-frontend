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


# Query to Determine Empty / Full Blokcs
cursor = cnx.cursor()
query = ("SELECT speed FROM speedo2 WHERE blockNum > %s AND blockNum < %s ")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

txData3 = pd.DataFrame(cursor.fetchall())
txData3.columns = head
cursor.close()

post['emptyBlocks'] =  len(txData3[txData3['speed']==0])
post['fullBlocks'] = len(txData3[txData3['speed']>=.95])
post['totalBlocks'] = len(txData3)

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
txDataMiner = pd.DataFrame({'txCount':txData.groupby('miner').size()})
txDataTx = pd.DataFrame({'catCount':txData.groupby(by=['minedGasPriceCat','miner']).size()}).reset_index()
txDataPriceCat = txData.groupby('minedGasPriceCat').mean()
txDataCat = pd.DataFrame({'count':txData.groupby('minedGasPriceCat').size()}).reset_index()
txDataPrice = pd.DataFrame({'count':txData.groupby('minedGasPrice').size()}).reset_index()

#require a price where at least 50 transactions have been mined 

txDataPrice['sum'] = txDataPrice['count'].cumsum()

for index, row in txDataPrice.iterrows():
    if row['sum'] > 50:
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

print(gpRecs)


try:
    url = "http://localhost/json/validated.json"
    response = urllib.urlopen(url)
    validation = json.loads(response.read())
    response.close()
    if any(validation):
        validationTable = pd.DataFrame.from_dict(validation, orient='index')
    else:
        validation = {
        'mined': [True],
        'index': [0],
        'postedBlock': [0]

        }
        validationTable = pd.DataFrame.from_dict(validation, orient='columns')

except:
    validation = {
        'mined': [True],
        'index': [0],
        'postedBlock': [0]

    }
    validationTable = pd.DataFrame.from_dict(validation, orient='columns')

#findLowest validated status

validationTable.sort_index()
validationTable= validationTable.reset_index(drop=False)
validationTable['gasPrice'] = validationTable['gasPrice'].apply(lambda x: x/1000)
validationTable['gasPrice'] = validationTable['gasPrice'].apply(lambda x: np.round(x, decimals=0) if x >=1 else np.round(x, decimals=1))
print(validationTable)


#Check if transactions are rejceted, is so, find one with higher gas price or one with lower gas price but mined later

rejected = validationTable.loc[validationTable['mined']==False, ['index', 'postedBlock']]

if not (rejected.empty):
    rejectedMaxgp = rejected['index'].max()
    rejMaxPostedBlock = rejected['postedBlock'].max()

    #check to see if there is an accepted gas price above the highest rejected
    acceptGp = validationTable.loc[(validationTable['mined'] == True) & (validationTable['index'] > rejectedMaxgp)]
    if not(acceptGp.empty):
        acceptGp = int(round(acceptGp['gasPrice'].min()))
    else:
        acceptGp = None

    #check to see if there is an accepted gas price lower than rejected but mined later
    latestGp =  validationTable.loc[(validationTable['mined'] == True) & (validationTable['postedBlock'] > rejMaxPostedBlock)]
    if not (latestGp.empty):
        latestGp= int(round(latestGp['gasPrice'].min()))
    else:
        latestGp = None
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
    

if gpRecs['safeLow'] > gpRecs['Average']:
    gpRecs['safeLow'] = gpRecs['Average']

print (gpRecs)

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
    '0xece701c76bd00d1c3f96410a0c69ea8dfcf5f34e': 'Oraclize',
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

cursor = cnx.cursor()
query = ("SELECT minedtransactions.minedBlock, transactions.postedBlock, minedtransactions.tsMined, transactions.tsPosted, minedtransactions.gasused, transactions.postedblock, minedtransactions.minedblock, transactions.gasOffered, minedtransactions.minedGasPrice FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > %s AND transactions.postedBlock < %s")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names
txData2 = pd.DataFrame(cursor.fetchall())
txData2.columns = head
cursor.close()

#change gas price from mwei to gwei but don't round if less than 1 gwei
txData2['minedGasPrice'] = txData2['minedGasPrice'].apply(lambda x: x/1000)
print(txData2['minedGasPrice'].min())
txData2['minedGasPrice'] = txData2['minedGasPrice'].apply(lambda x: np.round(x, decimals=0) if x >=1 else np.round(x, decimals=3))
print(txData2['minedGasPrice'].min())

txData2['delay'] = txData2['minedBlock'] - txData2['postedBlock']
txData2['delay2'] = txData2['tsMined'] - txData2['tsPosted']
txData2[txData2['delay']>1000] = np.nan
txData2[txData2['delay'] < 0] = np.nan
txData2[txData2['delay2'] < 0] = np.nan
txData2 = txData2.dropna()

if (gpRecs['safeLow'] < minLow):
    gpRecs['safeLow'] = minLow

if (gpRecs['safeLow'] == 0):
    gpRecs['safeLow'] = 1



#create Summary Stats

post['totalTimed'] = len(txData2)
post['maxMineDelay'] = int(txData2['delay'].max())
post['minMineDelay'] = int(txData2['delay'].min())
post['medianDelay'] = int(txData2['delay'].quantile(.5))
post['delay95'] = int(txData2['delay'].quantile(.95))
post['delay5'] = int(txData2['delay'].quantile(.05))
post['medianDelayTime'] = int(txData2['delay2'].quantile(.5))
post['delay95time'] = int(txData2['delay2'].quantile(.95))
post['delay5time'] = int(txData2['delay2'].quantile(.05))
post2['medianDelayLast100'] = int(txData2.loc[(txData2['minedBlock']>=start100Block) & (txData2['minedBlock']< endBlock), 'delay2'].median())

#write Summary Stats
print(post)
cursor = cnx.cursor()
query = ("INSERT INTO txDataLast10k "
        "(totalTimed, maxMineDelay, minMineDelay, medianMinedDelay, medianTime, latestblockNum, startSelect, cat1gasTotTx, cat2gasTotTx, cat3gasTotTx, cat4gasTotTx, cat5gasTotTx, totalTx, totalTransfers, totalConCalls, maxMinedGasPrice, minMinedGasPrice, medianGasPrice, totalBlocks, avgGasUsed, cheapestTx, cheapestTxID, dearestTx, dearestTxID, dearConTx, dearConTxID, mediantxFee, avgContractFee, avgContractGas, ETHpriceUSD, ETHpriceEUR, ETHpriceGBP, ETHpriceCNY, emptyBlocks, fullBlocks)"
        "VALUES (%(totalTimed)s, %(maxMineDelay)s, %(minMineDelay)s, %(medianDelay)s, %(medianDelayTime)s, %(latestblockNum)s, %(startSelect)s, %(totalCatTx1)s, %(totalCatTx2)s, %(totalCatTx3)s, %(totalCatTx4)s, %(totalCatTx5)s, %(totalTx)s, %(totalTransfers)s, %(totalConCalls)s, %(maxMinedGasPrice)s, %(minMinedGasPrice)s, %(medianGasPrice)s, %(totalBlocks)s, %(avgGasUsed)s, %(cheapestTx)s, %(cheapestTxID)s, %(dearestTx)s, %(dearestTxID)s, %(dearConTx)s, %(dearConTxID)s, %(avgTxFee)s, %(avgContractFee)s, %(avgContractGas)s, %(ETHpriceUSD)s, %(ETHpriceEUR)s, %(ETHpriceGBP)s, %(ETHpriceCNY)s, %(emptyBlocks)s, %(fullBlocks)s)")
        
        
cursor.execute(query, post)
cnx.commit()

query = ("INSERT INTO txDataLast100b "
        "(ethConsumedLast100, medianDelayLast100, latestblockNum, startSelect)"
        "VALUES (%(ethConsumedLast100)s, %(medianDelayLast100)s, %(latestblockNum)s, %(startSelect)s)")

cursor.execute(query, post2)
cnx.commit()
cursor.close()

#--summary stats for mysql

#summary table

#summary delay table


priceWait = txData2.loc[:, ['minedGasPrice', 'delay']]
priceWait.loc[priceWait['minedGasPrice']>=40, 'minedGasPrice'] = 40
priceWait = priceWait.loc[(priceWait['minedGasPrice']<=10) | (priceWait['minedGasPrice']==20) | (priceWait['minedGasPrice'] == 40), ['minedGasPrice', 'delay']]
priceWait.loc[priceWait['minedGasPrice']<1, 'minedGasPrice'] = 0
priceWait['delay'] = priceWait['delay'].apply(np.log)
priceWait = priceWait.groupby('minedGasPrice').mean()
priceWait.reset_index(inplace=True)
priceWait['delay'] = priceWait['delay'].apply(np.exp)
priceWait['delay'] = priceWait['delay']*blockInterval/float(60)


print(priceWait)

#define gas predictors
print (gpRecs)

dep = pd.DataFrame()

if (gpRecs['safeLow'] < gpRecs['Average']):
    dep['priceCat1'] = ((txData2['minedGasPrice']== gpRecs['safeLow'])).astype(int)
dep['priceCat2'] = (txData2['minedGasPrice'] == gpRecs['Average']).astype(int)
#dep['priceCat3'] = ((txData2['minedGasPrice'] > gpRecs['Average']) & (txData2['minedGasPrice'] < gpRecs['Fastest'])).astype(int)
dep['priceCat4'] = (txData2['minedGasPrice'] >= gpRecs['Fastest']).astype(int)

# Define gasused cats

quantiles= txData2['gasused'].quantile([.5, .75, .9, 1])

#dep['gasCat1'] = (txData2['gasused'] == 21000).astype(int)
dep['gasCat2'] = ((txData2['gasused']>21000) & (txData2['gasused']<=quantiles[.75])).astype(int)
dep['gasCat3'] = ((txData2['gasused']>quantiles[.75]) & (txData2['gasused']<=quantiles[.9])).astype(int)
dep['gasCat4'] = (txData2['gasused']> quantiles[.9]).astype(int)

dep['cons'] = 1

txData2['logDelay'] = txData2['delay'].apply(np.log)
indep = txData2['logDelay'].apply(np.round(decimals=3))

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#   print(indep)
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#    print(dep)


model = sm.OLS(indep, dep)

results = model.fit(disp=0)
dictResults = dict(results.params)
print (results.summary())
print (gpRecs)

dddd

if not 'priceCat1' in dictResults:
    dictResults['priceCat1'] = dictResults['priceCat2']


print(dictResults)
#check to see if really fastest
predictAverage = dictResults['cons']
predictFastest = dictResults['cons'] + dictResults['priceCat4']

if (predictFastest >= predictAverage):
    gpRecs['Fastest'] = gpRecs['Average']

#safeLow cannot be zero and must have 50 transactions mined at or below price over last 10,000 blocks


quantiles = quantiles.reset_index(drop=True)
quantiles.rename({0: '50pct', 1: '75pct', 2: '90pct', 3: 'max'}, inplace=True)
quantiles = quantiles.to_dict()

dictResults.update(quantiles)
dictResults.update(blockTime)
priceTable = priceTable.to_json(orient = 'records')
priceWait = priceWait.to_json(orient = 'records')
miningTable = txDataMiner.to_json(orient = 'records')
topMinerTable = topMiners.to_json(orient = 'records')
gasGuzzTable = gasGuzz.to_json(orient = 'records')

parentdir = os.path.dirname(os.getcwd())
if not os.path.exists(parentdir + '/json'):
    os.mkdir(parentdir + '/json')
filepath_calc = parentdir + '/json/calc.json'
filepath_recs = parentdir + '/json/ethgasAPI.json'
filepath_pricetable = parentdir + '/json/price.json'
filepath_miners = parentdir + '/json/miners.json'
filepath_gasguzz = parentdir + '/json/gasguzz.json'
filepath_topMiners = parentdir + '/json/topMiners.json'
filepath_priceWait = parentdir + '/json/priceWait.json'

with open(filepath_calc, 'w') as outfile:
    json.dump(dictResults, outfile)

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





cnx.close()
