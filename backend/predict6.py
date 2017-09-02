#1) run- gascalcPredict2.py with start - 2000 blocks
#2) edit analyzeBlock (start, end) and len (txpool)
#3) edit dbname below


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
    'start' : 4225516,
    'end' : 4226707
}

lenTxPool = 11528896

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
    lower = hashPower.loc[hashPower.index <= gasPrice, 'hashpPct']
    return (lower.max())

def totalTxinTxP ():
    return (len(currentBlockTxPool))

def totalTxFee ():
    return (currentBlockTxPoolSumTx['totalFee'].sum())

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

def numTo (address):
    if not address:
        return np.nan 

    if address in currentBlockTxPoolSumTo.index:
        num = currentBlockTxPoolSumTo.loc[address, 'txHash']
    else:
        num = 0
    
    if address in blockTxsTo.index:
        num2 = blockTxsTo.loc[address, 'txHash']
    else:
        num2 = 0

    print (address)
    print ('num2')
    print (num2)
    print (num + num2)
    return (num + num2)

def numFrom (address):
    if not address:
        return np.nan

    if address in currentBlockTxPoolSumFrom.index:
        num = currentBlockTxPoolSumFrom.loc[address, 'txHash']
        print (address)  
    else:
        num = 0
    
    if address in blockTxsFrom.index:
        num2 = blockTxsFrom.loc[address, 'txHash']
    else:
        num2 = 0

    print ('num2')
    print (num2)
    print (num + num2)
    return (num + num2)

def validateTx (block, gasPrice, numFrom, numTo):
    gasPrice = gasPrice / 1000
    if gasPrice >=1:
        gasPrice = np.floor(gasPrice)
    else:
        gasPrice = gasPrice*10
        gasPrice = np.floor(gasPrice)
        gasPrice = gasPrice / float(10)
    if gasPrice > 100:
        gasPrice = 100
    print ('roundedGasPrice')
    print (gasPrice)
    print ('block')
    print (block)
    if block in validatePredict['endBlock'].values:
        dump = 1.1163
        ico = 1.489
        sum = validatePredict.loc[(validatePredict['gasPrice']==gasPrice) & (validatePredict['endBlock'] == block), 'sum'].values[0]
        if numFrom > 5:
            sum = sum + dump
        if numTo >=100:
            sum = sum + ico
        prediction = exp(sum)
        print (prediction)
        ddd
        return prediction
    else:
        return np.nan



#Load Hash Power table- should be current for analysis set

try:
    url = "http://localhost/json/price3.json"
    response = urllib.urlopen(url)
    hashPower = pd.read_json(response, orient='records')
    response.close()
except:
    print ('error')
hashPower['hashpPct'] = hashPower['hashpPct'].round().astype(int)
hashPower = hashPower.set_index('gasPrice', drop=True)
print (hashPower)

#get all posted transactions in MySql start 10,000 blocks prior to analysis

analyzeBlock['start'] = analyzeBlock['start'] - 10000

cursor.execute("SELECT txHash, gasPrice, gasOffered, postedBlock, toAddress, fromAddress from transactions where postedblock >= %(start)s and postedblock <= %(end)s", analyzeBlock)
head = cursor.column_names
allPosted = pd.DataFrame(cursor.fetchall())
allPosted.columns = head

analyzeBlock['start'] = analyzeBlock['start'] + 10000

cursor.execute("SELECT blockNum, gasLimit from speedo2 where blockNum >= %(start)s and blockNum <= %(end)s", analyzeBlock)
head = cursor.column_names
blockInfo = pd.DataFrame(cursor.fetchall())
blockInfo.columns = head
gasLimitAvg = blockInfo['gasLimit'].mean()

cursor.execute("SELECT endBlock, gasPrice, sum, expectedWait from validate")
head = cursor.column_names
validatePredict = pd.DataFrame(cursor.fetchall())
validatePredict.columns = head
validatePredict['gasPrice'] = validatePredict['gasPrice'].apply(lambda x: x*10000)

print (validatePredict)

#loop to iterate through txpool- need to calculate based on length of txpool table

batch = {
    'batchStart' : 1,
    'batchEnd' : 100000 
}

