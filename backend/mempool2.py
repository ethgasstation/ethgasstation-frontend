#Reports on mempool wait times and miner gas mined on last block and votes on gas limit

import mysql.connector, sys, os
import pandas as pd
import numpy as np
import subprocess, json

endBlock = int(sys.argv[1])
callTime = int(sys.argv[2])
startBlock = str(endBlock-500)
priorBlock = str(endBlock-1)
endBlock = str(endBlock)

dictMiner = {
    '0xea674fdde714fd979de3edf0f56aa9716b898ec8':'Ethermine',
    '0x1e9939daaad6924ad004c2560e90804164900341':'ethfans',
    '0xb2930b35844a230f00e51431acae96fe543a0347':'miningpoolhub',
    '0x4bb96091ee9d802ed039c4d1a5f6216f90f81b01':'Ethpool',
    '0x52bc44d5378309ee2abf1539bf71de1b7d7be3b5':'Nanopool',
    '0x2a65aca4d5fc5b5c859090a6c34d164135398226':'Dwarfpool',
    '0x829bd824b016326a401d083b33d092293333a830':'f2pool',
    '0xa42af2c70d316684e57aefcc6e393fecb1c7e84e':'Coinotron',
    '0x6c7f03ddfdd8a37ca267c88630a4fee958591de0':'alpereum'

}

#load mempool and most recent block transactions

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

query = ("SELECT transactions.txHash, transactions.postedBlock, transactions.gasPrice, transactions.gasOffered, transactions.tsPosted, minedtransactions.minedBlock, minedtransactions.gasused FROM transactions LEFT JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > %s and transactions.postedBlock < %s")

query2 = ("SELECT miner, blockNum, gasLimit, gasUsed FROM speedo2 WHERE blockNum >= %s AND blocknum <= %s AND uncle = 0 ORDER BY blockNum ASC")


cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names
memPoolTx = pd.DataFrame(cursor.fetchall())
memPoolTx.columns = head

cursor.execute(query2, (priorBlock, endBlock))
head = cursor.column_names
minedTx = pd.DataFrame(cursor.fetchall())
minedTx.columns = head


cursor.execute("SELECT txHash FROM txpool2 WHERE block = %(priorBlock)s", {'priorBlock':priorBlock})
head = cursor.column_names
txpool = pd.DataFrame(cursor.fetchall())
txpool.columns = head
cursor.close()


endBlock = int(endBlock)

memPoolTx['gasPrice'] = memPoolTx['gasPrice'].apply(lambda x: x/1000)
memPoolTx['gasPrice'] = memPoolTx['gasPrice'].apply(lambda x: np.round(x, decimals=0) if x >=1 else np.round(x, decimals=3))
memPoolTx['gasOffered']= memPoolTx['gasOffered'].apply(lambda x: x/1e6)
memPoolTx['gasused']= memPoolTx['gasused'].apply(lambda x: x/1e6)

memPoolTx['waitBlocks'] = memPoolTx['postedBlock'].apply(lambda x: endBlock-x)
memPoolTx['waitTime'] = memPoolTx['tsPosted'].apply(lambda x: callTime-x)
memPoolTx['lastBlock'] = (memPoolTx['minedBlock'] == endBlock)
memPoolTx['gasRemoved'] = memPoolTx['gasOffered']
memPoolTx.loc[memPoolTx['lastBlock'] == False, 'gasRemoved'] = np.nan 
memPoolTx['pending'] = pd.isnull(memPoolTx['minedBlock'])
memPoolTx = memPoolTx[(memPoolTx['pending']==True) | (memPoolTx['lastBlock']==True)]
print (memPoolTx)
memPoolTx = memPoolTx.merge(txpool, how='inner', on='txHash')
print (memPoolTx)


memPool = memPoolTx.groupby('gasPrice').sum().reset_index()
memPool = memPool.drop(['minedBlock', 'postedBlock', 'tsPosted', 'waitBlocks', 'waitTime'], axis=1)
memPool['gasOffered'] = memPool['gasOffered'].apply(lambda x: np.round(x, decimals=2))
memPool['gasused'] = memPool['gasused'].apply(lambda x: np.round(x, decimals=2))
memPool['gasRemoved'] = memPool['gasRemoved'].apply(lambda x: np.round(x, decimals=2))

memPoolAvg = memPoolTx.groupby('gasPrice').mean().reset_index()
memPoolAvg = memPoolAvg.drop(['minedBlock', 'postedBlock', 'tsPosted', 'gasOffered', 'gasused', 'gasRemoved', 'lastBlock', 'pending', 'gasPrice'], axis=1)
memPoolAvg['waitTime'] = memPoolAvg['waitTime'].apply(lambda x: np.round(x, decimals=0))
memPoolAvg['waitBlocks'] = memPoolAvg['waitBlocks'].apply(lambda x: np.round(x, decimals=2))

memPool = pd.concat([memPool, memPoolAvg], axis = 1)

memPool = memPool.rename(columns = {'lastBlock':'numTxMined', 'pending': 'numTxPending'})
memPool = memPool.fillna(value=0)

#gasLimit Voting

minedTxDiff = minedTx['gasLimit']
minedTxDiff = minedTxDiff.diff()
gasLimitChange = minedTxDiff.sum()

if gasLimitChange < 0:
    vote = 'Lower'
elif gasLimitChange ==0 :
    vote = 'Hold'
else:
    vote = 'Raise'

voteDict = {}
voteDict = minedTx.loc[1,:].to_dict()
voteDict['priorLimit'] = int(minedTx.loc[0,'gasLimit'])
voteDict['priorGasused'] = int(minedTx.loc[0,'gasUsed'])
voteDict['vote'] = vote
voteDict['gasUsed'] = str(voteDict['gasUsed'])
voteDict['blockNum'] = str(voteDict['blockNum'])
voteDict['gasLimit'] = str(voteDict['gasLimit'])

if voteDict['miner'] in dictMiner.keys():
    voteDict['miner'] = dictMiner[voteDict['miner']]
    
query3= ("INSERT INTO votes "
        "(blockNum, miner, vote, gasLimit, priorLimit, gasused, priorGasused)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s)")
cursor= cnx.cursor()
cursor.execute(query3, (voteDict['blockNum'], voteDict['miner'], voteDict['vote'], voteDict['gasLimit'], voteDict['priorLimit'], voteDict['gasUsed'], voteDict['priorGasused']))
cnx.commit()
cursor.close()
cnx.close()

memPoolTable = memPool.to_json(orient = 'records')
parentdir = os.path.dirname(os.getcwd())
if not os.path.exists(parentdir + '/json'):
    os.mkdir(parentdir + '/json')
filepath_memPool = parentdir + '/json/memPool.json'
filepath_minerVote = parentdir + '/json/vote.json'


with open(filepath_minerVote, 'w') as outfile:
    json.dump(voteDict, outfile)

with open(filepath_memPool, 'w') as outfile:
    outfile.write(memPoolTable)


print(memPool)
print(minedTx)
print(gasLimitChange)
print(voteDict)