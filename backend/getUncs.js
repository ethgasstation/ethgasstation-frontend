var Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

var blockNumber = process.argv[2];
var numUncs = process.argv[3];
var result2 = {};

for (x=0; x<numUncs; x++)
{
    result = web3.eth.getUncle(blockNumber, x);
    result2.main = 0;
    result2.uncle = 1;
    result2.blockNum = result.number;
    result2.hash = result.hash;
    result2.miner = result.miner;
    result2.gasUsed = result.gasUsed;
    result2.gasLimit = result.gasLimit;
    result2.includedBlockNum = blockNumber;
}
var json = JSON.stringify(result2);
console.log(json);



