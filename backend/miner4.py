import mysql.connector, sys, os
import pandas as pd
import numpy as np
import statsmodels.api as sm
import subprocess, json

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()



startBlock = int(sys.argv[1])
endBlock = int(sys.argv[2])

#prune databases
deleteBlock = endBlock - 10000
deleteBlock2 = endBlock - 100000

cursor.execute("DELETE FROM transactions WHERE postedBlock < %(deleteBlock)s", {'deleteBlock':deleteBlock})
cnx.commit()
cursor.execute("DELETE FROM minedtransactions WHERE minedBlock < %(deleteBlock)s", {'deleteBlock':deleteBlock})
cnx.commit()
cursor.execute("DELETE FROM speedo2 WHERE blockNum < %(deleteBlock2)s", {'deleteBlock2':deleteBlock2})
cnx.commit()
#cursor.execute("DELETE FROM txDataLast10k WHERE blockNum < %(deleteBlock2)s", {'deleteBlock2':deleteBlock2})
#cnx.commit()
#cursor.execute("DELETE FROM txDataLast100b WHERE blockNum < %(deleteBlock2)s", {'deleteBlock':deleteBlock})
#cnx.commit()


# First Query to Determine Block TIme, and Estimate Miner Policies
query = ("SELECT * FROM speedo2 where blockNum>= %s and blockNum < %s")
cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

minerData = pd.DataFrame(cursor.fetchall())
minerData.columns = head
cursor.close()
cnx.close()

# Find Identical Blocks
minerData['idents'] = minerData.duplicated(subset=['blockHash'])
print(minerData[minerData['idents']==True])
minerData = minerData[minerData['idents']==False]

print(minerData['uncle'].sum())
print(minerData['uncsReported'].sum())

# Find Gaps

minerData = minerData.sort_values(by=['main', 'blockNum'])
minerData = minerData.reindex()
minerData['check'] = minerData.loc[minerData['main']==1, 'blockNum']
minerData['check'] = minerData['check'].shift(-1)
minerData['diff'] = minerData['check'] - minerData['blockNum']

gaps = pd.DataFrame (minerData.loc[minerData['diff']>1, ['blockNum', 'check', 'diff']])
for index, row in gaps.iterrows():
    print('gaps') 
    print(row['blockNum'])
    print(row['check'])

#clean data

minerData['uncsReported'].fillna(value=0, inplace=True)
minerData.loc[minerData['uncle']==1, 'blockFee'] = 0
minerData = minerData.dropna(subset=['blockFee'])

#uncleReportingFees
minerData.loc[minerData['uncsReported']==1, 'includeFee' ] = .15625
minerData.loc[minerData['uncsReported']==2, 'includeFee'] = .3125
minerData.loc[minerData['uncsReported']==0, 'includeFee'] = 0

# Define Miners of Interest

keyMiners = ['0xea674fdde714fd979de3edf0f56aa9716b898ec8', '0x1e9939daaad6924ad004c2560e90804164900341', '0xb2930b35844a230f00e51431acae96fe543a0347', '0x2a65aca4d5fc5b5c859090a6c34d164135398226', '0x829bd824b016326a401d083b33d092293333a830', '0x4bb96091ee9d802ed039c4d1a5f6216f90f81b01']

dictMiners = {
    '0xea674fdde714fd979de3edf0f56aa9716b898ec8':'Ethermine',
    '0x1e9939daaad6924ad004c2560e90804164900341':'Ethfans',
    '0xb2930b35844a230f00e51431acae96fe543a0347':'Miningpoolhub',
    '0x4bb96091ee9d802ed039c4d1a5f6216f90f81b01':'Ethpool',
    '0x52bc44d5378309ee2abf1539bf71de1b7d7be3b5':'Nanopool',
    '0x2a65aca4d5fc5b5c859090a6c34d164135398226':'Dwarfpool',
    '0x829bd824b016326a401d083b33d092293333a830':'F2pool',
    '0xa42af2c70d316684e57aefcc6e393fecb1c7e84e':'Coinotron',
    '0x6c7f03ddfdd8a37ca267c88630a4fee958591de0':'Alpereum',
    'All Others':'All Others'
}
minerData['miner2']=minerData['miner']
minerData.loc[~minerData['miner'].isin(keyMiners), ['miner']] = 'All Others'


