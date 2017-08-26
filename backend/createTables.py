import mysql.connector, sys

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()
'''
query = ("CREATE TABLE speedo2 ("
        "id INT NOT NULL AUTO_INCREMENT, " 
        "blockNum INT, " 
        "gasUsed INT, "
        "miner TEXT, "
        "uncle BOOLEAN, "
        "main BOOLEAN, "
        "gasLimit INT, "
        "numTx INT,"
        "speed DECIMAL(4,3),"
        "blockHash TEXT, " 
        "includedBlockNum INT, "
        "blockFee INT, " 
        "uncleBlockNum INT, "
        "uncsReported INT, " 
        "PRIMARY KEY (id))")

cursor.execute(query)

query = ("CREATE TABLE txDataLast100b ("
        "id INT NOT NULL AUTO_INCREMENT,"
        "latestblockNum INT,"
        "startSelect INT,"
        "ethConsumedLast100 BIGINT,"
        "medianDelayLast100 DECIMAL(5,3),"
        "PRIMARY KEY (id))")

cursor.execute(query)

query = ("CREATE TABLE txDataLast10k ("
    "id INT NOT NULL AUTO_INCREMENT,"
    "latestblockNum INT,"
    "startSelect INT,"
    "rowsChanged INT,"
    "totalBlocks INT,"
    "emptyBlocks INT,"
    "fullBlocks INT,"

    "totalTx INT,"
    "totalTransfers INT,"
    "totalConCalls INT,"
    "totalTimed INT,"

    "avgGasUsed DECIMAL(8,3),"
    "maxMinedGasPrice INT,"
    "minMinedGasPrice INT,"
    "medianGasPrice INT,"
    "maxMineDelay INT,"
    "minMineDelay INT,"
    "meanMineDelay DECIMAL(8,3),"
    "medianMinedDelay INT,"
    "medianTime INT,"
    "mine5delay INT,"
    "mine5delayTime INT,"
    "mine95delay INT,"
    "mine95delaytime INT,"
    "minedtime INT,"
    "mediantxfee DECIMAL(12,3),"
    "avgContractFee BIGINT,"
    "avgContractGas INT,"
    "min50 INT,"

    "ETHpriceUSD DECIMAL(10,3),"
    "ETHpriceEUR DECIMAl(10,3),"
    "ETHpriceGBP DECIMAL(10,3),"
    "ETHpriceCNY DECIMAL(10,3),"
    
    "cat1gasTotTx INT,"
    "cat1gasMeanDelay DECIMAL(8,3),"
    "cat1gasMedianDelay INT,"
    "cat1gasMedianTime INT,"
    "cat1gas5Delay INT,"
    "cat1gas5DelayTime INT,"
    "cat1gas95Delay INT,"
    "cat1gas95DelayTime INT,"

    "cat2gasTotTx INT,"
    "cat2gasMeanDelay DECIMAL(8,3),"
    "cat2gasMedianDelay INT,"
    "cat2gasMedianTime INT,"
    "cat2gas5Delay INT,"
    "cat2gas5DelayTime INT,"
    "cat2gas95Delay INT,"
    "cat2gas95DelayTime INT,"

    "cat3gasTotTx INT,"
    "cat3gasMeanDelay DECIMAL(8,3),"
    "cat3gasMedianDelay INT,"
    "cat3gasMedianTime INT,"
    "cat3gas5Delay INT,"
    "cat3gas5DelayTime INT,"
    "cat3gas95Delay INT,"
    "cat3gas95DelayTime INT,"


    "cat4gasTotTx INT,"
    "cat4gasMeanDelay DECIMAL(8,3),"
    "cat4gasMedianDelay INT,"
    "cat4gasMedianTime INT,"
    "cat4gas5Delay INT,"
    "cat4gas5DelayTime INT,"
    "cat4gas95Delay INT,"
    "cat4gas95DelayTime INT,"

    "cat5gasTotTx INT,"
    "cat5gasMeanDelay DECIMAL(8,3),"
    "cat5gasMedianDelay INT,"
    "cat5gasMedianTime INT,"
    "cat5gas5Delay INT,"
    "cat5gas5DelayTime INT,"
    "cat5gas95Delay INT,"
    "cat5gas95DelayTime INT,"

    "miner1name TEXT,"
    "miner1pctTot DECIMAL(5,3),"
    "miner1pctEmp DECIMAL(5,3),"
    "miner1minP  INT,"

    "miner2name TEXT,"
    "miner2pctTot DECIMAL(5,3),"
    "miner2pctEmp DECIMAL(5,3),"
    "miner2minP  INT,"

    "miner3name TEXT,"
    "miner3pctTot DECIMAL(5,3),"
    "miner3pctEmp DECIMAL(5,3),"
    "miner3minP  INT,"

    "miner4name TEXT,"
    "miner4pctTot DECIMAL(5,3),"
    "miner4pctEmp DECIMAL(5,3),"
    "miner4minP  INT,"

    "miner5name TEXT,"
    "miner5pctTot DECIMAL(5,3),"
    "miner5pctEmp DECIMAL(5,3),"
    "miner5minP  INT,"

    "miner6name TEXT,"
    "miner6pctTot DECIMAL(5,3),"
    "miner6pctEmp DECIMAL(5,3),"
    "miner6minP  INT,"

    "miner7name TEXT,"
    "miner7pctTot DECIMAL(5,3),"
    "miner7pctEmp DECIMAL(5,3),"
    "miner7minP  INT,"

    "miner8name TEXT,"
    "miner8pctTot DECIMAL(5,3),"
    "miner8pctEmp DECIMAL(5,3),"
    "miner8minP  INT,"

    "miner9name TEXT,"
    "miner9pctTot DECIMAL(5,3),"
    "miner9pctEmp DECIMAL(5,3),"
    "miner9minP  INT,"

    "miner10name TEXT,"
    "miner10pctTot DECIMAL(5,3),"
    "miner10pctEmp DECIMAL(5,3),"
    "miner10minP  INT,"

    "cheapestTx INT,"
    "cheapestTxID TEXT,"
    "dearestTx BIGINT,"
    "dearestTxID TEXT,"
    "dearConTx BIGINT,"
    "dearConTxID TEXT,"
    "longestWait INT,"
    "longestWaitID TEXT,"

    "PRIMARY KEY (id))")
    
cursor.execute(query)

query = ("CREATE TABLE transactions (txHash VARCHAR(75), toAddress VARCHAR(75), fromAddress VARCHAR(75), postedBlock INT, gasPrice INT, gasPriceCat INT, gasOffered INT, tsPosted INT, PRIMARY KEY(txHash))")

cursor.execute(query)

query = ("CREATE TABLE minedtransactions (txHash VARCHAR(75), minedBlock int, toAddress VARCHAR(50), fromAddress VARCHAR(50), miner text, minedGasPrice INT, minedGasPriceCat INT, gasused INT, blockGasUsed INT, blockGasLimit INT, tsMined INT, emptyBlock BOOLEAN, PRIMARY KEY(txHash))")

cursor.execute(query)
'''
query = ("CREATE TABLE votes ("
        "id INT NOT NULL AUTO_INCREMENT,"
        "miner TEXT,"
        "blockNum INT,"
        "vote TEXT,"
        "priorLimit INT,"
        "gasLimit INT,"
        "gasused INT,"
        "priorGasused INT,"
        "PRIMARY KEY (id))")

cursor.execute(query)




cursor.close()
cnx.close()