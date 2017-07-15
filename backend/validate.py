import mysql.connector, sys, os
import pandas as pd
import numpy as np
import subprocess, json
import os, subprocess, re
import urllib
import math
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)


startBlock = int(sys.argv[1])
endBlock = int(sys.argv[2])

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

query = ("SELECT transactions.txHash, minedtransactions.minedBlock, transactions.postedBlock, transactions.gasOffered, transactions.gasPrice FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > %s AND transactions.postedBlock < %s")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names
txData = pd.DataFrame(cursor.fetchall())
txData.columns = head

txData['gasPrice'] = txData['gasPrice'].apply(lambda x: x/float(1000))
txData['gasPrice'] = txData['gasPrice'].apply(lambda x: np.round(x, decimals=0) if x >=1 else np.round(x, decimals=1))
txData['actual'] = txData['minedBlock'] - txData['postedBlock']

query2 = ("SELECT gasPrice, expectedWait, expectedWaitC, endBlock from validate WHERE endBlock > %s AND endBlock < %s")

cursor.execute(query2, (startBlock, endBlock))
head = cursor.column_names
predictions = pd.DataFrame(cursor.fetchall())
predictions.columns = head
cursor.close()

blockList = predictions['endBlock'].tolist()

def getPredcition(gasPrice, gasOffered, block):
    if block in blockList:
        txWait = predictions.loc[(predictions['gasPrice']==gasPrice) & (predictions['endBlock']==block), 'expectedWait'].values[0]
        conWait = predictions.loc[(predictions['gasPrice']==gasPrice) & (predictions['endBlock']==block), 'expectedWaitC'].values[0]
        if gasOffered > 21000:
            return conWait
        else:
            return txWait
    else:
        return np.nan

print(txData)
print(predictions)


count = 100
countUp = 0

for index,row in txData.iterrows():
    if row['gasPrice']>100:
        row['gasPrice'] = 100
    print(countUp, row['txHash'])
    txData.loc[index, 'predictions'] = getPredcition(row['gasPrice'], row['gasOffered'], row['postedBlock'])
    count = count - 1
    countUp = countUp + 1
    if (count == 0):
        countFrom = countUp - 100
        countTo = countUp - 1
        predict1 = txData.loc[countFrom:countTo, ['predictions', 'actual', 'txHash', 'gasPrice', 'gasOffered', 'postedBlock']]
        print(len(predict1))
        predict1.to_sql(con=engine, name = 'validationData', if_exists='append', index=False)
        count = 100
    
    

predict1 = txData.loc[countFrom:, ['predictions', 'actual', 'txHash', 'gasPrice', 'gasOffered', 'postedBlock']]
predict1.to_sql(con=engine, name = 'validationData', if_exists='append', index=False)



