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
  if (err)
  {
    console.error('error connecting: ' + err.stack);
    return;
  }
  console.log('connected as id ' + connection.threadId);
});

validationStatus = {};
watchedTx = [];
blockFees = {};
blockFeeArray = [];

try {
    fs.readFileSync(path.join(__dirname, '..', '/json/validated.json'), 'utf8')
        validationStatus = JSON.parse(data);
        console.log(validationStatus);
    }

catch (e) {
    console.log("Transaction watch list not available");
}


var blockCounter=0;
var txCounter=0;
var filter = web3.eth.filter('latest');
var filter2 = web3.eth.filter('pending');


function lastValid (txHash, gasPrice, postedBlock, minedBlock)
{
    this.txHash = txHash;
    this.gasPrice = gasPrice;
    this.postedBlock = postedBlock;
    this.minedBlock = minedBlock;
}


filter.watch(function(err,blockHash)
{
    if (err){
        console.error(err);
    }
    web3.eth.getBlock(blockHash, function (err, block)
    {
        if (err){
            console.error(err.stack);
            return;
        }
        if (block != null)
        {
            var ts = Math.round(+new Date()/1000);
            if (block.transactions.length === 0)
            {
                var post = {
                    txHash: block.number,
                    minedBlock: block.number,
                    miner: block.miner,
                    tsMined: ts,
                    emptyBlock: true
                }
                writeData(post, 'minedtransactions');

            }
            else
            {   
                for(x=0; x <block.transactions.length; x++)
                {
                    web3.eth.getTransaction(block.transactions[x], function (err, tx)
                    {
                        if (err)
                        {
                            console.error(err.stack);
                            return;
                        }

                        if (tx !=null)
                        {
                            var gasPrice = tx.gasPrice.toString(10);
                            gasPrice = gasPrice/1e9; //convert to Gwei
                            var gasPriceCat = getGasPriceCat(gasPrice);
                            
                            web3.eth.getTransactionReceipt(tx.hash, function (err, receipt)
                            {
                                if (err)
                                {
                                    console.error(err.stack);
                                }
                                if (receipt != null){ 
                                    var post = {
                                        txHash: receipt.transactionHash,
                                        minedBlock: receipt.blockNumber,
                                        toAddress:receipt.to,
                                        fromAddress:receipt.from,
                                        gasused: receipt.gasUsed,
                                        miner: block.miner,
                                        blockGasUsed: block.gasUsed,
                                        blockGasLimit: block.gasLimit,
                                        minedGasPrice:gasPrice,
                                        minedGasPriceCat:gasPriceCat,
                                        tsMined: ts,
                                        emptyBlock:false
                                    }
                            
                                    writeData(post, 'minedtransactions');
                                    
                                }
                                
                            });
                        }
                    });
                }
            }
            
            blockCounter++;
            console.log(block.number);
            currentBlock = block.number;
            writeBlock = currentBlock - 5;
            commandString = 'node writeBlocks.js ' + writeBlock;
            launchProcess(commandString);
            if (block.number % 100 === 0 )
            {
                startQuery = currentBlock - 5760;
                commandString = 'node gasStationAnalyze.js ' + currentBlock;
                commandString2 = 'python gascalc.py ' + startQuery + ' ' +  currentBlock;
                launchProcess (commandString);
                launchProcess (commandString2); 
            
             }
             if (block.number % 1000 === 0 )
            {
                profitBlock = currentBlock - 100000;
                commandString = 'python miner.py ' + profitBlock + ' ' + currentBlock;
            }
            if (block.number % 50 === 0 )
            {

                var y = watchedTx.length;
                var last = false;
                for (var x = 0; x < y; x++ )
                {
                    if (x === (y-1))
                    {
                        last = true;
                    }
                    tx = watchedTx.shift();
                    validateTx(tx, block.number, last);
                }               
            }
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
                if (err)
                { 
                    console.error(err.stack);
                    return;
                }

                if (result != null)
                {    
                    var gasPrice = result.gasPrice.toString(10);
                    gasPrice = gasPrice/1e9;
                    var gasPriceCat = getGasPriceCat(gasPrice);
                    
                    var post2 = {
                        txHash: txHash,
                        postedBlock: blockNum,
                        gasOffered: result.gas,
                        gasPrice: gasPrice,
                        gasPriceCat: gasPriceCat,
                        tsPosted: ts2
                    }
                    
                    
                    writeData(post2, 'transactions');
                    if (gasPrice < 20)
                    {
                        watchedTx.push(post2);
                    }
                }
        
            });
        })
                
        txCounter++;
        console.log(txCounter);
    }

});


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
            

    
function getGasPriceCat (gasPrice)
{   
    var gasPriceCat;

    if (gasPrice < 10){
        gasPriceCat =1;}
    else if (gasPrice >= 10 && gasPrice <20){
        gasPriceCat=2;}
    else if (gasPrice === 20 ){
        gasPriceCat= 3;}
    else if (gasPrice >20 && gasPrice <=30){
        gasPriceCat= 4;}
    else if (gasPrice >30){
        gasPriceCat= 5;}
    
    return gasPriceCat;
}        

function launchProcess (commandString)
{
    console.log(commandString);
    const exec = require('child_process').exec;
    const child = exec(commandString);
}     

function validateTx (tx, blockNum, last)
{
    var currentBlock = blockNum;
    var txCheck = tx;
    var last = last;
    web3.eth.getTransactionReceipt(txCheck.txHash, function(err, result)
    {
        if (err)
        {
            console.error(err.stack);
            return;
        }
        if (result != null)
        {
            var lastValidTx = new lastValid (txCheck.txHash, txCheck.gasPrice, txCheck.postedBlock, result.blockNumber);
            lastValidTx['mined'] = true;
            lastValidTx['miner'] = result.miner;
            txCheck.gasPrice = Math.round(txCheck.gasPrice);
            validationStatus[txCheck.gasPrice] = lastValidTx;
        }
        else
        {
            if (txCheck.postedBlock >= currentBlock - 50)
            {
                watchedTx.push(txCheck);
            }
            else
            {
                var lastValidTx = new lastValid (txCheck.txHash, txCheck.gasPrice, txCheck.postedBlock);
                lastValidTx['mined'] = false;
                txCheck.gasPrice = Math.round(txCheck.gasPrice);
                validationStatus[txCheck.gasPrice] = lastValidTx;
            }
            
        }
        if (last)
        {
            var str = JSON.stringify(validationStatus);
            console.log(str);
            fs.writeFile(path.join(__dirname, '..', '/json/validated.json'), str, (err) => {
                if (err)
                {
                    console.log(err.stack)
                }
            })
        }       
    })

}

