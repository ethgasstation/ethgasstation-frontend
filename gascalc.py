import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import math
import sys

# Get current Gas Price Cats
import urllib,json
url = "http://localhost/ethgasAPI.html"
response = urllib.urlopen(url)
gasdata = json.loads(response.read())
response.close()
for key in gasdata:
    gasdata[key] = int(gasdata[key])

#-- GasPriceCats
startBlock = sys.argv[1]
endBlock = sys.argv[2]

cnx = mysql.connector.connect(user='jake', password='dopamine', host='127.0.0.1', database='tx')

cursor = cnx.cursor()


query = ("SELECT (minedtransactions.minedBlock - transactions.postedBlock) as delay, (minedtransactions.tsMined - transactions.tsPosted) as delaysecs, minedtransactions.gasused, transactions.gasOffered, minedtransactions.minedGasPrice,minedtransactions.minedGasPriceCat, minedtransactions.miner FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock IS NOT NULL AND transactions.postedBlock > %s AND transactions.postedBlock < %s ORDER BY delay")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

txData = pd.DataFrame(cursor.fetchall())
txData.columns = head


#Clean Data
txData['minedGasPrice'] = pd.to_numeric(txData['minedGasPrice'], errors='coerce')
txData['delay'] = pd.to_numeric(txData['delay'], errors='coerce')

txData.loc[(txData['delay']>100) | (txData['delay']<=0), 'delay'] =  np.nan
txData.loc[(txData['delaysecs']>1500) | (txData['delaysecs']<=0), 'delaysecs'] = np.nan

txData = txData.dropna()

#--Clean Data

'''
#Data for Lowess Plot Price

pruned1 = txData.loc[txData['minedGasPrice']==20]
lowessdata = txData.loc[txData['minedGasPrice']!=20]

#random sample of 1000 with 20gp
rand = pruned1.sample(2000)
lowessdata = lowessdata.append(rand)


indep = lowessdata.loc[lowessdata['minedGasPrice']<100, 'delay'].apply(np.log)
dep = lowessdata.loc[lowessdata['minedGasPrice']<100,'minedGasPrice']

lowess = sm.nonparametric.lowess



z = lowess(indep, dep, delta=1)

plotvars = pd.DataFrame(z)

indep = indep.reset_index(drop=True)
dep = dep.reset_index(drop=True)

plotvars['indep']=indep
plotvars['dep']=dep


print (plotvars.info())

print(plotvars)

plt.figure()
ax = plotvars.plot(x=0, y=1)
plt.savefig('low.png')
plotvars.plot(kind='scatter', x='dep', y='indep', ax=ax)
plt.savefig('lowess.png')
#-- Lowess Price Data
'''
'''

#lowess gasused data

pruned2 = txData.loc[txData['gasused']==21000]
lowessdata2 = txData.loc[txData['gasused']!=21000]

#random sample of 1000 with 20gp
rand2 = pruned2.sample(2000)
lowessdata2 = lowessdata2.append(rand2)

indep = lowessdata2.loc[lowessdata2['gasused']<2000000, 'delay'].apply(np.log)
dep = lowessdata2.loc[lowessdata2['gasused']<2000000 , 'gasused']

lowess = sm.nonparametric.lowess

z = lowess(indep, dep, delta=1000)

plotvars2 = pd.DataFrame(z)

indep = indep.reset_index(drop=True)
dep = dep.reset_index(drop=True)

plotvars2['indep']=indep
plotvars2['dep']=dep


print (plotvars2.info())


plt.figure()
ax = plotvars2.plot(x=0, y=1)
plt.savefig('lowess2.png')
plotvars2.plot(kind='scatter', x='dep', y='indep', ax=ax)
plt.savefig('lowess.png')

#---lowess gasused
'''

