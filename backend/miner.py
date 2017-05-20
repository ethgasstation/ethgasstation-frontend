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
cnx.close()

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

#clean data

totalBlocks = len(minerData)
minerData['uncsReported'].fillna(value=0, inplace=True)
minerData.loc[minerData['uncle']==1, 'blockFee'] = 0
minerData = minerData.dropna(subset=['blockFee'])



minerData['blockFee'] = minerData['blockFee']/1e9

minerData.loc[minerData['uncsReported']==1, 'includeFee' ] = .15625
minerData.loc[minerData['uncsReported']==2, 'includeFee'] = .3125
minerData.loc[minerData['uncsReported']==0, 'includeFee'] = 0

minerData['blockAward'] = 5 + minerData['includeFee'] + minerData['blockFee']
minerData['blockAwardwoFee'] = 5 + minerData['includeFee']

#find average gas mined per block for each miner


# find empty block uncle rate

totemptyBlocks = len(minerData.loc[minerData['gasUsed']==0])
emptyUncles = len(minerData.loc[(minerData['gasUsed']==0) & (minerData['uncle']==True)])
emptyMains =  len(minerData.loc[(minerData['gasUsed']==0) & (minerData['main']==True)])
emptyUnclePct = emptyUncles/float(totemptyBlocks)

print (totemptyBlocks, emptyUncles, emptyMains)
print ("%.3f" % (emptyUnclePct))

# Create uncle dataframe to summarize uncle stats
uncleBlocks = pd.DataFrame(minerData.loc[minerData['uncle'] == 1]) 
uncleBlocks['incDelay']= uncleBlocks['includedBlockNum'] - uncleBlocks['blockNum']
uncleBlocks['uncleAward'] = (8-uncleBlocks['incDelay'])/8 * 5
avgUncleAward = uncleBlocks['uncleAward'].mean()

minerUncleBlocks = uncleBlocks.groupby('miner').sum()

#clean
minerUncleBlocks = minerUncleBlocks.drop(['id', 'blockNum', 'gasLimit', 'uncsReported', 'numTx', 'main', 'duplicates', 'keep', 'includedBlockNum', 'incDelay', 'blockFee', 'includeFee', 'blockAward', 'blockAwardwoFee'], axis=1)
minerUncleBlocks = minerUncleBlocks.rename(columns={'gasUsed': 'uncleGasUsed'})

# Create mainchain dataframe to summarize mined blocks
mainBlocks = pd.DataFrame(minerData.loc[minerData['uncle']==0])
avgMainRewardwoFee = mainBlocks['blockAwardwoFee'].mean()
avgMainRewardwFee = mainBlocks['blockAward'].mean()

#create summary table
minerBlocks = mainBlocks.groupby('miner').sum()
minerBlocks = minerBlocks.drop(['id', 'blockNum', 'gasLimit', 'includedBlockNum', 'duplicates', 'keep', 'uncle'], axis=1)


# Merge the two tables on miner
minerBlocks = minerBlocks.join(minerUncleBlocks)
minerBlocks['uncleAward'].fillna(0, inplace = True)
minerBlocks['uncle'].fillna(0, inplace = True)


minerBlocks['totReward'] = minerBlocks['blockAward'] + minerBlocks['uncleAward']

#calc Total Return
minerBlocks['totalBlocks'] = minerBlocks['main'] + minerBlocks['uncle']
minerBlocks['mainAwardwFee'] = minerBlocks['blockAward']/minerBlocks['main']
minerBlocks['mainAwardwoFee'] =  minerBlocks['blockAwardwoFee'] / minerBlocks['main']
minerBlocks['uncRatio'] = minerBlocks['uncle'] / minerBlocks['totalBlocks']
minerBlocks['avgUncleAward'] = minerBlocks['uncleAward'] / minerBlocks['uncle']
minerBlocks['avgGasUsed'] = (minerBlocks['gasUsed'] + minerBlocks['uncleGasUsed'])/totalBlocks

