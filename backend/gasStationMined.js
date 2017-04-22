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
  if (err) {
    console.error('error connecting: ' + err.stack);
    return;
  }
  console.log('connected as id ' + connection.threadId);
});

var blockCounter=0;

var filter = web3.eth.filter('latest');
filter.watch(function(err,blockHash) {
    if (err){
        console.error(err);
    }
    web3.eth.getBlock(blockHash, function (err, block) {
        if (err){
            console.error(err.stack);
            return;
        }
        var ts = Math.round(+new Date()/1000);
        if (block != null){     
            for(x=0; x <block.transactions.length; x++){
                web3.eth.getTransaction(block.transactions[x], function (err, tx){
                    if (err){
                    console.error(err.stack);
                    return;}

                    if (tx !=null){
                        var gasPrice = tx.gasPrice.toString(10);
                        gasPrice = gasPrice/1000000000;
                        if (gasPrice < 10){
                        var gasPriceCat =1;}
                        else if (gasPrice >= 10 && gasPrice <20){
                        gasPriceCat=2;}
                        else if (gasPrice === 20 ){
                        gasPriceCat= 3;}
                        else if (gasPrice >20 && gasPrice <=30){
                        gasPriceCat= 4;}
                        else if (gasPrice >30){
                        gasPriceCat= 5;}
                    
                        

                    web3.eth.getTransactionReceipt(tx.hash, function (err, receipt){
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
                            };
                
                        
                        
                        connection.query('INSERT IGNORE INTO minedtransactions SET ?', post, function(err,result){
                            if (err){
                                console.error(err.stack);}
                            gasPriceCat=null;
                            gasPrice=null;
                        });
                    }
                });
                }
                         
            });
        };
        if (block.transactions.length ===0){
            var postEmpty = {
                txHash:block.number,
                minedBlock:block.number,
                miner:block.miner,
                blockGasUsed: block.gasUsed,
                blockGasLimit: block.gasLimit,
                tsMined: ts,
                emptyBlock:true
            }
            connection.query('INSERT IGNORE INTO minedtransactions SET ?', postEmpty, function(err,result){
                if (err){
                    console.error(err.stack);}
            });

        }
        blockCounter++;
        console.log(web3.eth.blockNumber);
      };
    });
});




