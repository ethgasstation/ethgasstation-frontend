#Reports on mempool wait times and miner gas mined on last block and votes on gas limit

import mysql.connector, sys, os
import pandas as pd
import numpy as np
import subprocess, json
import os, subprocess, re
import urllib
import math
from sqlalchemy import create_engine

endBlock = int(sys.argv[1])
callTime = int(sys.argv[2])

engine = create_engine('mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)


dictMiner = {
    '0xea674fdde714fd979de3edf0f56aa9716b898ec8':'Ethermine',
    '0x1e9939daaad6924ad004c2560e90804164900341':'ethfans',
    '0xb2930b35844a230f00e51431acae96fe543a0347':'miningpoolhub',
    '0x4bb96091ee9d802ed039c4d1a5f6216f90f81b01':'Ethpool',
    '0x52bc44d5378309ee2abf1539bf71de1b7d7be3b5':'Nanopool',
    '0x2a65aca4d5fc5b5c859090a6c34d164135398226':'Dwarfpool',
    '0x829bd824b016326a401d083b33d092293333a830':'f2pool',
    '0xa42af2c70d316684e57aefcc6e393fecb1c7e84e':'Coinotron',
    '0x6c7f03ddfdd8a37ca267c88630a4fee958591de0':'alpereum'

}

try:
    url = "http://localhost/json/price3.json"
    response = urllib.urlopen(url)
    hashPower = pd.read_json(response, orient='records')
    response.close()
except:
    print ('error')
hashPower['hashpPct'] = hashPower['hashpPct'].round().astype(int)
hashPower['gasPrice'] = hashPower['gasPrice'].apply(lambda x: x /float(1000))
hashPower = hashPower.set_index('gasPrice', drop=True)
print(hashPower)

try:
    url = "http://localhost/json/ethgas.json"
    response = urllib.urlopen(url)
    calc = json.load(response)
    response.close()
except:
    print ('error')


#load mempool and most recent block transactions

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

cursor.execute("SELECT txHash FROM txpool2 WHERE block = %s" % endBlock)
head = cursor.column_names
txpool = pd.DataFrame(cursor.fetchall())
txpool.columns = head
txpoolList = txpool['txHash'].values.astype(str)
txpoolList2 = txpoolList.tolist()

query = "SELECT txHash, gasPrice, gasOffered, postedBlock, tsPosted from transactions where txHash IN (%s)" % ','.join("'" + item + "'" for item in txpoolList2)
cursor.execute(query)
head = cursor.column_names
memPoolTx = pd.DataFrame(cursor.fetchall())
memPoolTx.columns = head
memPoolTx['tx'] = 1
memPoolTx['gasPrice'] = memPoolTx['gasPrice'].apply(lambda x: x/float(1000))
memPoolTx['gasPrice'] = memPoolTx['gasPrice'].apply(lambda x: np.round(x, decimals=0) if x >=1 else np.round(x, decimals=3))
memPoolTx['waitBlocks'] = memPoolTx['postedBlock'].apply(lambda x: endBlock-x)
memPoolTx['waitTime'] = memPoolTx['tsPosted'].apply(lambda x: callTime-x)
memPoolTx['pctLimit'] = memPoolTx['gasOffered'].apply(lambda x: x/ calc['gasLimit'])
memPoolTx['gasOffered'] = memPoolTx['gasOffered'].apply(lambda x: x/1e6)

#pd.options.display.max_colwidth=100
#print(memPoolTx.loc[memPoolTx['gasPrice']==0.6, :])


memPool = memPoolTx.groupby('gasPrice').sum().reset_index()

memPool = memPool.drop(['postedBlock', 'tsPosted', 'waitBlocks', 'waitTime'], axis=1)
memPool['gasOffered'] = memPool['gasOffered'].apply(lambda x: np.round(x, decimals=2))

memPoolAvg = memPoolTx.groupby('gasPrice').median().reset_index()
memPoolAvg = memPoolAvg.drop(['postedBlock', 'tsPosted', 'gasOffered', 'gasPrice', 'tx', 'pctLimit'], axis=1)
#memPoolAvg['waitTime'] = memPoolAvg['waitTime'].apply(lambda x: np.round(x, decimals=0))
#memPoolAvg['waitBlocks'] = memPoolAvg['waitBlocks'].apply(lambda x: np.round(x, decimals=2))

memPool = pd.concat([memPool, memPoolAvg], axis = 1)
memPool = memPool.fillna(value=0)

print (memPool)

n=100
k=10
predictTable = pd.DataFrame({'gasPrice' :  range(1, n+1, 1)})
ptable2 = pd.DataFrame({'gasPrice' : [0, .1, .2, .3, .4 , .5, .6, .7, .8 , .9]})
predictTable = predictTable.append(ptable2).reset_index(drop=True)
predictTable = predictTable.sort_values('gasPrice').reset_index(drop=True)



def getHashPowerAccepting (gasPrice):
    lower = hashPower.loc[hashPower.index <= gasPrice, 'hashpPct']
    return (lower.max())

def txAbove (gasPrice):
    seriesTxAbove = memPool.loc[memPool['gasPrice'] > gasPrice, 'tx']
    return (seriesTxAbove.sum())

def txAt (gasPrice):
    seriesTxAt = memPool.loc[memPool['gasPrice'] == gasPrice, 'tx']
    return (seriesTxAt.sum())

def getPctLimitGasAbove (gasPrice):
    seriesGasAbove = memPool.loc[memPool['gasPrice'] > gasPrice, 'pctLimit']
    return (seriesGasAbove.sum())

def getPctLimitGasAt (gasPrice):
    seriesGasAt = memPool.loc[memPool['gasPrice'] == gasPrice, 'pctLimit']
    return (seriesGasAt.sum())


for index, row in predictTable.iterrows():
    predictTable.loc[index, 'hashPowerAccepting'] = getHashPowerAccepting(row['gasPrice'])
    predictTable.loc[index, 'txAbove'] = txAbove(row['gasPrice'])
    predictTable.loc[index, 'txAt'] = txAt(row['gasPrice'])
    predictTable.loc[index, 'pctLimitGasAbove'] = getPctLimitGasAbove(row['gasPrice'])
    predictTable.loc[index, 'pctLimitGasAt'] = getPctLimitGasAt(row['gasPrice'])

totalTxTxP = memPool['tx'].sum()
predictTable['congestedCont'] = totalTxTxP/float(calc['gasLimit'])
predictTable['congestedcontXtxabove'] = predictTable['congestedCont']*predictTable['txAbove']
predictTable['txAtAbove'] = predictTable['txAt'] + predictTable['txAbove']
predictTable['transfer']=1

#model Parameters

#predictTable['intercept'] = 2.1152
#predictTable['hashPowerCoef'] = -0.0124
#predictTable['tfercoef'] = -.4628
#predictTable['pctLimitGasAboveCoeff'] = .0189
#predictTable['pctLimitGasAtCoeff'] = .0181
#predictTable['totalTxCoeff'] = .00009466

#predictTable['intercept'] = 4.2062
#predictTable['hashPowerCoef'] = -0.0298
#predictTable['tfercoef'] = -1.1295
#predictTable['pctLimitGasAboveCoeff'] = .0133
#predictTable['pctLimitGasAtCoeff'] = .0291
#predictTable['totalTxCoeff'] = .0002

predictTable['intercept'] = .9471
predictTable['gp1'] = 1.9277
predictTable['gp2'] = 1.3221
predictTable['gp3'] = .5899
predictTable['gp4'] = 0.2544
predictTable['txAtAboveCoef']= 0.0005 
predictTable['numFrom'] = 0


#predictTable['totalTxVal'] = predictTable['totalTxCoeff'].apply(lambda x: x * totalTxTxP)

predictTable['gp1'] = predictTable['intercept'] + predictTable['gp1'] + (predictTable['txAtAbove']*predictTable['txAtAboveCoef'])
predictTable['gp2'] = predictTable['intercept'] + predictTable['gp2'] + (predictTable['txAtAbove']*predictTable['txAtAboveCoef'])
predictTable['gp3'] = predictTable['intercept'] + predictTable['gp3'] + (predictTable['txAtAbove']*predictTable['txAtAboveCoef'])
predictTable['gp4'] = predictTable['intercept'] + predictTable['gp4'] + (predictTable['txAtAbove']*predictTable['txAtAboveCoef'])
predictTable['gp5'] = predictTable['intercept'] + (predictTable['txAtAbove']*predictTable['txAtAboveCoef'])

predictTable['sum'] = 0
for index, row in predictTable.iterrows():
    if row['gasPrice']<.5:
        predictTable.loc[index,'sum'] = row['gp1']
    elif row['gasPrice']>=.5 and row['gasPrice']<1:
        predictTable.loc[index, 'sum'] = row['gp2']
    elif row['gasPrice']>=1 and row['gasPrice']<4:
        predictTable.loc[index, 'sum'] = row['gp3']
    elif row['gasPrice']>=4 and row['gasPrice']<23:
        predictTable.loc[index, 'sum'] = row['gp4']
    else:
        predictTable.loc[index, 'sum'] = row['gp5']

print(predictTable)


predictTable['expectedWait'] = predictTable['sum'].apply(lambda x: np.exp(x))
predictTable['expectedWait'] = predictTable['expectedWait'].apply(lambda x: 2 if (x < 2) else x)
predictTable['expectedTime'] = predictTable['expectedWait'].apply(lambda x: x * calc['blockInterval']/60)

predictTable['expectedWaitC'] = predictTable['sum'].apply(lambda x: np.exp(x))
predictTable['expectedWaitC'] = predictTable['expectedWait'].apply(lambda x: 2 if (x < 2) else x)
predictTable['expectedTimeC'] = predictTable['expectedWait'].apply(lambda x: x * calc['blockInterval']/60)

predictTable['endBlock'] = endBlock

#uncomment to create validation data
#predictTable.to_sql(con=engine, name = 'validate', if_exists='append', index=False)

print(predictTable)

def getSafeLow():
    series = predictTable.loc[predictTable['expectedTime'] <= 20, 'gasPrice']
    safeLow = series.min()
    minHashList = hashPower[hashPower['hashpPct']>2].index
    #series2 = memPool.loc[memPool['waitBlocks'] <=45, 'gasPrice']
    #safe = series2.min()
    #print ('safe ')
    #print (safe)
    #print(minHashList)
    if (safeLow < minHashList.min()):
        safeLow = minHashList.min()
    print('calc min low')
    print(calc['minLow'])
    if (safeLow < calc['minLow']):
        safeLow = calc['minLow']
    return (math.ceil(safeLow*100)/100)

def getAverage():
    series = predictTable.loc[predictTable['expectedTime'] <= 5, 'gasPrice']
    average = series.min()
    minHashList = hashPower[hashPower['hashpPct']>=35].index
    if (average < minHashList.min()):
        average= minHashList.min()
    return (math.ceil(average*100)/100)

def getFastest():
    series = predictTable.loc[predictTable['expectedTime'] <= 2, 'gasPrice']
    fastest = series.min()
    series2 = predictTable.loc[predictTable['gasPrice']==23, 'expectedTime'].values[0]
    if (fastest < series2):
        fastest= 23
    if np.isnan(fastest):
        fastest = 100
    return (math.ceil(fastest*100)/100)

def getWait(gasPrice):
    if gasPrice<1:
        gasPrice = np.round(gasPrice, 1)
    else:
        gasPrice = np.round(gasPrice, 0)
    if gasPrice < .1:
        gasPrice = .1
    wait = round(predictTable.loc[predictTable['gasPrice'] == gasPrice, 'expectedTime'].values[0], 1)
    return wait

def getConWait(gasPrice):
    if gasPrice<1:
        gasPrice = np.round(gasPrice, 1)
    else:
        gasPrice = np.round(gasPrice, 0)
    if gasPrice < .1:
        gasPrice = .1
    wait = round(predictTable.loc[predictTable['gasPrice'] == gasPrice, 'expectedTimeC'].values[0], 1)
    return wait

calc2 = {}
calc2['safeLow'] = getSafeLow()
calc2['safeLowWait'] = getWait(calc2['safeLow'])
calc2['average'] = getAverage()
calc2['avgWait'] = getWait(calc2['average'])
calc2['fastest'] = getFastest()
calc2['fastWait'] = getWait(calc2['fastest'])
calc2['safeLowWaitC'] = getConWait(calc2['safeLow'])
calc2['avgWaitC'] = getConWait(calc2['average'])
calc2['fastWaitC'] = getConWait(calc2['fastest'])
calc2['blockNum'] = endBlock
print(calc2)


memPoolTable = memPool.to_json(orient = 'records')
parentdir = os.path.dirname(os.getcwd())
if not os.path.exists(parentdir + '/json'):
    os.mkdir(parentdir + '/json')
filepath_gpRecs2 = parentdir + '/json/ethgasAPI.json'
filepath_memPool = parentdir + '/json/memPool.json'


with open(filepath_gpRecs2, 'w') as outfile:
    json.dump(calc2, outfile)

with open(filepath_memPool, 'w') as outfile:
    outfile.write(memPoolTable)

