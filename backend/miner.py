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

query = ("SELECT * from minedtransactions where minedBlock >= %s and minedBlock < %s")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

txData = pd.DataFrame(cursor.fetchall())
txData.columns = head
cursor.close()

# Clean blocks first reported as mainchain that later become uncles
minerData['duplicates'] = minerData.duplicated(subset='blockNum', keep = False)
minerData['keep'] = True

def resolveDup(blockHash):
    match = minerData.loc[(minerData['blockHash'] == blockHash) & (minerData['uncle'] == True)]
    if len(match) > 0:
        return False
    else:
        return True 


for index, row in minerData.iterrows():
    if ((row['duplicates'] == True) & (row['main'] == True)):
        minerData.loc[index, 'keep'] = resolveDup(row['blockHash'])

#drop the duplicate row from mainBlocks- it is actually an uncle

minerData= minerData[minerData['keep'] == True]

# find empty block uncle rate

totemptyBlocks = len(minerData.loc[minerData['gasUsed']==0])
emptyUncles = len(minerData.loc[(minerData['gasUsed']==0) & (minerData['uncle']==True)])
emptyMains =  len(minerData.loc[(minerData['gasUsed']==0) & (minerData['main']==True)])

totTxBlocks = len(minerData.loc[minerData['gasUsed'] > 0])
txUncles = len(minerData.loc[(minerData['gasUsed'] > 0) & (minerData['uncle']==True)])
txMains =  len(minerData.loc[(minerData['gasUsed'] > 0) & (minerData['main']==True)])

emptyUnclePct = emptyUncles/float(totemptyBlocks)

print (totemptyBlocks, emptyUncles, emptyMains)
print (totTxBlocks, txUncles, txMains)
print ("%.3f" % (emptyUnclePct))

# Create uncle dataframe to summarize uncle stats
uncleBlocks = pd.DataFrame(minerData.loc[minerData['uncle'] == 1]) 
uncleBlocks['incDelay']= uncleBlocks['includedBlockNum'] - uncleBlocks['blockNum']
uncleBlocks['uncleAwards'] = uncleBlocks['incDelay']/8 * 5
minerUncleBlocks = uncleBlocks.groupby('miner').sum()
minerUncleBlocks = minerUncleBlocks.drop(['id', 'blockNum', 'gasLimit', 'uncsReported', 'numTx', 'main', 'duplicates', 'keep', 'includedBlockNum', 'incDelay'], axis=1)
minerUncleBlocks = minerUncleBlocks.rename(columns={'gasUsed': 'uncleGasUsed'})

# Create mainchain dataframe to summarize mined blocks
mainBlocks = pd.DataFrame(minerData.loc[minerData['uncle']==0])

#find total reward per block

def getRewardMain (uncsReported):
    reward = 5
    if uncsReported == 2:
        reward = reward + .3125
    elif uncsReported == 1:
        reward = reward + .15625
    return reward

for index,row in mainBlocks.iterrows():
    mainBlocks.loc[index, 'totRewardminusTxFees'] = getRewardMain(row['uncsReported'])

#create summary table
minerBlocks = mainBlocks.groupby('miner').sum()
minerBlocks = minerBlocks.drop(['id', 'blockNum', 'gasLimit', 'includedBlockNum', 'duplicates', 'keep', 'uncle'], axis=1)


# Merge the two tables on miner
minerBlocks = minerBlocks.join(minerUncleBlocks)
minerBlocks['uncleAwards'].fillna(0, inplace = True)
minerBlocks['uncle'].fillna(0, inplace = True)


#find txFees by Miner and merge

txData['fee'] = txData['gasused'] * txData['minedGasPrice']/1e9
txData = txData.groupby('miner').sum()
minerBlocks = minerBlocks.join(txData['fee'])

minerBlocks['totReward'] = minerBlocks['fee'] + minerBlocks['totRewardminusTxFees'] + minerBlocks['uncleAwards']

#calc Total Return
minerBlocks['totalBlocks'] = minerBlocks['main'] + minerBlocks['uncle']
minerBlocks['avgReward'] = minerBlocks['totReward'] / minerBlocks['totalBlocks']
minerBlocks['uncRatio'] = minerBlocks['uncle'] / minerBlocks['totalBlocks']
minerBlocks = minerBlocks.sort_values('avgReward')

print(minerBlocks)

# Regression model for gas
minerData['const'] = 1
minerData['gasUsedPerM'] = minerData['gasUsed']/1e6
model = sm.OLS(minerData['uncle'], minerData[['const','gasUsedPerM']])
results = model.fit()
print (results.summary())

miner1Data = minerData.loc[minerData['miner'] == '0xea674fdde714fd979de3edf0f56aa9716b898ec8', :]
model = sm.OLS(miner1Data['uncle'], miner1Data[['const','gasUsedPerM']])
results = model.fit()
print (results.summary())



