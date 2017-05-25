var Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

var tx = process.argv[2];

var receipt = web3.eth.getTransaction(tx);
console.log(receipt);
