import mysql.connector, sys

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()

query = ("CREATE TABLE speedo2 ("
        "id INT NOT NULL AUTO_INCREMENT, " 
        "blockNum INT, " 
        "gasUsed INT, "
        "miner TEXT, "
        "uncle BOOLEAN, "
        "main BOOLEAN, "
        "gasLimit INT, "
        "numTx INT,"
        "speed DECIMAL(4,3)"
        "blockHash TEXT, " 
        "includedBlockNum INT, "
        "blockFee INT, " 
        "uncleBlockNum INT, "
        "uncsReported INT, " 
        "PRIMARY KEY (id))")

cursor.execute(query)
cursor.close()
cnx.close()