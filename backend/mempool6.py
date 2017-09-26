"""Reports on mempool wait times and miner gas mined on last block and votes on gas limit"""

import sys
import json
import urllib
import pandas as pd
import numpy as np
import mysql.connector
from sqlalchemy import create_engine

endBlock = int(sys.argv[1])

def round_gasprice(gasPrice):
    """Rounds the gas price to Gwei, allows 10ths"""
    gasPrice = gasPrice/100
    if gasPrice >=1 and gasPrice<10:
        gasPrice = np.floor(gasPrice)
    elif gasPrice>=10 and gasPrice<1000:
        gasPrice=gasPrice/10
        gasPrice=np.floor(gasPrice)
        gasPrice=gasPrice*10
    elif gasPrice > 1000:
        gasPrice = 1000
    else:
        gasPrice = 0
   
    return gasPrice

def get_hpa(gasPrice):
    """gets the hash power accpeting the gas price over last 200 blocks"""
    hpa = txDataHashP.loc[gasPrice >= txDataHashP.index, 'hashpPct']
    if gasPrice > txDataHashP.index.max():
        hpa = 100
    elif gasPrice < txDataHashP.index.min():
        hpa = 0
    else:
        hpa = hpa.max()
    return hpa

def txAtAbove(gasPrice):
    """gets the number of transactions in the txpool at or above the given gasprice"""
    txAtAb = memPoolbyGP.loc[memPoolbyGP.index >= gasPrice, 'txHash']
    if gasPrice > memPoolbyGP.index.max():
        txAtAb = 0
    else:
        txAtAb = txAtAb.sum()
    return txAtAb



#Load datasets

engine = create_engine(
    'mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)

try:
    url = "http://localhost/json/ethgas.json"
    response = urllib.urlopen(url)
    calc = json.load(response)
    response.close()
except:
    print ('error')

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

#load txpool list at call block
cursor.execute("SELECT txHash FROM txpool2 WHERE block = %s" % endBlock)
head = cursor.column_names
txpool = pd.DataFrame(cursor.fetchall())
txpool.columns = head
txpoolList = txpool['txHash'].values.astype(str)
txpoolList2 = txpoolList.tolist()
txHashString = ','.join("'" + item + "'" for item in txpoolList2)

#load all transactions in the txpool or in current block
query = "SELECT txHash, gasPrice, toAddress, fromAddress, gasOffered, postedBlock, tsPosted from transactions where (txHash IN (%s)) OR (postedBlock = %s)" % (txHashString, endBlock)
cursor.execute(query)
head = cursor.column_names
memPoolTx = pd.DataFrame(cursor.fetchall())
memPoolTx.columns = head
memPoolTx['gasPrice'] = memPoolTx['gasPrice'].apply(round_gasprice)

#load the block data to estimate hash power accepting
cursor.execute("SELECT blockNum, minGasPrice, speed FROM speedo2 WHERE main = 1 order by ID desc limit 200")
head = cursor.column_names
gpData = pd.DataFrame(cursor.fetchall())
gpData.columns = head
gpData['minGasPrice'] = gpData['minGasPrice'].apply(round_gasprice)

#create the hash power accepting data frame and calculate hpa
txDataHashP = gpData[['blockNum', 'minGasPrice']].groupby('minGasPrice').count()
txDataHashP = txDataHashP.rename(columns={'blockNum': 'count'})
txDataHashP['cumBlocks'] = txDataHashP['count'].cumsum()
totalBlocks2 = txDataHashP['count'].sum()
txDataHashP['hashpPct'] = txDataHashP['cumBlocks']/totalBlocks2*100
print(txDataHashP)

#create groupby object from all transactions: gasprice
memPoolbyGP = memPoolTx[['txHash', 'gasPrice']].groupby('gasPrice').count()

#create predict table to speed lookups
n=100
k=10
predictTable = pd.DataFrame({'gasPrice' :  range(10, 1010, 10)})
ptable2 = pd.DataFrame({'gasPrice' : range(0, 10, 1)})
predictTable = predictTable.append(ptable2).reset_index(drop=True)
predictTable = predictTable.sort_values('gasPrice').reset_index(drop=True)
predictTable['hashPowerAccepting'] = predictTable['gasPrice'].apply(get_hpa)
predictTable['txAtAbove'] = predictTable['gasPrice'].apply(txAtAbove)
print (predictTable)

gpLookup = predictTable.set_index('gasPrice')['hashPowerAccepting'].to_dict()
txAtAboveLookup = predictTable.set_index('gasPrice')['txAtAbove'].to_dict()
print (gpLookup)


#calculate the parameters for each transaction in the txpool
memPoolTx['waitBlocks'] = memPoolTx['postedBlock'].apply(lambda x: endBlock-x)
memPoolTx['pctLimit'] = memPoolTx['gasOffered'].apply(lambda x: x/ calc['gasLimit'])
memPoolTx['hashPowerAccepting'] = memPoolTx['gasPrice'].apply(lambda x: gpLookup[x])
memPoolTx['numFrom'] = memPoolTx.groupby('fromAddress')['txHash'].transform('count')
memPoolTx['numTo'] = memPoolTx.groupby('toAddress')['txHash'].transform('count')
memPoolTx['txAtAbove'] = memPoolTx['gasPrice'].apply(lambda x: txAtAboveLookup[x])
memPoolTx['blockss'] = endBlock

#now write the block data
with pd.option_context('display.max_rows', 50, 'display.max_columns', None,):
    print(memPoolTx.sort_values('gasPrice'))

memPoolTx.to_sql(con=engine, name = 'blockSnapshot', if_exists='replace', index=False)


