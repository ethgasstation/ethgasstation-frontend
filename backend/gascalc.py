import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import math
import sys

# Get current Gas Price Cats
import urllib,json
url = "http://localhost/json/ethgasAPI.html"
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


query = ("SELECT (minedtransactions.minedBlock - transactions.postedBlock) as delay, (minedtransactions.tsMined - transactions.tsPosted) as delaysecs, minedtransactions.gasused, transactions.gasOffered, minedtransactions.minedGasPrice,minedtransactions.minedGasPriceCat, minedtransactions.miner, minedtransactions.tsMined, minedtransactions.minedBlock FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock IS NOT NULL AND transactions.postedBlock > %s AND transactions.postedBlock < %s ORDER BY delay")

cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names

txData = pd.DataFrame(cursor.fetchall())
txData.columns = head


#Clean Data
txData['minedGasPrice'] = pd.to_numeric(txData['minedGasPrice'], errors='coerce')
txData['delay'] = pd.to_numeric(txData['delay'], errors='coerce')

txData.loc[(txData['delay']>500) | (txData['delay']<=0), 'delay'] =  np.nan
txData.loc[(txData['delaysecs']>60000) | (txData['delaysecs']<=0), 'delaysecs'] = np.nan

txData = txData.dropna()

#--Clean Data

blockTime = txData[['tsMined', 'minedBlock']]
blockTime = blockTime.sort_values('minedBlock')
blockTime2 = blockTime.groupby('minedBlock', as_index=False).mean()

blockTime2 = blockTime2.diff()

blockTime2.loc[blockTime2['minedBlock'] > 1, ['tsMined', 'minedBlock']] = np.nan
blockInterval = blockTime2['tsMined'].mean()

blockTime = {
    'blockInterval':blockInterval
}

#define gas predictors


dep = pd.DataFrame()
dep['priceCat1'] = (txData['minedGasPrice'] < gasdata['Average']).astype(int)
dep['priceCat2'] = (txData['minedGasPrice'] == gasdata['Average']).astype(int)
dep['priceCat3'] = ((txData['minedGasPrice'] > gasdata['Average']) & (txData['minedGasPrice'] < gasdata['Fastest'])).astype(int)
dep['priceCat4'] = (txData['minedGasPrice'] > gasdata['Fastest']).astype(int)


# Define gasused cats

quantiles= txData['gasused'].quantile([.5, .75, .9, 1])


dep['gasCat2'] = ((txData['gasused']>21000) & (txData['gasused']<=quantiles[.75])).astype(int)
dep['gasCat3'] = ((txData['gasused']>quantiles[.75]) & (txData['gasused']<=quantiles[.9])).astype(int)
dep['gasCat4'] = (txData['gasused']> quantiles[.9]).astype(int)

dep = sm.add_constant(dep)

indep = txData['delay']

model = sm.Poisson(indep, dep.iloc[:,[0,1,3,4,5,6,7]])


results = model.fit(disp=0)
dictResults = dict(results.params)


quantiles = quantiles.reset_index(drop=True)
quantiles.rename({0: '50pct', 1: '75pct', 2: '90pct', 3: 'max'}, inplace=True)
quantiles = quantiles.to_dict()

dictResults.update(quantiles)
dictResults.update(blockTime)

with open('../json/calc.html', 'w') as outfile:
    json.dump(dictResults, outfile)

print (results.summary())


'''
dep['predict'] = results.predict()
dep['delay'] = indep
print(dep)
'''



cursor.close()
cnx.close()
