#analysis:  block 3930236 - 3935602:  340,057 total submitted transactions

import mysql.connector
import pandas as pd
import numpy as np 
import statsmodels.api as sm
import math
import sys
import os, subprocess, re
import urllib,json

try:
    url = "http://localhost/json/price.json"
    response = urllib.urlopen(url)
    hashPower = pd.read_json(response, orient='records')
    response.close()
except:
    print (error)

hashPower['adjustedMinP'] = hashPower['adjustedMinP'].apply(lambda x: x*1000)
hashPower = hashPower.set_index('adjustedMinP', drop=True)

print (hashPower)

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')

cursor = cnx.cursor()

# First Query to Determine Block TIme, and Estimate Miner Policies

gasLimit = 4710000
block = 3930236


batch = 100000
cursor.execute("SELECT txHash, block from txpool where id < %(batch)s ", {'batch':batch})
head = cursor.column_names
txpoolData = pd.DataFrame(cursor.fetchall())
txpoolData.columns = head

lastBlockinBatch = txpoolData['block'].max()
print(lastBlockinBatch)


cursor.execute("SELECT txHash, gasPrice, gasOffered, postedBlock from transactions where postedblock > 3920236 and postedblock < 3935603")
head = cursor.column_names
allPosted = pd.DataFrame(cursor.fetchall())
allPosted.columns = head

currentBlockTxPool = pd.DataFrame(txpoolData.loc[txpoolData['block']==block, 'txHash'])
currentBlockTxPool = currentBlockTxPool.merge(allPosted, how='inner', on='txHash')

currentBlockTxPoolSum = pd.DataFrame(currentBlockTxPool.groupby('gasPrice').sum())
currentBlockTxPoolSum['gasLimit'] = 4710000
currentBlockTxPoolSum['pctLimit'] = currentBlockTxPoolSum['gasOffered']/currentBlockTxPoolSum['gasLimit']
print(currentBlockTxPoolSum)

currentBlockTxPoolSumTx = pd.DataFrame(currentBlockTxPool.groupby('gasPrice').count())
print (currentBlockTxPoolSumTx)

blockTxs = pd.DataFrame(allPosted.loc[allPosted['postedBlock']==block]) 


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
    seriesTxAbove = currentBlockTxPoolSumTx.loc[currentBlockTxPoolSumTx.index > gasPrice, 'count']
    return (seriesTxAbove.sum())


blockTxs = blockTxs.sort_values('gasPrice')

for index,row in blockTxs.iterrows():
    blockTxs.loc[index, 'pctLimitGasAbove'] = getPctLimitGasAbove(row['gasPrice'])
    blockTxs.loc[index, 'pctLimitGasAt'] = getPctLimitGasAt(row['gasPrice'])
    blockTxs.loc[index, 'pctLimitGasBelow'] = getPctLimitGasBelow(row['gasPrice'])
    blockTxs.loc[index, 'hashPowerAccepting'] = getHashPowerAccepting(row['gasPrice'])
    


print(blockTxs)











