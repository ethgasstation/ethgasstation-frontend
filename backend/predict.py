#analysis:  block 3930236 - 3935602:  340,057 total submitted transactions

import mysql.connector
import pandas as pd
import numpy as np 
import statsmodels.api as sm
import math
import sys
import os, subprocess, re
import urllib,json


# analysis constants
predictDataSet = pd.DataFrame()
gasLimit = 4710000

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
    url = "http://localhost/json/price.json"
    response = urllib.urlopen(url)
    hashPower = pd.read_json(response, orient='records')
    response.close()
except:
    print ('error')

hashPower['adjustedMinP'] = hashPower['adjustedMinP'].apply(lambda x: x*1000)
hashPower = hashPower.set_index('adjustedMinP', drop=True)
print (hashPower)


#get all posted transactions in MySql start 10,000 blocks prior to analysis
cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()
cursor.execute("SELECT txHash, gasPrice, gasOffered, postedBlock from transactions where postedblock > 3920236 and postedblock < 3935603")
head = cursor.column_names
allPosted = pd.DataFrame(cursor.fetchall())
allPosted.columns = head


#loop to iterate through txpool- need to calculate based on length of txpool table
batchStart = 1
batchEnd = 100000
blockStart = 3930236
for batchloop in range(1, 1):
    cursor.execute("SELECT txHash, block from txpool where id >= %(batchStart) AND id < %(batchEnd)s ", {'batchStart':batchStart, 'batchEnd':batchEnd})
    head = cursor.column_names
    txpoolData = pd.DataFrame(cursor.fetchall())
    txpoolData.columns = head

    #blockEnd = (txpoolData['block'].max()-1)
    blockEnd = blockStart + 5
    print(blockStart) 
    print (blockEnd)

    for block in range(blockStart, blockEnd):
        #Define a dataframe with a txpool for one block
        currentBlockTxPool = pd.DataFrame(txpoolData.loc[txpoolData['block']==block, 'txHash'])
        currentBlockTxPool = currentBlockTxPool.merge(allPosted, how='inner', on='txHash')

        #get all gas offered by gas price in Block's txpool
        currentBlockTxPoolSum = pd.DataFrame(currentBlockTxPool.groupby('gasPrice').sum())
        currentBlockTxPoolSum['gasLimit'] = 4710000
        currentBlockTxPoolSum['pctLimit'] = currentBlockTxPoolSum['gasOffered']/currentBlockTxPoolSum['gasLimit']
        print(currentBlockTxPoolSum)

        #get num tx by gas price in Block's txpool
        currentBlockTxPoolSumTx = pd.DataFrame(currentBlockTxPool.groupby('gasPrice').count())
        print (currentBlockTxPoolSumTx)

        #Define dataframe with all the posted transactions for the block then iterate through the block to define new predictors for each transaction

        blockTxs = pd.DataFrame(allPosted.loc[allPosted['postedBlock']==block])
        blockTxs = blockTxs.reset_index(drop=True) 
        blockTxs = blockTxs.sort_values('gasPrice')

        for index,row in blockTxs.iterrows():
            blockTxs.loc[index, 'pctLimitGasAbove'] = getPctLimitGasAbove(row['gasPrice'])
            blockTxs.loc[index, 'pctLimitGasAt'] = getPctLimitGasAt(row['gasPrice'])
            blockTxs.loc[index, 'pctLimitGasBelow'] = getPctLimitGasBelow(row['gasPrice'])
            blockTxs.loc[index, 'hashPowerAccepting'] = getHashPowerAccepting(row['gasPrice'])
            blockTxs.loc[index, 'totalTxTxP'] = totalTxinTxP()
            blockTxs.loc[index, 'txAbove'] = txAbove(row['gasPrice'])
            blockTxs.loc[index, 'txAt'] = txAt(row['gasPrice'])
            blockTxs.loc[index, 'txBelow'] = txBelow(row['gasPrice'])

        print(blockTxs)
        predictDataSet= predictDataSet.append(blockTxs)
        print(block)

print(predictDataSet)