'''
#lowess gasoffered data

pruned2 = txData.loc[txData['gasOffered']==21000]
lowessdata2 = txData.loc[txData['gasOffered']!=21000]

#random sample of 1000 with 20gp
rand2 = pruned2.sample(2000)
lowessdata2 = lowessdata2.append(rand2)

indep = lowessdata2.loc[lowessdata2['gasOffered']<9000000, 'delay'].apply(np.log)
dep = lowessdata2.loc[lowessdata2['gasOffered']<9000000 , 'gasOffered']

lowess = sm.nonparametric.lowess

z = lowess(indep, dep, delta=1000)

plotvars2 = pd.DataFrame(z)

indep = indep.reset_index(drop=True)
dep = dep.reset_index(drop=True)

plotvars2['indep']=indep
plotvars2['dep']=dep


print (plotvars2.info())


plt.figure()
ax = plotvars2.plot(x=0, y=1)
plt.savefig('lowess2.png')
plotvars2.plot(kind='scatter', x='dep', y='indep', ax=ax)
plt.savefig('lowess.png')

#---lowess gasoffered
'''


'''
#plots

txData[txData['delay']<100].hist(column=0, bins=25)
plt.savefig('hist.png')

txData.loc[(txData.minedGasPrice>=20) & (txData.minedGasPrice <50)].plot.scatter(y='delay', x='minedGasPrice')
plt.savefig('scatter.png')

txData[txData['minedGasPrice']<50].plot.scatter(y='delay', x='minedGasPrice', logy=True)
plt.savefig('logscatter.png')

'''






'''

def definegasvars(ncat1, ncat2, txData):
    dep = pd.DataFrame()
    if ncat1 >= 50 & ncat2 >= 50:
        dep['gasCat1'] = (txData['minedGasPrice'] < 10).astype(int)
        dep['gasCat2'] = ((txData['minedGasPrice'] >= 10) & (txData['minedGasPrice'] < 20)).astype(int)
        dep['gasCat3'] = (txData['minedGasPrice'] == 20).astype(int)
        dep['gasCat4'] = ((txData['minedGasPrice'] > 20) & (txData['minedGasPrice'] < 40)).astype(int)
        dep['gasCat5'] = (txData['minedGasPrice'] >= 40).astype(int)
    else:
        dep['gasCat1'] = (txData['minedGasPrice'] < 20).astype(int)
        dep['gasCat2'] = (txData['minedGasPrice'] == 20).astype(int)
        dep['gasCat3'] = ((txData['minedGasPrice'] > 20) & (txData['minedGasPrice'] < 40)).astype(int)
        dep['gasCat4'] = (txData['minedGasPrice'] >= 40).astype(int)
    return dep.iloc[:,1:]

#gas price categories: first figure out how many
ncat1 = len(txData.loc[txData['minedGasPrice'] <10, :].index)
ncat2 = len(txData.loc[(txData['minedGasPrice'] >= 10) & (txData['minedGasPrice'] < 20), :].index)
'''

'''
# sort dataframe by gasprice

txData = txData.sort_values('minedGasPrice')
txData = txData.reset_index(drop=True)

x= len(txData)
y=0
while y < (x-50):
    txDataSub = txData.iloc[y:y+50]

    if (txDataSub['delay'].mean())<=15:
        print(txDataSub.loc[y+49,['minedGasPrice']])
        print(y)
        print(txDataSub['delay'].mean())
        print(txDataSub['delaysecs'].mean())
        break
    y=y+1

txDataMiner = pd.DataFrame ({'count':txData.groupby('miner').size()}).reset_index()

txDataMiner = txDataMiner.sort_values('count', ascending=False)
print(txDataMiner)

#--sort dataframe by gas price
'''

#define gas predictors


dep = pd.DataFrame()
dep['priceCat1'] = (txData['minedGasPrice'] < gasdata['Average']).astype(int)
dep['priceCat2'] = (txData['minedGasPrice'] == gasdata['Average']).astype(int)
dep['priceCat3'] = ((txData['minedGasPrice'] > gasdata['Average']) & (txData['minedGasPrice'] < gasdata['Fastest'])).astype(int)
dep['priceCat4'] = (txData['minedGasPrice'] > gasdata['Fastest']).astype(int)

