//This script writes a range of blocks and their uncles into speedo table

var Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
var mysql = require('mysql');
var connection = mysql.createConnection({
    host:'localhost',
    user: 'ethgas',
    password: 'station',
    database: 'tx'
});



var blockNumber = parseInt(process.argv[2]);
if (typeof process.argv[3])
{
    toBlock = parseInt(process.argv[3]);
}
if (!toBlock){
    toBlock = parseInt(blockNumber);
}

numBlocks = toBlock - blockNumber;
console.log(numBlocks);
processBlock(blockNumber, nextBlock);

function processBlock(block, callBack)
{
    var result2 = {};
    result2.blockFee = 0;
    var result = web3.eth.getBlock(block, true)
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
    console.log(result2);
    connection.query('INSERT INTO speedo2 SET ?', [result2], function(err, sql){
        callBack(result2.blockNum, result2.uncsReported);
    })
    
}

function processUncle(block, pos, callBack)
{
    var result4 = {};
    var result3 = web3.eth.getUncle(block, pos);
    result4.main = 0;
    result4.uncle = 1;
    result4.blockNum = result3.number;
    result4.blockHash = result3.hash;
    result4.miner = result3.miner;
    result4.gasUsed = result3.gasUsed;
    result4.gasLimit = result3.gasLimit;
    result4.includedBlockNum = block;
    console.log(result4);
    connection.query('INSERT INTO speedo2 SET ?', [result4], function(err, result){
        callBack(result4.includedBlockNum);
    })
    
}

function closeUp (block)
{
    console.log('finished '+ block);
    connection.end();
}
function nextUncle(block)
{
    processUncle(block, 1, nextBlock);
}

function nextBlock(block, uncsReported)
{
    if (uncsReported == 1)
    {
        processUncle(block, 0, nextBlock);
    }
    else if (uncsReported == 2)
    {
        processUncle(block, 0, nextUncle);
    }
    else
    {
        var next = block + 1;
        if (next > toBlock)
        {
            closeUp(block);
        }
        else
        {
            processBlock(next, nextBlock);
        }

    }
    

}