#define constants for all blocks

totalBlocks = len(minerData)
totalUncsReported = minerData['uncsReported'].sum()
totAvgGasUsed = minerData['gasUsed'].mean()
uncleRate = totalUncsReported/float(totalBlocks)
#note blockfee stored as gwei/1e4
minerData['blockFee'] = minerData['blockFee']/1e5
totalIncludeFee = minerData['includeFee'].sum()
minerData['blockAward'] = 5 + minerData['includeFee'] + minerData['blockFee']
minerData['mainAwardwoFee'] = 5 + minerData['includeFee']
minerData['mainAwardwFee'] = minerData['blockAward']
minerData.loc[minerData['uncle']==1, ['mainAwardwoFee', 'mainAwardwFee']] = np.nan
minerData['incDelay'] = minerData['includedBlockNum'] - minerData['blockNum']
minerData['mgasUsed'] = minerData['gasUsed']/1e6
minerData['mainGasUsed'] = minerData.loc[minerData['main']==1, 'gasUsed']
minerData['uncleGasUsed'] = minerData.loc[minerData['uncle']==1, 'gasUsed']
avgMgasUsed = minerData['mgasUsed'].mean()
minMgasUsed = minerData['mgasUsed'].min()
maxMgasUsed = minerData['mgasUsed'].max()
medMgasUsed = minerData['mgasUsed'].quantile(.5)
avgUncleGas = minerData.loc[minerData['uncle']==1, 'mgasUsed'].mean()
avgMainGas = minerData.loc[minerData['main']==1, 'mgasUsed'].mean()

minerData.loc[(minerData['gasUsed']==0) & (minerData['uncle']==True), 'emptyUncle'] = 1
minerData.loc[(minerData['gasUsed']==0) & (minerData['main']==True), 'emptyBlock'] = 1
minerData.loc[(minerData['gasUsed']==0), 'empty'] = 1
minerData.loc[(minerData['gasUsed']>0), 'empty'] = 0

minerData['emptyUncle'].fillna(0, inplace=True)
minerData['emptyBlock'].fillna(0, inplace=True)
emptyUncles = minerData['emptyUncle'].sum()

avgMainRewardwFee = minerData['mainAwardwFee'].mean()
avgMainRewardwoFee = minerData['mainAwardwoFee'].mean()
avgBlockFee = minerData['blockFee'].mean()
avgTxPrice = avgBlockFee/float(totAvgGasUsed)*1e9

#define reward for uncleBlocks

minerData['uncleAward'] = (8-minerData['incDelay'])/8 * 5
avgUncleAward = minerData['uncleAward'].mean()
minerData.loc[minerData['uncle']==1, 'blockAward'] = minerData.loc[minerData['uncle']==1, 'uncleAward']

avgBlockAward = minerData['blockAward'].mean()
avgUncleAward = minerData['uncleAward'].mean()
totalUncles = minerData.loc[minerData['uncle']==1, 'uncle'].sum()
totalMains = minerData.loc[minerData['main']==1, 'main'].sum()

# find empty block uncle rate

totemptyBlocks = len(minerData.loc[minerData['gasUsed']==0])
emptyMains =  len(minerData.loc[(minerData['gasUsed']==0) & (minerData['main']==True)])
emptyUnclePct = emptyUncles/float(totemptyBlocks)
print (totemptyBlocks, emptyUncles, emptyMains)
print ("%.3f" % (emptyUnclePct))


print minerData

