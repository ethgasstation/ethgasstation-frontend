#analysis:  block 3975317 - 3980356:  276,618 total submitted transactions
#avgGasLimit = 6704158
import mysql.connector
import pandas as pd
import numpy as np 
import statsmodels.api as sm
import math
import sys
import os, subprocess, re
import urllib,json
from sqlalchemy import create_engine


# analysis constants
#setTheseBased on Dataset
analyzeBlock = {
    'start' : 3975317,
    'end' : 3980367
}

lenTxPool = 1444975

engine = create_engine('mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)
cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

predictDataSet = pd.DataFrame()
remainder = pd.DataFrame()

cycles = (lenTxPool/100000) + 1
print ('cycles = '+ str(cycles))

# functions to define new predcitors for each posted transaction

def getPctLimitGasAbove (gasPrice):
    seriesGasAbove = currentBlockTxPoolSum.loc[currentBlockTxPoolSum.index > gasPrice, 'pctLimit']
    return (seriesGasAbove.sum())

def getPctLimitGasAt (gasPrice):
    seriesGasAt = currentBlockTxPoolSum.loc[currentBlockTxPoolSum.index == gasPrice, 'pctLimit']
    return (seriesGasAt.sum())

def getPctLimitGasBelow (gasPrice):
    seriesGasBelow = currentBlockTxPoolSum.loc[currentBlockTxPoolSum.index < gasPrice, 'pctLimit']
    return (seriesGasBelow.sum())

def getHashPowerAccepting (gasPrice):
    lower = hashPower.loc[hashPower.index <= gasPrice, 'cumPctTotBlocks']
    return (lower.max())

def totalTxinTxP ():
    return (len(currentBlockTxPool))

def totalGasTxP():
    return(currentBlockTxPoolSum['gasOffered'].sum())

def txAbove (gasPrice):
    seriesTxAbove = currentBlockTxPoolSumTx.loc[currentBlockTxPoolSumTx.index > gasPrice, 'txHash']
    return (seriesTxAbove.sum())

def txAt (gasPrice):
    seriesTxAt = currentBlockTxPoolSumTx.loc[currentBlockTxPoolSumTx.index == gasPrice, 'txHash']
    return (seriesTxAt.sum())

def txBelow (gasPrice):
    seriesTxBelow = currentBlockTxPoolSumTx.loc[currentBlockTxPoolSumTx.index < gasPrice, 'txHash']
    return (seriesTxBelow.sum())

#Load Hash Power table- should be current for analysis set

try:
    url = "http://localhost/json/price2.json"
    response = urllib.urlopen(url)
    hashPower = pd.read_json(response, orient='records')
    response.close()
except:
    print ('error')

hashPower['adjustedMinP'] = hashPower['adjustedMinP'].apply(lambda x: x*1000)
hashPower = hashPower.set_index('adjustedMinP', drop=True)
print (hashPower)


#get all posted transactions in MySql start 10,000 blocks prior to analysis

cursor.execute("SELECT txHash, gasPrice, gasOffered, postedBlock from transactions where postedblock >= %(start)s and postedblock <= %(end)s", analyzeBlock)
head = cursor.column_names
allPosted = pd.DataFrame(cursor.fetchall())
allPosted.columns = head

cursor.execute("SELECT blockNum, gasLimit from speedo2 where blockNum >= %(start)s and blockNum <= %(end)s", analyzeBlock)
head = cursor.column_names
blockInfo = pd.DataFrame(cursor.fetchall())
blockInfo.columns = head
gasLimitAvg = blockInfo['gasLimit'].mean()

#loop to iterate through txpool- need to calculate based on length of txpool table

batch = {
    'batchStart' : 1,
    'batchEnd' : 100000 
}

blockStart = analyzeBlock['start']
for batchloop in range(1, cycles):
    cursor.execute("SELECT id, txHash, block from txpool where id >= %(batchStart)s AND id < %(batchEnd)s ", batch)
    head = cursor.column_names
    txpoolData = pd.DataFrame(cursor.fetchall())
    txpoolData.columns = head
    print(len(txpoolData))
    txpoolData = txpoolData.append(remainder).sort_values('block')
    print(len(txpoolData))

    blockEnd = (txpoolData['block'].max()-1)
    tailId = txpoolData.loc[txpoolData['block']==blockEnd, 'id'].max()
    print(blockStart) 
    print (blockEnd)

    for block in range(blockStart, blockEnd):
        #Define a dataframe with a txpool for one block
        currentBlockTxPool = pd.DataFrame(txpoolData.loc[txpoolData['block']==block, 'txHash'])
        currentBlockTxPool = currentBlockTxPool.merge(allPosted, how='inner', on='txHash')

        #get all gas offered by gas price in Block's txpool
        currentBlockTxPoolSum = pd.DataFrame(currentBlockTxPool.groupby('gasPrice').sum())
        
        currentBlockTxPoolSum['gasLimit'] = gasLimitAvg
        currentBlockTxPoolSum['pctLimit'] = currentBlockTxPoolSum['gasOffered']/currentBlockTxPoolSum['gasLimit']

        #get num tx by gas price in Block's txpool
        currentBlockTxPoolSumTx = pd.DataFrame(currentBlockTxPool.groupby('gasPrice').count())

        #Define dataframe with all the posted transactions for the block then iterate through the block to define new predictors for each transaction

        blockTxs = pd.DataFrame(allPosted.loc[allPosted['postedBlock']==block])
        blockTxs = blockTxs.reset_index(drop=True) 
        blockTxs = blockTxs.sort_values('gasPrice')
        blockTxs['gasOfferedPct'] = blockTxs['gasOffered'].apply(lambda x: x/gasLimitAvg)

        for index,row in blockTxs.iterrows():
            blockTxs.loc[index, 'pctLimitGasAbove'] = getPctLimitGasAbove(row['gasPrice'])
            blockTxs.loc[index, 'pctLimitGasAt'] = getPctLimitGasAt(row['gasPrice'])
            blockTxs.loc[index, 'pctLimitGasBelow'] = getPctLimitGasBelow(row['gasPrice'])
            blockTxs.loc[index, 'hashPowerAccepting'] = getHashPowerAccepting(row['gasPrice'])
            blockTxs.loc[index, 'totalTxTxP'] = totalTxinTxP()
            blockTxs.loc[index, 'totalGasTxP'] = totalGasTxP()
            blockTxs.loc[index, 'txAbove'] = txAbove(row['gasPrice'])
            blockTxs.loc[index, 'txAt'] = txAt(row['gasPrice'])
            blockTxs.loc[index, 'txBelow'] = txBelow(row['gasPrice'])

        print(len(blockTxs))
        predictDataSet= predictDataSet.append(blockTxs)
        print(block)
    remainder = pd.DataFrame(txpoolData.loc[txpoolData['id'] > tailId,:])
    batch['batchStart'] = batch['batchStart'] + 100000
    batch['batchEnd'] = batch['batchEnd'] + 100000
    blockStart = blockEnd
    print('remainder ' + str(len(remainder)))
    predictDataSet.to_sql(con=engine, name = 'prediction2', if_exists='append', index=False)
    predictDataSet = pd.DataFrame()



predictDataSet = predictDataSet.reset_index(drop=True)
print(predictDataSet)















