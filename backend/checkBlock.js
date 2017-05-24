var Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

var hash = process.argv[2];
var result2 = {};

web3.eth.getBlock(hash, function(err, result){
    if (err){
        console.log(err);
    }
    if (result){
        var uncsReported = result.uncles.length;
        result2.main = 1;
        result2.uncle = 0;
        result2.blockNum = result.number;
        result2.hash = result.hash;
        result2.miner = result.miner;
        result2.gasUsed = result.gasUsed;
        result2.uncsReported = uncsReported;
        var json = JSON.stringify(result2);
        console.log(json);
    }
});
