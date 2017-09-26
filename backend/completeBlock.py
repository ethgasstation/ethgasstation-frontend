import mysql.connector, sys, os
import pandas as pd
import numpy as np
import subprocess, json
import os, subprocess, re
import urllib
import math
from sqlalchemy import create_engine

dataset = 'blockSnapshot'
target = 'blockSnapshotComplete'

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

engine = create_engine('mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)

query = ("SELECT {0}.*, minedtransactions.minedBlock FROM {0} LEFT JOIN minedtransactions ON {0}.txHash = minedtransactions.txHash" .format(dataset))

cursor.execute(query)
head = cursor.column_names
predictData = pd.DataFrame(cursor.fetchall())
predictData.columns = head

predictData = predictData[predictData['waitBlocks'] < 2500]
predictData['mined'] = predictData['minedBlock'] - predictData['postedBlock']
totalMined = predictData['mined'].count()
totalTx = len(predictData)
percentMined = round(totalMined/float(totalTx)*100)


predictData.to_sql(con=engine, name = target, if_exists='append', index=False) 

print "Of %s transactions in block, %s or %s percent were mined" % (totalTx, totalMined, percentMined)
