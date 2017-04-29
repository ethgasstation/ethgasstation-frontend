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

function postObject(){};


filter.watch(function(err,blockHash)
{
    if (err){
        console.error(err);
    }
    var post = new postObject();
    web3.eth.getBlock(blockHash, function (err, block)
    {
        if (err){
            console.error(err.stack);
            return;
        }
        if (block != null)
        {
            post['tsMined'] = Math.round(+new Date()/1000);
            post['miner'] = block.miner;
            post['blockGasUsed'] = block.gasUsed;
            post['blockGasLimit'] = block.gasLimit;
            post['minedBlock'] = block.number;

            if (block.transactions.length === 0)
            {
                post['txHash'] = block.number;
                post['emptyBlock'] = true;
                writeData(post, 'minedtransactions');

            }
            else
            {   
                post['emptyBlock'] = false;
                for(x=0; x <block.transactions.length; x++)
                {
                    console.log("loop " + x)
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
                            post['minedGasPrice'] = gasPrice;
                            post['minedGasPriceCat'] = gasPriceCat;
                            post['fromAddress'] = tx.from;
                            post['toAddress'] = tx.to;
                            post['txHash'] = tx.hash;
                        
                    
                            web3.eth.getTransactionReceipt(tx.hash, function (err, receipt)
                            {
                                console.log("loop2 " + x)
                                if (err)
                                {
                                    console.error(err.stack);
                                }
                                if (receipt != null){  
                                    console.log("loop3 " + x)
                                    post['gasused'] = receipt.gasUsed;
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
                //commandString3 = 'python getPrice.py';
                launchProcess (commandString);
                launchProcess (commandString2);
                //launchProcess (commandString3);  
            
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
    
    var post2 = new postObject();

    if (txHash != null)
    {
        post2['txHash'] = txHash;
        post2['tsPosted'] = Math.round(+new Date()/1000);
        
        web3.eth.getBlockNumber(function (err,blockNum)
        {
            if (err)
            {
                console.log(err.stack);
            }
            post2['postedBlock'] = blockNum;
        })

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
                    post2['gasPrice'] = gasPrice/1e9;
                    post2['gasPriceCat'] = getGasPriceCat(post2['gasPrice']);
                    post2['gasOffered'] = result.gas;
                    writeData(post2, 'transactions');
            }
        
        });
                
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

                
    