#create summary table
minerBlocks = minerData.groupby('miner').sum()
minerBlocks = minerBlocks.drop(['id', 'blockNum', 'includedBlockNum', 'idents', 'incDelay'], axis=1)

uncGraphArray = []
point = {}
uncGraph = minerData.groupby('miner2').sum()
uncGraph['totalBlocks']= uncGraph['main'] + uncGraph['uncle']
uncGraph['uncRatio']= uncGraph['uncle'] / uncGraph['totalBlocks']
for index, row in uncGraph.iterrows(): 
    point['y']=row['uncRatio']
    point['x']=row['totalBlocks']
    uncGraphArray.append(dict(point))


#calc miner totals
minerBlocks['totalBlocks'] = minerBlocks['main'] + minerBlocks['uncle']
minerBlocks['avgMainAwardwFee'] = minerBlocks['mainAwardwFee']/minerBlocks['main']
minerBlocks['avgBlockFee'] = minerBlocks['blockFee']/minerBlocks['main']
minerBlocks['avgMainAwardwoFee'] =  minerBlocks['mainAwardwoFee'] / minerBlocks['main']
minerBlocks['uncRatio'] = minerBlocks['uncle'] / minerBlocks['totalBlocks']
minerBlocks['emptyUncRatio'] = minerBlocks['emptyUncle']/(minerBlocks['emptyUncle']+ minerBlocks['emptyBlock'])
minerBlocks['avgUncleAward'] = minerBlocks['uncleAward'] / minerBlocks['uncle']
minerBlocks['avgGasUsed'] = minerBlocks['gasUsed']/minerBlocks['totalBlocks']
minerBlocks['avgUncleGas'] = minerBlocks['uncleGasUsed']/minerBlocks['uncle']
minerBlocks['avgMainGas'] = minerBlocks['mainGasUsed']/minerBlocks['main']
minerBlocks['avgTxPrice'] = minerBlocks['avgBlockFee']/minerBlocks['avgGasUsed']*1e9
minerBlocks['avgReward'] = minerBlocks['blockAward'] / minerBlocks['totalBlocks']
for index, row in minerBlocks.iterrows():
    avg = minerData.loc[minerData['miner']==index, 'blockAward'].mean()
    min = minerData.loc[minerData['miner']==index, 'mgasUsed'].min()
    max = minerData.loc[minerData['miner']==index, 'mgasUsed'].max()
    med = minerData.loc[minerData['miner']==index, 'mgasUsed'].quantile(.5)
    minerBlocks.loc[index, 'minGas'] = min
    minerBlocks.loc[index, 'maxGas'] = max
    minerBlocks.loc[index, 'medGas'] = med

minerBlocks = minerBlocks.sort_values('totalBlocks', ascending = False)

print(minerBlocks)

# Regression model for gas
minerData['const'] = 1
model = sm.OLS(minerData['uncle'], minerData[['const','mgasUsed']])
results = model.fit()
print('all miners')
print (results.summary())
dictResults = dict(results.params)

mainUncleDiff = avgUncleAward - avgMainRewardwoFee
breakeven = -1*dictResults['mgasUsed']/1e6 * mainUncleDiff * 1e9
print(breakeven)

#find Profit
expectedEmptyAward = (avgMainRewardwoFee*(1-dictResults['const'])) + (avgUncleAward*dictResults['const'])
predictedUncle = dictResults['const'] + (dictResults['mgasUsed'] * totAvgGasUsed/1e6)
expectedTxAward = (avgMainRewardwFee*(1-predictedUncle)) + (avgUncleAward*predictedUncle)

profit = expectedTxAward - expectedEmptyAward
profitpct = profit/avgBlockFee
profitpctBlock = profit/expectedTxAward
#create Dataframe

