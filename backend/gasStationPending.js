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


var txCounter = 0;


var filter = web3.eth.filter('pending');
    filter.watch(function(err, txHash) {
        if (err){
            console.error(err.stack);
            return;
        }
        if (txHash != null){
        var txHash = txHash;
        var ts = Math.round(+new Date()/1000);
        }

        else return;
    

        web3.eth.getBlockNumber(function (err,blockNum){
            if (err){
                console.log(err.stack);
            }
            var blockNum = blockNum;

            web3.eth.getTransaction(txHash, function(err,result){
                if (err){ 
                    console.error(err.stack);
                    return;}

                if (result != null){    
                    var gasPrice = result.gasPrice.toString(10);
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
                    else {gasPrice = null;}

                    var gasOffered = result.gas;
                }
                
                    var post = {txHash: txHash, postedBlock: blockNum, gasPrice: gasPrice, gasPriceCat: gasPriceCat, gasOffered: gasOffered, tsPosted: ts};
                    connection.query('INSERT IGNORE INTO transactions SET ?', post, function(err, result){
                        if (err) {
                        console.error(err.stack);}
                    });
                
                txCounter++;
                console.log(txCounter);

                
            });
        });
    });