#dep = pd.DataFrame()
#dep['gasPrice'] = txData['minedGasPrice']

#define gasused predictors
dep['transferCat'] = (txData['gasused'] == 21000).astype(int)
dep['gasUsedCont'] = txData['gasused']/100000
#dep['offered']=txData['gasOffered']/100000

# Define gasused cats

quantiles= txData['gasused'].quantile([.5, .75, .9, 1])


dep['gasCat2'] = ((txData['gasused']>21000) & (txData['gasused']<=quantiles[.75])).astype(int)
dep['gasCat3'] = ((txData['gasused']>quantiles[.75]) & (txData['gasused']<=quantiles[.9])).astype(int)
dep['gasCat4'] = (txData['gasused']> quantiles[.9]).astype(int)

dep = sm.add_constant(dep)

indep = txData['delay']
#indep = txData['delaysecs']

model = sm.Poisson(indep, dep.iloc[:,[0,1,3,4,7,8,9]])

#model = sm.Poisson(indep, dep.iloc[:,[0,5]])

results = model.fit(disp=0)
dictResults = dict(results.params)


quantiles = quantiles.reset_index(drop=True)
quantiles.rename({0: '50pct', 1: '75pct', 2: '90pct', 3: 'max'}, inplace=True)
quantiles = quantiles.to_dict()

dictResults.update(quantiles)
print (dictResults)

with open('calc.html', 'w') as outfile:
    json.dump(dictResults, outfile)
    #json.dump(quantiles, outfile)


print (results.summary())



'''
dep['predict'] = results.predict()
dep['delay'] = indep
print(dep)
'''

'''

#txData.info()

minerlist = ['0x2a65aca4d5fc5b5c859090a6c34d164135398226', '0x61c808d82a3ac53231750dadc13c777b59310bd9', 
'0xb2930b35844a230f00e51431acae96fe543a0347', '0x1e9939daaad6924ad004c2560e90804164900341', '0x4bb96091ee9d802ed039c4d1a5f6216f90f81b01', '0xea674fdde714fd979de3edf0f56aa9716b898ec8',
'0x52bc44d5378309ee2abf1539bf71de1b7d7be3b5', '0xa42af2c70d316684e57aefcc6e393fecb1c7e84e',
'0x6c7f03ddfdd8a37ca267c88630a4fee958591de0', '0xc0ea08a2d404d3172d2add29a45be56da40e2949',
'0xf3b9d2c81f2b24b0fa0acaaa865b7d9ced5fc2fb'  ]



dwarfpool = txData['miner'].str.contains('0x2a65aca4d5fc5b5c859090a6c34d164135398226')
dwarfpool2 = txData.loc[:,'miner'].count()

f2pool = txData.loc[txData.miner == '0x61c808d82a3ac53231750dadc13c777b59310bd9', 'miner'].count()
miningpoolhub = txData.loc[txData.miner == '0xb2930b35844a230f00e51431acae96fe543a0347', 'miner'].count()
ethfans = txData.loc[txData.miner == '0x1e9939daaad6924ad004c2560e90804164900341', 'miner'].count()
ethpool = txData.loc[txData.miner == '0x4bb96091ee9d802ed039c4d1a5f6216f90f81b01', 'miner'].count()


#print number of tx mined by topminers

print(txData[txData['miner'].isin(minerlist)].groupby('miner').size())

#print(grouped.size())

groupedGas = txData.loc[txData['gasused']>100000, :]


print(groupedGas[groupedGas['miner'].isin(minerlist)].groupby('miner').size())

'''

'''

all = txData['miner'].isin(minerlist).sum()
print(all.sum())

print(dwarfpool.sum())
print(dwarfpool2)
print(f2pool)
print(miningpoolhub)
print(ethfans)
print(ethpool)
'''

cursor.close()
cnx.close()
