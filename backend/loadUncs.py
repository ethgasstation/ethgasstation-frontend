import mysql.connector, sys
import subprocess, json
import pandas as pd
import numpy as np

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()



startBlock = sys.argv[1]
endBlock = sys.argv[2]

# First Query to Determine Block TIme, and Estimate Miner Policies
query = ("SELECT * FROM speedo2 where blockNum>= %s and blockNum < %s")
cursor.execute(query, (startBlock, endBlock))
head = cursor.column_names
blockData = pd.DataFrame(cursor.fetchall())
blockData.columns = head

addUnc = ("INSERT INTO speedo2 "
        "(blockNum, miner, blockHash, includedBlockNum, gasUsed, main, uncle) "
        "VALUES (%(blockNum)s, %(miner)s, %(hash)s, %(includedBlockNum)s, %(gasUsed)s, %(main)s, %(uncle)s)")

for index, row in blockData.iterrows():
    if row['uncsReported'] > 0 :
        block = str(row['blockNum'])
        for x in range(0, row['uncsReported']):
                uncNum = str(x)
                out = subprocess.check_output(['node', 'getUncs.js', block, uncNum])
                uncData = json.loads(out)
                cursor.execute(addUnc, uncData)
                print(cursor.statement)
                cnx.commit()



