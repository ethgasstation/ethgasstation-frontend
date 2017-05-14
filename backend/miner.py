import mysql.connector, sys
import pandas as pd
import numpy as np
import statsmodels.api as sm

startBlock = sys.argv[1]
endBlock = sys.argv[2]

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

# First Query to Determine Block TIme, and Estimate Miner Policies
query = ("SELECT * FROM speedo where blockNum>= %s and blockNum < %s")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

minerData = pd.DataFrame(cursor.fetchall())
minerData.columns = head
cursor.close()

print (minerData)

# Find Block Totals Excluding Uncles

mainBlocks = minerData.loc[minerData['uncle']==0]

mainBlocks['duplicates'] = mainBlocks.duplicated(subset='blockNum', keep = 'first')

print(mainBlocks.loc[mainBlocks['duplicates']==True])

print(duplicates.sum())

minerBlocks = mainBlocks.groupby('miner').sum()
minerBlocks = minerBlocks.drop(['id', 'blockNum', 'gasLimit', 'includedBlockNum', 'uncle'], axis=1)

# generates following aggregates by miner:  total mainblocks, total gasUsed in mainBlocks, total uncleInlcusions, 

print (minerBlocks)

# Find Uncle Stats

uncleBlocks = minerData.loc[minerData['uncle']==1]
uncleBlocks['incDelay']= uncleBlocks['includedBlockNum'] - uncleBlocks['blockNum']
uncleBlocks['uncleAwards'] = uncleBlocks['incDelay']/8 * 5
minerUncleBlocks = uncleBlocks.groupby('miner').sum()
minerUncleBlocks = minerUncleBlocks.drop(['id', 'blockNum', 'gasLimit', 'numUncs', 'numTx', 'main', 'includedBlockNum', 'incDelay'], axis=1)

minerUncleBlocks = minerUncleBlocks.rename(columns={'gasUsed': 'uncleGasUsed'})

minerBlocks = minerBlocks.join(minerUncleBlocks)

print (minerBlocks)

# now we have following uncle aggregates by miner:  total uncles, total gasUsed in uncleBlocks, uncleAwards



