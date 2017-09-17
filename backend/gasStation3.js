//Monitor pending transactions and mined blocks- post data to MySQL
//Also montior low gas price transactions to alert if they aren't mined

var Web3 = require('web3');
var mysql = require('mysql');
const fs = require('fs');
var path = require('path');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
var connection = mysql.createConnection({
    host:'localhost',
    user: 'ethgas',
    password: 'station',
    database: 'tx'
});

connection.connect(function(err) {
  if (err){
    console.error('error connecting: ' + err.stack);
    return;
  }
  console.log('connected as id ' + connection.threadId);
});


blockTime = {};
blockQueue = [];
processing = false;
var blockCounter=0;
var txCounter=0;

var filter = web3.eth.filter('latest');
var filter2 = web3.eth.filter('pending');


filter.watch(function(err,blockHash){
    if (err){
        console.error(err);
        return;
    }
    var ts = Math.round(+new Date()/1000);

    web3.eth.getBlock(blockHash, true, function (err, block){
        if (!block){
            return;
        }
        console.log("\nreceived block number " + block.number);
        if (!(block.number in blockTime)){
            blockTime[block.number]=ts;
            blockQueue.push(block);
            getTxPool(block.number);
        }

    })
})

filter2.watch(function(err, txHash)
{
    if (err)
    {
        console.error(err.stack);
        return;
    }
    var txHash = txHash;
    if (txHash != null)
    {
        
        var ts2 = Math.round(+new Date()/1000);
        
        web3.eth.getBlockNumber(function (err,blockNum)
        {
            if (err)
            {
                console.log(err.stack);
            }
            var blockNum = blockNum;

            web3.eth.getTransaction(txHash, function(err,result)
            {
                if (err){ 
                    console.error(err.stack);
                    return;
                }

                if (result != null){    
                    var gasPrice = result.gasPrice.toString(10);
                    gasPrice = gasPrice/1e6;
                    
                    var post2 = {
                        txHash: txHash,
                        postedBlock: blockNum,
                        gasOffered: result.gas,
                        gasPrice: gasPrice,
                        tsPosted: ts2,
                        toAddress: result.to,
                        fromAddress: result.from
                    }
                    writeData(post2, 'transactions');
                }
        
            });
        })
                
        txCounter++;
        process.stdout.write(txCounter + ' ');
    }

});

function manageBlocks (blockNum){
    blockNum--;
    if ((blockNum % 100 === 0) && (!processing)){
        procesing = true;
        startBlock = blockNum - 2500;
        processStats(startBlock, blockNum);
    }
    if ((blockQueue[0]['number'] <= blockNum) && (!processing)){
        console.log("\nblock queue length = " + blockQueue.length);
        processing = true;
        var blockObj = blockQueue.shift();
        console.log("now processing block " + blockObj.number)
        getReceipts(0, blockObj)
        if (blockQueue[0]['number'] <= blockNum){
            console.log("\nblock queue length = " + blockQueue.length);  
            var blockObj = blockQueue.shift();
            console.log("catching up- processing block " + blockObj.number)
            getReceipts(0, blockObj)
        }
    }
    
}


function processStats (start, end){
    var end = end;
    commandString = 'python gascalc4.py ' + start + ' ' +  end;
    console.log("\n"+ commandString);
    const exec = require('child_process').exec;
    const child = exec(commandString, function(){
        if (end % 1000 === 0){
            var start = end-100000;
            processMinerProfit(start, end);
        }
        else{
            processing = false;
        }
    });
}

function processMinerProfit (start, end){
    commandString= 'python miner4.py ' + start + ' ' + end;
    console.log("\n"+ commandString);
    const exec = require('child_process').exec;
    const child = exec(commandString, function(){
        processing = false;
    });
}


function processTxPool (blockNum){
    var blockNum = blockNum;
    time = blockTime[blockNum];
    commandString = 'python mempool5.py '+ blockNum + ' ' + time;
    console.log("\n" + commandString);
    const exec = require('child_process').exec;
    const child = exec(commandString, function(){
        manageBlocks(blockNum);
    });
}