resultTable = {
    'miner': ['Total'],
    'totalBlocks': [totalBlocks],
    'uncles': [totalUncles],
    'emptyUncles':[emptyUncles],
    'avgmGas': [avgMgasUsed],
    'minGas':[minMgasUsed],
    'maxGas':[maxMgasUsed],
    'medGas':[medMgasUsed],
    'avgUncleGas':[avgUncleGas],
    'avgMainGas':[avgMainGas],
    'uncRate': [uncleRate],
    'predictedUncRate': [predictedUncle],
    'zeroUncRate': [dictResults['const']],
    'actualZeroUncRate': [emptyUnclePct],
    'avgUncleReward': [avgUncleAward],
    'avgMainRewardwoFee': [avgMainRewardwoFee],
    'avgTxFees': [avgBlockFee],
    'predictEmpAward': [expectedEmptyAward],
    'predictTxAward': [expectedTxAward],
    'actualTxAward':[avgBlockAward],
    'breakeven':[breakeven],
    'profit': [profit],
    'profitPct': [profitpct],
    'profitPctBlock': [profitpctBlock]}

resultSummary = pd.DataFrame.from_dict(resultTable)
resultSummary = resultSummary[['miner', 'totalBlocks', 'uncles', 'emptyUncles', 'uncRate', 'predictedUncRate', 'avgmGas','zeroUncRate', 'actualZeroUncRate','avgUncleReward', 'avgMainRewardwoFee', 'avgTxFees', 'predictEmpAward', 'predictTxAward', 'actualTxAward', 'breakeven', 'profit', 'profitPct', 'profitPctBlock', 'minGas', 'maxGas','medGas', 'avgUncleGas', 'avgMainGas']]

miningpoolgas = minerBlocks.loc['0xb2930b35844a230f00e51431acae96fe543a0347', 'avgGasUsed']
miningpoolfee = minerBlocks.loc['0xb2930b35844a230f00e51431acae96fe543a0347', 'avgBlockFee']



x = 1
for index, row in minerBlocks.iterrows(): 
    md = minerData.loc[minerData['miner']==index, :]
    model = sm.OLS(md['uncle'], md[['const', 'mgasUsed']])
    results = model.fit()
    dictResults = dict(results.params)
    predictedUncle = dictResults['const'] + (dictResults['mgasUsed'] * row['avgGasUsed']/1e6)
    mpoolUncle = dictResults['const'] + (dictResults['mgasUsed'] * miningpoolgas/1e6)
    mpoolAward = ((row['avgMainAwardwoFee']+(miningpoolgas * avgTxPrice/1e9))*(1-mpoolUncle)) + (row['avgUncleAward']*mpoolUncle)
    expectedEmptyAward = (row['avgMainAwardwoFee']*(1-dictResults['const'])) + (row['avgUncleAward']*dictResults['const'])
    expectedTxAward = (row['avgMainAwardwFee']*(1-predictedUncle)) + (row['avgUncleAward']*predictedUncle)
    mainUncleDiff = row['avgUncleAward'] - row['avgMainAwardwoFee']
    breakeven = -1*dictResults['mgasUsed']/1e6 * mainUncleDiff * 1e9
    resultSummary.loc[x, 'miner'] = dictMiners[index]
    resultSummary.loc[x, 'totalBlocks'] = row['totalBlocks']
    resultSummary.loc[x, 'uncles'] = row['uncle']
    resultSummary.loc[x, 'emptyUncles'] = row['emptyUncle']
    resultSummary.loc[x, 'avgmGas'] = row['avgGasUsed']/1e6
    resultSummary.loc[x, 'avgUncleGas'] = row['avgUncleGas']/1e6
    resultSummary.loc[x, 'avgMainGas'] = row['avgMainGas']/1e6
    resultSummary.loc[x, 'minGas'] = row['minGas']
    resultSummary.loc[x, 'maxGas'] = row['maxGas']
    resultSummary.loc[x, 'medGas'] = row['medGas']
    resultSummary.loc[x, 'uncRate'] = row['uncRatio']
    resultSummary.loc[x, 'predictedUncRate'] = predictedUncle
    resultSummary.loc[x, 'zeroUncRate'] = dictResults['const']
    resultSummary.loc[x, 'actualZeroUncRate'] = row['emptyUncRatio']
    resultSummary.loc[x, 'avgUncleReward'] = row['avgUncleAward']
    resultSummary.loc[x, 'avgMainRewardwoFee'] = row['avgMainAwardwoFee']
    resultSummary.loc[x, 'avgTxFees'] = row['avgBlockFee']
    resultSummary.loc[x, 'predictEmpAward'] = expectedEmptyAward
    resultSummary.loc[x, 'predictTxAward'] = expectedTxAward
    resultSummary.loc[x, 'actualTxAward'] = row['avgReward']
    resultSummary.loc[x, 'profit'] = row['avgReward'] - expectedEmptyAward
    resultSummary.loc[x, 'profitPct'] = (row['avgReward'] - expectedEmptyAward)/ row['avgBlockFee']
    resultSummary.loc[x, 'profitPctBlock'] = (row['avgReward'] - expectedEmptyAward) / row['avgReward']
    resultSummary.loc[x, 'breakeven'] = breakeven
    resultSummary.loc[x, 'potentialAward'] = mpoolAward
    resultSummary.loc[x, 'potentialProfit'] = mpoolAward - row['avgReward']
    resultSummary.loc[x, 'avgTxPrice'] = row['avgTxPrice']
    print(dictMiners[index])
    print (results.summary())
    x=x+1


