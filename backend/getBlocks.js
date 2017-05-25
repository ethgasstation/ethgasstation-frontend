var Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

var hash = process.argv[2];
var result2 = {};
var blockFee = 0;
result = web3.eth.getBlock(hash, true)

var uncsReported = result.uncles.length;
result2.main = 1;
result2.uncle = 0;
result2.blockNum = result.number;
result2.hash = result.hash;
result2.miner = result.miner;
result2.gasUsed = result.gasUsed;
result2.uncsReported = uncsReported;
result2.gasLimit = result.gasLimit
for (x=0; x<result.transactions.length; x++)
{   
    var gasPrice = result.transactions[x].gasPrice.toString(10);
    gasPrice = gasPrice/1e9; //convert to Gwei
    var tx = web3.eth.getTransactionReceipt(hash);
    fee = tx.gasUsed * gasPrice;
    blockFee = blockFee+fee;
}
result2.blockFee = blockFee;
var json = JSON.stringify(result2);
console.log(json);



