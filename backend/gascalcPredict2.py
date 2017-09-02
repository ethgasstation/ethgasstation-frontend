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


txData['txFee'] = txData['gasused']*txData['minedGasPrice']


#summary stats

totalTx = len(txData)
# Calculate Each Miners Mininum Price
# First Identify all Unique Miners in list

txDataMinP = pd.DataFrame(txData[['minedBlock', 'minedGasPrice']].groupby('minedBlock').min().reset_index())

txDataHashP = pd.DataFrame(txDataMinP.groupby('minedGasPrice').count().reset_index())

txDataHashP = txDataHashP.rename(columns={'minedGasPrice': 'minMinedGP', 'minedBlock': 'count'})
totalBlocks = txDataHashP['count'].sum()


print (txDataMinP)
print (txDataHashP)

n=100000
predictTable = pd.DataFrame({'gasPrice' :  range(1000, n+1000, 1000)})
ptable2 = pd.DataFrame({'gasPrice' : [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]})
predictTable = predictTable.append(ptable2).reset_index(drop=True)
predictTable = predictTable.sort_values('gasPrice').reset_index(drop=True)
predictTable['hashP'] = 0

for index, row in txDataHashP.iterrows():
    predictTable.loc[predictTable['gasPrice'] >= row['minMinedGP'], 'hashP'] = predictTable['hashP'].apply(lambda x: x+ row['count'])
    
predictTable['hashpPct'] = predictTable['hashP'].apply(lambda x: x/float(totalBlocks)*100)
print (predictTable)

predictTable= predictTable.to_json(orient = 'records')


parentdir = os.path.dirname(os.getcwd())
if not os.path.exists(parentdir + '/json'):
    os.mkdir(parentdir + '/json')

filepath_pricetable = parentdir + '/json/price3.json'

with open(filepath_pricetable, 'w') as outfile:
    outfile.write(predictTable)


cursor.close()
cnx.close()