blockStart = analyzeBlock['start']
if cycles == 1:
    cycles = 2
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

        #define age of transactions in txpool
        currentBlockTxPool['blockAge'] = currentBlockTxPool['postedBlock'].apply(lambda x: block - x)
        currentBlockTxPool.loc[currentBlockTxPool['blockAge'] < 0, 'blockAge'] = np.nan
        #get all gas offered by gas price in Block's txpool
        currentBlockTxPoolSum = pd.DataFrame(currentBlockTxPool.groupby('gasPrice').sum())
        
        currentBlockTxPoolSum['gasLimit'] = gasLimitAvg
        currentBlockTxPoolSum['pctLimit'] = currentBlockTxPoolSum['gasOffered']/currentBlockTxPoolSum['gasLimit']
        

        print(currentBlockTxPoolSum)
        

        currentBlockTxPoolSumTo = pd.DataFrame(currentBlockTxPool.groupby('toAddress').count())

        #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(currentBlockTxPoolSumTo)

        currentBlockTxPoolSumFrom = pd.DataFrame(currentBlockTxPool.groupby('fromAddress').count())

        print(currentBlockTxPoolSumFrom)
        

        #get num tx by gas price in Block's txpool
        currentBlockTxPoolSumTx = pd.DataFrame(currentBlockTxPool.groupby('gasPrice').count())
        currentBlockTxPoolSumTx['totalFee'] = currentBlockTxPoolSumTx['txHash'] * currentBlockTxPoolSumTx.index

        print (currentBlockTxPoolSumTx)

        #get mean age of tx in txpool by gasprice /dont count tx offering more gas than gas limit
        currentBlockTxPool.loc[currentBlockTxPool['gasOffered'] > (gasLimitAvg/.95), 'blockAge'] = np.nan

        f = {'txHash':['count'], 'blockAge':['mean']}
        currentBlockTxPoolMeanTx = currentBlockTxPool.groupby('gasPrice').agg(f)
        currentBlockTxPoolMeanTx.columns = ['blockAge', 'txCount']
        print(currentBlockTxPool)
        print(currentBlockTxPoolMeanTx)
        

        #Define dataframe with all the posted transactions for the block then iterate through the block to define new predictors for each transaction

        blockTxs = pd.DataFrame(allPosted.loc[allPosted['postedBlock']==block])
        blockTxsTo = pd.DataFrame(blockTxs.groupby('toAddress').count())
        blockTxsFrom = pd.DataFrame(blockTxs.groupby('fromAddress').count())
        blockTxs = blockTxs.reset_index(drop=True) 
        blockTxs = blockTxs.sort_values('gasPrice')
        blockTxs['gasOfferedPct'] = blockTxs['gasOffered'].apply(lambda x: x/gasLimitAvg)

        

        for index,row in blockTxs.iterrows():
            blockTxs.loc[index, 'pctLimitGasAbove'] = getPctLimitGasAbove(row['gasPrice'])
            blockTxs.loc[index, 'pctLimitGasAt'] = getPctLimitGasAt(row['gasPrice'])
            blockTxs.loc[index, 'pctLimitGasBelow'] = getPctLimitGasBelow(row['gasPrice'])
            blockTxs.loc[index, 'hashPowerAccepting'] = getHashPowerAccepting(row['gasPrice'])
            blockTxs.loc[index, 'totalTxTxP'] = totalTxinTxP()
            blockTxs.loc[index, 'totalTxFee'] = totalTxFee()
            blockTxs.loc[index, 'totalGasTxP'] = totalGasTxP()
            blockTxs.loc[index, 'txAbove'] = txAbove(row['gasPrice'])
            blockTxs.loc[index, 'txAt'] = txAt(row['gasPrice'])
            blockTxs.loc[index, 'txBelow'] = txBelow(row['gasPrice'])
            numToTemp = numTo(row['toAddress'])
            numFromTemp = numFrom(row['fromAddress'])
            blockTxs.loc[index, 'numTo'] = numToTemp
            blockTxs.loc[index, 'numFrom'] = numFromTemp
            blockTxs.loc[index, 'prediction'] = validateTx(row['postedBlock'], row['gasPrice'], numToTemp, numFromTemp)
            
        print(len(blockTxs))
        predictDataSet= predictDataSet.append(blockTxs)
        print(block)
    remainder = pd.DataFrame(txpoolData.loc[txpoolData['id'] > tailId,:])
    batch['batchStart'] = batch['batchStart'] + 100000
    batch['batchEnd'] = batch['batchEnd'] + 100000
    blockStart = blockEnd
    print('remainder ' + str(len(remainder)))
    predictDataSet.to_sql(con=engine, name = 'prediction7', if_exists='append', index=False)
    predictDataSet = pd.DataFrame()



predictDataSet = predictDataSet.reset_index(drop=True)
print(predictDataSet)















