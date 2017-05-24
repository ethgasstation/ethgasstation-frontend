var Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

var hash = process.argv[2];

web3.eth.getBlock(hash, function(err, result){
    if (err){
        console.log(err);
    }
    if (result){
        result.main = 1;
        result.uncle = 0;
        delete result.logsBloom;
        delete result.transactionsRoot;
        delete results.transactions;

        var json = JSON.stringify(result);
        console.log(json);
    }
    if (!result){
        web3.getUncle(hash, function(err, result2){
            if (err){
                console.log(err);
            }
            if (result2){
                result2.uncle = 1;
                result2.main = 0;
                var json2= JSON.stringify(result2);
                console.log(json2);
            }
        })
    }
});