minerBlocks['avgReward'] = minerBlocks['totReward'] / minerBlocks['totalBlocks']
minerBlocks = minerBlocks.sort_values('avgReward')

print(minerBlocks)

# Regression model for gas
minerData['const'] = 1
minerData['gasUsedPerM'] = minerData['gasUsed']/1e6


model = sm.OLS(minerData['uncle'], minerData[['const','gasUsedPerM']])
results = model.fit()
print (results.summary())

dictResults = dict(results.params)
print (dictResults)


mainUncleDiff = avgUncleAward - avgMainRewardwoFee
breakeven = -1*dictResults['gasUsedPerM']/1e6 * mainUncleDiff * 1e9
print(breakeven)

#find Profit

#Awards without tx Fees
avgMainRewardwoFee = minerBlocks['mainAwardwoFee'].mean()
avgMainReward = minerBlocks['avgReward'].mean()
avgUncleAward = minerBlocks['avgUncleAward'].mean()
totalMainBlocks = len(mainBlocks)
totalUncleBlocks = len(uncleBlocks)
allBlocks = len(minerData)
mainBlockRatio = len(mainBlocks)/float(allBlocks)
uncBlockRatio = len(uncleBlocks)/float(allBlocks)

emptyBlockTotal = (totalMainBlocks*avgMainRewardwoFee*(1-dictResults['const'])) + (totalUncleBlocks*avgUncleAward*dictResults['const'])

actualBlockTotal = (totalMainBlocks*avgMainReward*mainBlockRatio) + (totalUncleBlocks*avgUncleAward*uncBlockRatio)

print(avgMainReward, avgMainRewardwoFee, avgUncleAward)
print (allBlocks, mainBlockRatio, uncBlockRatio)
print (emptyBlockTotal/float(allBlocks))
print (actualBlockTotal/float(allBlocks))  

miner1Data = minerData.loc[minerData['miner'] == '0xea674fdde714fd979de3edf0f56aa9716b898ec8', :]
model = sm.OLS(miner1Data['uncle'], miner1Data[['const','gasUsedPerM']])
results = model.fit()
print (results.summary())
print(miner1Data.describe())



'''
miner2Data = minerData.loc[minerData['miner'] == '0x61c808d82a3ac53231750dadc13c777b59310bd9', :]
model = sm.OLS(miner2Data['uncle'], miner2Data[['const','gasUsedPerM']])
results = model.fit()
print (results.summary())
print(miner2Data.describe())

miner3Data = minerData.loc[minerData['miner'] == '0xb2930b35844a230f00e51431acae96fe543a0347', :]
model = sm.OLS(miner3Data['uncle'], miner3Data[['const','gasUsedPerM']])
results = model.fit()
print (results.summary())
print(miner3Data.describe())

miner4Data = minerData.loc[minerData['miner'] == '0x1e9939daaad6924ad004c2560e90804164900341', :]
model = sm.OLS(miner4Data['uncle'], miner4Data[['const','gasUsedPerM']])
results = model.fit()
print (results.summary())
print(miner4Data.describe())

miner5Data = minerData.loc[(minerData['miner']== '0xea674fdde714fd979de3edf0f56aa9716b898ec8') | (minerData['miner']=='0x61c808d82a3ac53231750dadc13c777b59310bd9') | (minerData['miner'] == '0xb2930b35844a230f00e51431acae96fe543a0347'),  :]
model = sm.OLS(miner5Data['uncle'], miner5Data[['const','gasUsedPerM']])
results = model.fit()
print (results.summary())
print(miner5Data.describe())

miner6Data = minerData.loc[minerData['miner'] == '0x2a65aca4d5fc5b5c859090a6c34d164135398226', :]
model = sm.OLS(miner6Data['uncle'], miner6Data[['const','gasUsedPerM']])
results = model.fit()
print (results.summary())
print(miner6Data.describe())
'''
