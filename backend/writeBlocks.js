var Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
var mysql = require('mysql');


var blockNumber = process.argv[2];
var result2 = {};
var result4 = {};
result2.blockFee = 0;
result = web3.eth.getBlock(blockNumber, true)

var uncsReported = result.uncles.length;
result2.main = 1;
result2.uncle = 0;
result2.speed = result.gasUsed/result.gasLimit;
result2.numTx = result.transactions.length;
result2.blockNum = result.number;
result2.blockHash = result.hash;
result2.miner = result.miner;
result2.gasUsed = result.gasUsed;
result2.uncsReported = uncsReported;
result2.gasLimit = result.gasLimit
for (x=0; x<result.transactions.length; x++)
{   
    var gasPrice = result.transactions[x].gasPrice.toString(10);
    gasPrice = gasPrice/1e9; //convert to Gwei
    hash = result.transactions[x].hash;
    var tx = web3.eth.getTransactionReceipt(hash);
    fee = tx.gasUsed * gasPrice;
    result2.blockFee = result2.blockFee+(fee/1e4);
}

if (uncsReported>0)
{
    for(y=0; y<uncsReported; y++)
    {
        var result3 = web3.eth.getUncle(blockNumber, y)
        {
            result4.main = 0;
            result4.uncle = 1;
            result4.blockNum = result3.number;
            result4.blockHash = result3.hash;
            result4.miner = result3.miner;
            result4.gasUsed = result3.gasUsed;
            result4.gasLimit = result3.gasLimit;
            result4.includedBlockNum = blockNumber;
            writeBlock(result4);
        }

    }


}

writeBlock(result2);

function writeBlock(dict)
{
    var connection = mysql.createConnection({
    host:'localhost',
    user: 'ethgas',
    password: 'station',
    database: 'tx'
    });
    connection.query('INSERT IGNORE INTO speedo2 SET ?', [dict], function(err, result)
    {
        if (err)
        {
            console.error(err.stack);
        }
    })
    connection.end();
}