#resultSummary = resultSummary.reindex([0, 2, 3, 4, 5, 6, 7, 1])

model = sm.OLS(minerData['blockAward'], minerData[['const','empty']])
results = model.fit()
print (results.summary())

#for index,row in minerBlocks

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(resultSummary)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(minerBlocks)

minerProfits = resultSummary.to_json(orient = 'records')

parentdir = os.path.dirname(os.getcwd())
if not os.path.exists(parentdir + '/json'):
    os.mkdir(parentdir + '/json')
filepath_profit = parentdir + '/json/profit.json'

with open(filepath_profit, 'w') as outfile:
    outfile.write(minerProfits)

if not os.path.exists(parentdir + '/json'):
    os.mkdir(parentdir + '/json')
filepath_uncGraph = parentdir + '/json/uncGraph.json'

with open(filepath_uncGraph, 'w') as outfile:
    json.dump(uncGraphArray, outfile)


'''
minerData.loc[minerData['miner']== '0x61c808d82a3ac53231750dadc13c777b59310bd9', 'f2pool'] = 1
minerData.loc[minerData['miner']!= '0x61c808d82a3ac53231750dadc13c777b59310bd9', 'f2pool'] = 0
minerData.loc[minerData['miner']== '0xb2930b35844a230f00e51431acae96fe543a0347', 'mpoolhub'] = 1
minerData.loc[minerData['miner']!= '0xb2930b35844a230f00e51431acae96fe543a0347', 'mpoolhub'] = 0
minerData.loc[~minerData['miner'].isin(['0xb2930b35844a230f00e51431acae96fe543a0347', '0x61c808d82a3ac53231750dadc13c777b59310bd9']), 'others'] = 1
minerData.loc[minerData['miner'].isin(['0xb2930b35844a230f00e51431acae96fe543a0347', '0x61c808d82a3ac53231750dadc13c777b59310bd9']), 'others'] = 0

minerData['f2poolgas'] = minerData['mgasUsed'] * minerData['f2pool']
minerData['mpoolgas'] = minerData['mgasUsed'] * minerData['mpoolhub']

model = sm.OLS(minerData['uncle'], minerData[['const','mgasUsed', 'f2pool', 'mpoolhub', 'f2poolgas', 'mpoolgas']])
results = model.fit()
print (results.summary())
'''