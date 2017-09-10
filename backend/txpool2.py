import mysql.connector, sys
import subprocess, json
import pandas as pd
from sqlalchemy import create_engine

startBlock = int(sys.argv[1])
dblock = startBlock-25

engine = create_engine('mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

out = subprocess.check_output(['geth', '--exec', 'JSON.stringify(txpool.content)', 'attach', 'http://localhost:8545'])

dict = json.loads(out)
dict2 = json.loads(dict)

pendingTxList = []

for key1, value in dict2['pending'].iteritems():
    for key, value2 in value.iteritems():
        pendingTxList.append(value2['hash'])
        




txpool = pd.DataFrame(data = pendingTxList, columns=['txHash'])
txpool['block'] = startBlock

print(txpool)

#txpool.to_sql(con=engine, name = 'txpool', if_exists='append', index=False)

txpool.to_sql(con=engine, name = 'txpool2', if_exists='append', index=False)


cursor.execute("DELETE FROM txpool2  WHERE block < %(dblock)s ", {'dblock': dblock} )
cnx.commit()
cursor.close()

#ALTER TABLE txpool ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY 

#CREATE TABLE txpool (id INT NOT NULL AUTO_INCREMENT, txHash VARCHAR(75), block INT, PRIMARY KEY (id));










