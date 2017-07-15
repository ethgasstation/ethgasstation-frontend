import mysql.connector, sys, os
import pandas as pd
import numpy as np
import subprocess, json
import os, subprocess, re
import urllib
import math
from patsy import dmatrices
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

query = ("SELECT * from validationData")

cursor.execute(query)
head = cursor.column_names
txData = pd.DataFrame(cursor.fetchall())
txData.columns = head
txData = txData.dropna()

y, X = dmatrices('actual ~ predictions', data = txData, return_type = 'dataframe')

print(y[:5])
print(X[:5])

model = sm.OLS(y, X)
results = model.fit()
print (results.summary())

print('prediction')
print(txData['predictions'].mean())
print(txData['predictions'].median())
print(txData['predictions'].quantile(.05))
print(txData['predictions'].quantile(.95))

print('actual')
print(txData['actual'].mean())
print(txData['actual'].median())
print(txData['actual'].quantile(.05))
print(txData['actual'].quantile(.95))





fast = txData.loc[txData['predictions'] <= 5, 'actual']

print ('<=5')
print (fast.count())
print (fast.mean())
print (fast.median())
print (fast.quantile(.95))


fast = txData.loc[(txData['predictions'] > 5) & (txData['predictions'] <= 10), 'actual']

print ('6-10')
print (fast.count())
print (fast.mean())
print (fast.median())
print (fast.quantile(.95))

fast = txData.loc[(txData['predictions'] > 10) & (txData['predictions'] <= 20), 'actual']

print ('11-20')
print (fast.count())
print (fast.mean())
print (fast.median())
print (fast.quantile(.95))

fast = txData.loc[(txData['predictions'] > 20) & (txData['predictions'] <= 40), 'actual']

print ('21-40')
print (fast.count())
print (fast.mean())
print (fast.median())
print (fast.quantile(.95))


fast = txData.loc[(txData['predictions'] > 40) & (txData['predictions'] <= 80), 'actual']

print ('41-80')
print (fast.count())
print (fast.mean())
print (fast.median())
print (fast.quantile(.95))

txData['outLimit'] = txData['predictions'].apply(lambda x: x * 2.5)

txData['outlier'] = txData['actual'] > txData['outLimit']

print('count = total ')
count = txData['outlier'].count()
false = txData['outlier'].sum()
ratio = false / float(count)
print (count, false, ratio)



print('count = Fast ')
count = txData.loc[txData['predictions'] <=2, 'outlier'].count()
false = txData.loc[txData['predictions'] <=2, 'outlier'].sum()
ratio = false / float(count)
print (count, false, ratio)

print('count  = avg ')
count = txData.loc[(txData['predictions'] >2) & (txData['predictions'] <13), 'outlier'].count()
false = txData.loc[(txData['predictions'] >2) & (txData['predictions'] <13), 'outlier'].sum()
ratio = false / float(count)
print (count, false, ratio)

print('count = inclusive ')
count = txData.loc[txData['predictions'] <13, 'outlier'].count()
false = txData.loc[txData['predictions'] <13, 'outlier'].sum()
ratio = false / float(count)
print (count, false, ratio)



print('count slow')
count = txData.loc[(txData['predictions'] >=13) & (txData['predictions'] <60), 'outlier'].count()
false =  txData.loc[(txData['predictions'] >=13) & (txData['predictions'] <60), 'outlier'].sum()
ratio = false / float(count)
print (count, false, ratio)


print('count very slow ')
count = txData.loc[txData['predictions'] >=13, 'outlier'].count()
false = txData.loc[txData['predictions'] >=13, 'outlier'].sum()
ratio = false / float(count)
print (count, false, ratio)

'''
plot = txData.plot.scatter(x ='predictions', y='actual')
plt.savefig('valid.png')
'''