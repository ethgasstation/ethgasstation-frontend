import mysql.connector
import pandas as pd
import numpy as np
import statsmodels.api as sm

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

# First Query to Determine Block TIme, and Estimate Miner Policies
query = ("SELECT * FROM speedo where speedo.blockNum>=3705683")

cursor.execute(query)
head = cursor.column_names

minerData = pd.DataFrame(cursor.fetchall())
minerData.columns = head
cursor.close()

print (minerData)

# Find Block Totals Excluding Uncles

mainBlocks = minerData.loc[minerData['uncle']==0]

minerBlocks = mainBlocks.groupby('miner').sum()

print (minerBlocks)

minerBlocks = minerBlocks.drop(['id', 'blockNum', 'gasLimit', 'includedBlockNum', 'speed', 'avgWait'], axis=1)

# generates following aggregates by miner:  total mainblocks, total gasUsed in mainBlocks, total uncleInlcusions, 

print (minerBlocks)

# Find Uncle Stats

uncleBlocks = minerData.loc[minerData['uncle']==1]
uncleBlocks['awards']= 5*((uncleBlocks['includedBlockNum'] - uncleBlocks['blockNum'])/8) 
minerUncleBlocks = uncleBlocks.groupby('miner').sum()
minerUncleBlocks = minerUncleBlocks.drop(['id', 'blockNum', 'gasLimit', 'speed', 'averageTx', 'numUncs', 'numTx'], axis=1)

print (minerUncleBlocks)

# now we have following uncle aggregates by miner:  total uncles, total gasUsed in uncleBlocks, uncleAwards



