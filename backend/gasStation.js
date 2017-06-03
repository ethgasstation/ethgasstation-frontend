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
blockTime = {};

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
    var ts = Math.round(+new Date()/1000);
    web3.eth.getBlock(blockHash, function (err, block)
    {
        if (!(block.number in blockTime))
        {
            blockTime[block.number]=ts;
        }
        writeBlock = block.number - 5;
        deleteBlock = block.number - 25;
        if (writeBlock in blockTime)
        {
            processBlock(writeBlock, blockTime[writeBlock]);

        }  
        if (deleteBlock in blockTime)
        {
            delete blockTime[deleteBlock];
        }
        blockCounter++;
        console.log(block.number);
        currentBlock = block.number;
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
            commandString = 'python miner4.py ' + profitBlock + ' ' + currentBlock;
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
    });
});



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

function processBlock(block, ts)
{

    function iterTxs(num, txFee)
    {
        
        if (result2.numTx == 0)
        {
            var post = 
            {
                txHash: result.number,
                minedBlock: result.number,
                miner: result.miner,
                emptyBlock: true,
                tsMined: ts,
                emptyBlock: true
            }
            connection.query('INSERT INTO minedtransactions SET ?', [post], function(err, out)
            {
                if (err)
                {
                    console.log(err);
                }
                iterUncs();

            })
            
        }
        else if (num < result2.numTx)
        {
            result2.blockFee = result2.blockFee + (txFee/1e4);
            processTx(result.transactions[num], num, result2.blockFee);

        }
        else
        {
            result2.blockFee = result2.blockFee + (txFee/1e4);
            connection.query('INSERT INTO speedo2 SET ?', [result2], function(err, out)
            {
                iterUncs();

            })
            
        }
    }

    function processTx(txObj, num)
    {
        var gasPrice = txObj.gasPrice.toString(10);
        gasPrice = gasPrice/1e9; //convert to Gwei
        var gasPriceCat = getGasPriceCat(gasPrice);
        var txReceipt = web3.eth.getTransactionReceipt(txObj.hash);
        fee = txReceipt.gasUsed * gasPrice;
        var post = 
        {
            txHash: txObj.hash,
            minedBlock: txObj.blockNumber,
            toAddress:txObj.to,
            fromAddress:txObj.from,
            gasused: txReceipt.gasUsed,
            miner: result2.miner,
            minedGasPrice:gasPrice,
            minedGasPriceCat:gasPriceCat,
            tsMined: ts,
            emptyBlock:false
        }
        connection.query('INSERT INTO minedtransactions SET ?', [post], function(err, out)
        {
            if (err)
            {
                    console.log(err);
            }
            num++;
            iterTxs(num, fee);
        })
    }

    function iterUncs()
    {
        if (result2.uncsReported==0)
        {
            closeUp(result2.blockNum);
        }
        else if (result2.uncsReported==1)
        {
            processUncle(result2.blockNum, 0, closeUp)
        }
        else if (result2.uncsReported==2)
        {
            processUncle(result2.blockNum, 0, nextUncle)
        }
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

    function nextUncle(block)
    {
        processUncle(block, 1, closeUp);
    }


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
    result2.gasLimit = result.gasLimit;
    if (result2.numTx == 0)
    {
        result2.blockFee = 0;
        connection.query('INSERT INTO speedo2 SET ?', [result2], function(err, out)
        {
            if (err)
            {
                console.log(err);
            }
            iterTxs(0, 0);    

        })
        
    }
    else
    {
        iterTxs(0, 0);
    }
    
    
}

function closeUp (block)
{
    console.log('finished ' + block);
}
