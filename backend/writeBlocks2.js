//This script writes a single block and its transactions and its uncles to mysql

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
var ts = parseInt(process.argv[3]);



processBlock(blockNumber);

function processBlock(block)
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
            console.log(result2.blockFee);
            connection.query('INSERT INTO speedo2 SET ?', [result2], function(err, out)
            {
                iterUncs();

            })
            
        }
    }

    function processTx(txObj, num)
    {
        console.log(num);
        var gasPrice = txObj.gasPrice.toString(10);
        gasPrice = gasPrice/1e9; //convert to Gwei
        var gasPriceCat = getGasPriceCat(gasPrice);
        var txReceipt = web3.eth.getTransactionReceipt(txObj.hash);
        fee = txReceipt.gasUsed * gasPrice;
        console.log(fee);
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
            closeUp();
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
            console.log(result2);
            iterTxs(0, 0);    

        })
        
    }
    else
    {
        iterTxs(0, 0);
    }
    
    
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

function closeUp (block)
{
    connection.end();
}