function getTxPool(blockNum){
    var prevBlock = blockNum - 1;
    commandString = 'python txpool2.py ' + blockNum;
    console.log("\n" + commandString);
    const exec = require('child_process').exec;
    const child = exec(commandString, function(){
        processTxPool(prevBlock);
    });
}


       
function getReceipts(number, blockObj){
    if (number < blockObj.transactions.length){
        requestReceipt(number, blockObj.transactions[number].hash, blockObj);
    }
    else{
        processTransactions(blockObj);
    }
}
        

function requestReceipt (number, txHash, blockObj){
    receipt = web3.eth.getTransactionReceipt(txHash);
    if (receipt){
        blockObj.transactions[number].gasUsed = receipt.gasUsed;
    }
    number++;
    getReceipts(number, blockObj)
}
        
        
function processTransactions (blockObj){
    gasPriceArray = [];
    var ts = blockTime[blockObj.number];
    var blockFee = 0;
    var txPost = [];
    for (var x=0; x<blockObj.transactions.length; x++){
        gasPrice = (blockObj.transactions[x].gasPrice.toString(10))/1e6;
        gasPriceArray.push(gasPrice);
        blockFee += (gasPrice * blockObj.transactions[x].gasUsed/1e7); 
        txPost.push(
            [blockObj.transactions[x].hash, 
            blockObj.number,
            blockObj.transactions[x].to,
            blockObj.transactions[x].from,
            blockObj.miner,
            gasPrice, 
            ts,
            blockObj.transactions[x].gasUsed
        ]);
    
    }
    blockMinGasPrice = (Math.min.apply(Math,gasPriceArray));
    numTx = blockObj.transactions.length;
    if (blockObj.transactions.length > 0){
        writeTransactions(txPost);
        writeBlock (blockMinGasPrice, numTx, blockFee, blockObj);
    }
    else {
        writeBlock (null, 0, 0, blockObj);
    }
}        
        
function writeTransactions(txPost) {
    var sql = "INSERT INTO minedtransactions (txHash, minedBlock, toAddress, fromAddress, miner, minedGasPrice, tsMined, gasUsed) VALUES ?";
    connection.query(sql, [txPost], function(err, result){
        if (err){
            console.log(err.stack);
        }
        else{
            console.log("\nwrote tx for block " + txPost[0][1]);
        }
    })
}

function writeBlock (blockMinGasPrice, numTx, blockFee, blockObj){
    var sql = "INSERT INTO speedo2 (blockNum, gasUsed, miner, uncle, main, gasLimit, numTx, speed, blockFee, blockHash, minGasPrice, uncsReported) VALUES (?)";
    speed = blockObj.gasUsed/blockObj.gasLimit;
    blockFee = Math.round(blockFee);
    blockPost = [blockObj.number, blockObj.gasUsed, blockObj.miner, 0, 1, blockObj.gasLimit, numTx, speed, blockFee, blockObj.hash, blockMinGasPrice, blockObj.uncles.length];
    connection.query(sql, [blockPost], function(err, result){
        if (err){
            console.log(err.stack);
        }
        else{
            console.log("\nwrote block data for block " + blockObj.number);
        }
    })
    if (blockObj.uncles.length > 0){
        getUncles(0, 0, blockObj)
    }
    else{
        processing = false;

    }
    
}

function getUncles(number, cycle, blockObj){
    uncle = web3.eth.getUncle(blockObj.number, number);
    if (uncle){
        writeUncle(uncle, cycle, blockObj);
    }
}

function writeUncle (uncle, cycle, blockObj){
    var sql = "INSERT INTO speedo2 (blockNum, gasUsed, miner, uncle, main, gasLimit, blockHash, includedBlockNum) VALUES (?)";

    unclePost = [uncle.number, uncle.gasUsed, uncle.miner, 1, 0, uncle.gasLimit, uncle.hash, blockObj.number];

    connection.query(sql, [unclePost], function(err, result){
        if (err){
            console.log(err.stack);
        }
        else{
            console.log("\n wrote uncle for block " + blockObj.number);
        }
    })
    cycle += 1;
    if ((blockObj.uncles.length > 1) && (cycle < 2)){
        getUncles(1, cycle, blockObj);
    }
    else{
        processing = false;
    }

}       



function writeData (post, table)
{   
    connection.query('INSERT IGNORE INTO ?? SET ?', [table, post], function(err, result)
    {
        if (err)
        {
            console.error(err.stack);
        }
    })
}
            

    




