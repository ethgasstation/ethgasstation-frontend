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


# Create uncle dataframe to summarize uncle stats
uncleBlocks = pd.DataFrame(minerData.loc[minerData['uncle'] == 1]) 
uncleBlocks['incDelay']= uncleBlocks['includedBlockNum'] - uncleBlocks['blockNum']
uncleBlocks['uncleAwards'] = uncleBlocks['incDelay']/8 * 5
minerUncleBlocks = uncleBlocks.groupby('miner').sum()
minerUncleBlocks = minerUncleBlocks.drop(['id', 'blockNum', 'gasLimit', 'numUncs', 'numTx', 'main', 'includedBlockNum', 'incDelay'], axis=1)
minerUncleBlocks = minerUncleBlocks.rename(columns={'gasUsed': 'uncleGasUsed'})



# Create mainchain dataframe to summarize mined blocks
mainBlocks = pd.DataFrame(minerData.loc[minerData['uncle']==0])


# Clean blocks first reported as mainchain that later become uncles
mainBlocks['duplicates'] = mainBlocks.duplicated(subset='blockNum', keep = False)

def resolveDup(blockHash):
    match = (uncleBlocks['blockHash'] == blockHash).sum()
    if match > 0:
        return False
    else:
        return True 

for index, row in mainBlocks.iterrows():
    if row['duplicates'] == True:
        mainBlocks.loc[index, 'keep'] = resolveDup(row['blockHash'])

#drop the duplicate row from mainBlocks- it is actually an uncle
mainBlocks= mainBlocks[mainBlocks['keep'] == True]

#create summary table
minerBlocks = mainBlocks.groupby('miner').sum()
minerBlocks = minerBlocks.drop(['id', 'blockNum', 'gasLimit', 'includedBlockNum', 'uncle'], axis=1)

# Merge the two tables on miner
minerBlocks = minerBlocks.join(minerUncleBlocks)

print (minerBlocks)




