CREATE TABLE transactions (txHash VARCHAR(75), postedBlock INT, gasPrice INT, gasPriceCat INT, gasOffered INT, tsPosted INT,
PRIMARY KEY(txHash));

CREATE TABLE minedtransactions (txHash VARCHAR(75), minedBlock int, toAddress VARCHAR(50), fromAddress VARCHAR(50),
miner text, minedGasPrice INT, minedGasPriceCat INT, gasused INT, blockGasUsed INT, blockGasLimit INT, tsMined INT, emptyBlock BOOLEAN, PRIMARY KEY(txHash));

CREATE TABLE speedo (id INT NOT NULL AUTO_INCREMENT, blockNum INT, avgWait INT, speed DECIMAL(3,3), numTx INT, PRIMARY KEY (id));

CREATE TABLE txDataLast10k (
    id INT NOT NULL AUTO_INCREMENT,
    latestblockNum INT,
    startSelect INT,
    rowsChanged INT,
    totalBlocks INT,
    emptyBlocks INT,
    fullBlocks INT,

    totalTx INT,
    totalTransfers INT,
    totalConCalls INT,
    totalTimed INT,

    avgGasUsed DECIMAL(8,3),
    maxMinedGasPrice INT,
    minMinedGasPrice INT,
    medianGasPrice INT,
    maxMineDelay INT,
    minMineDelay INT,
    meanMineDelay DECIMAL(8,3),
    medianMinedDelay INT,
    medianTime INT,
    mine5delay INT,
    mine5delayTime INT,
    mine95delay INT,
    mine95delaytime INT,
    minedtime INT,
    mediantxfee DECIMAL(12,3),
    avgContractFee BIGINT,
    avgContractGas INT,
    min50 INT,

    ETHpriceUSD DECIMAL(5,3),
    ETHpriceEUR DECIMAl(5,3),
    ETHpriceGBP DECIMAL(5,3),
    ETHpriceCNY DECIMAL(5,3),
    
    cat1gasTotTx INT,
    cat1gasMeanDelay DECIMAL(8,3),
    cat1gasMedianDelay INT,
    cat1gasMedianTime INT,
    cat1gas5Delay INT,
    cat1gas5DelayTime INT,
    cat1gas95Delay INT,
    cat1gas95DelayTime INT,

    cat2gasTotTx INT,
    cat2gasMeanDelay DECIMAL(8,3),
    cat2gasMedianDelay INT,
    cat2gasMedianTime INT,
    cat2gas5Delay INT,
    cat2gas5DelayTime INT,
    cat2gas95Delay INT,
    cat2gas95DelayTime INT,

    cat3gasTotTx INT,
    cat3gasMeanDelay DECIMAL(8,3),
    cat3gasMedianDelay INT,
    cat3gasMedianTime INT,
    cat3gas5Delay INT,
    cat3gas5DelayTime INT,
    cat3gas95Delay INT,
    cat3gas95DelayTime INT,


    cat4gasTotTx INT,
    cat4gasMeanDelay DECIMAL(8,3),
    cat4gasMedianDelay INT,
    cat4gasMedianTime INT,
    cat4gas5Delay INT,
    cat4gas5DelayTime INT,
    cat4gas95Delay INT,
    cat4gas95DelayTime INT,

    cat5gasTotTx INT,
    cat5gasMeanDelay DECIMAL(8,3),
    cat5gasMedianDelay INT,
    cat5gasMedianTime INT,
    cat5gas5Delay INT,
    cat5gas5DelayTime INT,
    cat5gas95Delay INT,
    cat5gas95DelayTime INT,

    miner1name TEXT,
    miner1pctTot DECIMAL(5,3),
    miner1pctEmp DECIMAL(5,3),
    miner1minP  INT,

    miner2name TEXT,
    miner2pctTot DECIMAL(5,3),
    miner2pctEmp DECIMAL(5,3),
    miner2minP  INT,

    miner3name TEXT,
    miner3pctTot DECIMAL(5,3),
    miner3pctEmp DECIMAL(5,3),
    miner3minP  INT,

    miner4name TEXT,
    miner4pctTot DECIMAL(5,3),
    miner4pctEmp DECIMAL(5,3),
    miner4minP  INT,

    miner5name TEXT,
    miner5pctTot DECIMAL(5,3),
    miner5pctEmp DECIMAL(5,3),
    miner5minP  INT,

    miner6name TEXT,
    miner6pctTot DECIMAL(5,3),
    miner6pctEmp DECIMAL(5,3),
    miner6minP  INT,

    miner7name TEXT,
    miner7pctTot DECIMAL(5,3),
    miner7pctEmp DECIMAL(5,3),
    miner7minP  INT,

    miner8name TEXT,
    miner8pctTot DECIMAL(5,3),
    miner8pctEmp DECIMAL(5,3),
    miner8minP  INT,

    miner9name TEXT,
    miner9pctTot DECIMAL(5,3),
    miner9pctEmp DECIMAL(5,3),
    miner9minP  INT,

    miner10name TEXT,
    miner10pctTot DECIMAL(5,3),
    miner10pctEmp DECIMAL(5,3),
    miner10minP  INT,

    cheapestTx INT,
    cheapestTxID TEXT,
    dearestTx BIGINT,
    dearestTxID TEXT,
    dearConTx BIGINT,
    dearConTxID TEXT,
    longestWait INT,
    longestWaitID TEXT,

    PRIMARY KEY (id)
);

CREATE TABLE txDataLast100b (
    id INT NOT NULL AUTO_INCREMENT,
    latestblockNum INT,
    startSelect INT,
    ethConsumedLast100 BIGINT,
    medianDelayLast100 DECIMAL(5,3),
    PRIMARY KEY (id)
);

CREATE USER 'ethgas'@'localhost' IDENTIFIED BY 'station';

GRANT ALL PRIVILEGES ON tx.* TO 'ethgas'@'localhost';

FLUSH PRIVILEGES;








    
