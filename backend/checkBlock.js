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
        delete result.transactions;

        var json = JSON.stringify(result);
        console.log(json);
    }
});
