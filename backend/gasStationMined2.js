//Monitor pending transactions and mined blocks- post data to MySQL

var Web3 = require('web3');
var mysql = require('mysql');
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

var blockCounter=0;
var txCounter=0;
var filter = web3.eth.filter('latest');
var filter2 = web3.eth.filter('pending');


watchedTx = [];

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
                console.log("emptyBlock");
                var post = {
                    txHash: block.number,
                    minedBlock: block.number,
                    miner: block.miner,
                    tsMined: ts,
                    emptyBlock: true
                }
                console.log(post);
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
                                    console.log(receipt.transactionHash);  
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
            writeSpeedo(block); //for Speedometer
            blockCounter++;
            console.log(web3.eth.blockNumber);
            currentBlock = block.number;
            startQuery = currentBlock - 10000;
            if (block.number % 100 === 0 )
            {
                commandString = 'node gasStationAnalyze2.js ' + currentBlock + ' &>output2.txt';
                commandString2 = 'python gascalc.py ' + startQuery + ' ' +  currentBlock + ' &>output3.txt';
                launchProcess (commandString);
                launchProcess (commandString2); 
            
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
                        txHash: result.txHash,
                        postedBlock: blockNum,
                        gasOffered: result.gas,
                        gasPrice: gasPrice,
                        gasPriceCat: gasPriceCat,
                        tsPosted: ts2
                    }
                    
                    }
                    writeData(post2, 'transactions');
            
        
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
            

// Data for the speedometer- written every block        
function writeSpeedo (blockObj)
{
    post3 = {};
    post3['blockNum']= blockObj.number;
    post3['speed'] = blockObj.gasUsed / blockObj.gasLimit;
    writeData (post3, 'speedo');
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
    const child = exec(commandString, (error, stdout, stderr) => 
    {
        if (error)
        {
            throw error;
        }
        console.log(stdout);
    })
}

                
    