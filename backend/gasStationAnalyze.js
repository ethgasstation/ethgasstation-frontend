//Open connections

var https = require('https');
var mysql = require('mysql');
var connection = mysql.createConnection({
    host:'localhost',
    user: 'ethgas',
    password: 'station',
    database: 'tx'
});
connection.connect(function(err) {
    if (err) {
        console.error('error connecting: ' + err.stack);}
});


// define Query Interval

var toBlock = process.argv[2];
var startSelect = toBlock - 10000;
var start2 = toBlock - 100;

//post is the global object that will be used to write to new database
var post={};
var post2={};
var post3={};

post['latestBlockNum']=toBlock;
post['startSelect']=startSelect;
post2['latestBlockNum']=toBlock;
post2['startSelect']=start2;
       

//keep database from getting too large

var pruneBlock = toBlock - 30000;

if (toBlock % 5000 === 0)
{
    databasePrune('transactions', 'postedBlock', pruneBlock);
    databasePrune('minedtransactions', 'minedBlock', pruneBlock);
    databasePrune('speedo', 'blockNum', pruneBlock);    
    databasePrune('txDataLast10k', 'latestblockNum', pruneBlock);
    databasePrune('txDataLast100b', 'latestblockNum', pruneBlock);
}  

//Miner Names
var minerTable = {
    '0xea674fdde714fd979de3edf0f56aa9716b898ec8':'Ethermine',
    '0x1e9939daaad6924ad004c2560e90804164900341':'ethfans',
    '0xb2930b35844a230f00e51431acae96fe543a0347':'miningpoolhub',
    '0x4bb96091ee9d802ed039c4d1a5f6216f90f81b01':'Ethpool',
    '0x52bc44d5378309ee2abf1539bf71de1b7d7be3b5':'Nanopool',
    '0x2a65aca4d5fc5b5c859090a6c34d164135398226':'Dwarfpool',
    '0x61c808d82a3ac53231750dadc13c777b59310bd9':'f2pool',
    '0xa42af2c70d316684e57aefcc6e393fecb1c7e84e':'Coinotron',
    '0x6c7f03ddfdd8a37ca267c88630a4fee958591de0':'alpereum'

};

//start Queries

startClean(startSelect,toBlock);
startDiscrete(start2,toBlock);


// Database maintenance

function databasePrune (tableName, colName, deleteBlock) {

        connection.query('DELETE from ?? WHERE (?? < ?)', [tableName, colName, deleteBlock], function (err,result){
            if (err){
            console.error(err.stack);}

        });

         connection.query('DELETE from minedtransactions WHERE minedblock is null', function (err,result){
            if (err){
            console.error(err.stack);}

        });

        connection.query('DELETE from transactions WHERE postedblock is null', function (err,result){
            if (err){
            console.error(err.stack);}

        });

        
};

//Queries that set Post object for database write

function startClean (startSelect,toBlock) {
    connection.query('UPDATE transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash SET transactions.postedBlock = null WHERE (minedtransactions.minedBlock - transactions.postedBlock)<=0', [startSelect,toBlock], function (err, result){

        if(err){
            console.error(err.stack);
        }
        post['changedRows']=result.changedRows;

        avgMineTimeCat(1,startSelect,toBlock,avgMineTimeCat)
        console.log('1');

    
    });

}


//Average time from post to mine by category
function avgMineTimeCat (y, startSelect, toBlock, callback){

    connection.query('SELECT AVG (minedtransactions.minedBlock - transactions.postedBlock) as avg FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > ? AND transactions.postedBlock < ? AND transactions.gasPriceCat = ?', [startSelect,toBlock, y], function (err, result){

        if (err){
            console.error(err.stack);}

        post['avgCatTx'+y]=result[0]['avg'];

        y++;

        if (y < 6){
            callback(y, startSelect,toBlock, avgMineTimeCat);
        }
        else {
            calcTotMineTime(startSelect,toBlock); //wait for loop to finish
            console.log('2');

        }
    });
}



//Average time from post to mine overall
function calcTotMineTime (startSelect, toBlock){
 
    connection.query('SELECT AVG (minedtransactions.minedBlock - transactions.postedBlock) as avg FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > ? AND transactions.postedBlock < ?', [startSelect,toBlock], function (err, result){

        if (err){
            console.error(err.stack);}

    
        post['avgMineDelay']=result[0]['avg'];

        totalTimed(startSelect, toBlock);
        console.log('3');
    
    });
}

//Total Number of Tx Timed By Node
function totalTimed (startSelect, toBlock){
 
    connection.query('SELECT count(minedtransactions.minedBlock - transactions.postedBlock) as count FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > ? AND transactions.postedBlock < ?', [startSelect,toBlock], function (err, result){

        if (err){
            console.error(err.stack);}

    
        post['totalTimed']=result[0]['count'];

        calcCatTx(1,startSelect, toBlock,calcCatTx);
        console.log('4');
    
    });
}

//Number of transactions by Gas Price category
function calcCatTx (y, startSelect, toBlock, callback){
 
    connection.query('SELECT COUNT(*) as num FROM minedtransactions WHERE minedblock > ? AND minedblock < ? AND minedGasPriceCat =? AND emptyblock = FALSE', [startSelect,toBlock, y], function (err, result){

        if (err){
            console.error(err.stack);}
        
        post['totalCatTx'+y]=result[0]['num'];
                
        y++;

        if (y < 6){
            callback(y, startSelect, toBlock, calcCatTx);
        }
        else {
            calcTotTx(startSelect,toBlock); //wait for loop to finish
            console.log('5');

        }
    });
 }


//Total number of transactions
function calcTotTx (startSelect, toBlock){
    connection.query('SELECT COUNT(*) as num FROM minedtransactions WHERE minedblock > ? AND minedblock < ? AND emptyBlock = FALSE', [startSelect,toBlock], function (err, result){

        if (err){
            console.error(err.stack);}
        
        post['totalTx']=result[0]['num'];
        calcTotTransfers(startSelect,toBlock);
        console.log('6');
                
        
    });
}

//Total number of transfers
function calcTotTransfers (startSelect, toBlock){
    connection.query('SELECT COUNT(*) as num FROM minedtransactions WHERE minedblock > ? AND minedblock < ? AND gasused = 21000', [startSelect,toBlock], function (err, result){

        if (err){
            console.error(err.stack);}
        
        post['totalTransfers']=result[0]['num'];
        calcTotConCalls(startSelect,toBlock);
        console.log('7');
                
        
    });
}

//Total number of contract calls
function calcTotConCalls (startSelect, toBlock){
    connection.query('SELECT COUNT(*) as num FROM minedtransactions WHERE minedblock > ? AND minedblock < ? AND gasused != 21000 AND gasused IS NOT NULL', [startSelect,toBlock], function (err, result){

        if (err){
            console.error(err.stack);}
        
        post['totalConCalls']=result[0]['num'];

        maxMin('MinedGasPrice', startSelect,toBlock);
        console.log('8');
                
        
    });
}



//Max and min gas price mined
function maxMin (col, startSelect, toBlock) {
   connection.query('SELECT MAX(??) as max FROM minedtransactions WHERE minedblock > ? AND minedblock < ?', [col,startSelect,toBlock], function (err, result){

        if (err){
            console.error(err.stack);}
        
        post['max'+col]=result[0]['max'];


    connection.query('SELECT MIN(??) as min FROM minedtransactions WHERE minedblock > ? AND minedblock < ?', [col,startSelect,toBlock], function (err, result){

        if (err){
            console.error(err.stack);}
        
    
        post['min'+col]=result[0]['min'];
                
        medianGasPrice (startSelect,toBlock);
        console.log('9');    
        
    });
   });

}

function medianGasPrice (startSelect, toBlock){
    connection.query('SELECT minedgasprice FROM minedtransactions WHERE minedblock> ? and minedblock <? and minedgasprice IS NOT NULL ORDER BY minedgasprice ASC', [startSelect, toBlock],function (err, result){

        if (err){
            console.error(err.stack);}

        var numRows = result.length;
        var midPoint = Math.floor(numRows/2);

        post.medianGasPrice = result[midPoint]['minedgasprice'];
        console.log('10');
        maxMineDelay (startSelect, toBlock);


    })
}

//Max and min blocks from post to mine
function maxMineDelay (startSelect,toBlock){
    connection.query('SELECT MAX (minedtransactions.minedBlock - transactions.postedBlock) as max FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > ? AND transactions.postedBlock < ?', [startSelect, toBlock], function (err, result){

        if (err){
            console.error(err.stack);}

        post['maxMineDelay']=result[0]['max'];


    connection.query('SELECT MIN (minedtransactions.minedBlock - transactions.postedBlock) as min FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > ? AND transactions.postedBlock < ?', [startSelect,toBlock], function (err, result){

        if (err){
            console.error(err.stack);}

    
        post['minMineDelay']=result[0]['min'];

        medianPctlDelay (startSelect, toBlock);
        console.log('11');

    });
 });
}

// Median /Percentile Blocks/time from post to mine all transactions

function medianPctlDelay (startSelect, toBlock){


    connection.query('SELECT (minedtransactions.minedBlock - transactions.postedBlock) as delay FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock IS NOT NULL AND transactions.postedBlock > ? AND transactions.postedBlock < ? ORDER BY delay ASC', [startSelect,toBlock], function (err, result){
        
        if (err){ 
            console.error(err.stack);
        }
        var numRows = result.length;
        var midPoint = Math.floor(numRows/2);
        var pctl95 = Math.floor(numRows * .95);
        var pctl5 = Math.floor(numRows * .05);

        post.medianDelay = result[midPoint]['delay'];
        post.delay95 = result[pctl95]['delay'];
        post.delay5 = result[pctl5]['delay'];

        medianPctlDelayTime (startSelect,toBlock);
        console.log('12');

    });
}
function medianPctlDelayTime (startSelect, toBlock){


    connection.query('SELECT (minedtransactions.tsMined - transactions.tsPosted) as time FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.tsPosted IS NOT NULL AND transactions.postedBlock > ? AND transactions.postedBlock < ? ORDER BY time ASC', [startSelect,toBlock], function (err, result){
        
        if (err){ 
            console.error(err.stack);
        }
        var numRows = result.length;
        var midPoint = Math.floor(numRows/2);
        var pctl95 = Math.floor(numRows * .95);
        var pctl5 = Math.floor(numRows * .05);

        post.medianTime = result[midPoint]['time'];
        post.delay95time = result[pctl95]['time'];
        post.delay5time = result[pctl5]['time'];

        medianPctlDelayCat(1,startSelect,toBlock,medianPctlDelayCat);
        console.log('13');

    });
}


//Median/percentile time from post to mine by Gas Price category
function medianPctlDelayCat (y, startSelect, toBlock, callback){   
   
    connection.query('SELECT (minedtransactions.minedBlock - transactions.postedBlock) as delay FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock IS NOT NULL AND transactions.postedBlock > ? AND transactions.postedBlock < ? AND transactions.gasPriceCat = ? ORDER BY delay ASC',[startSelect, toBlock, y], function (err, result){


        if (err){
            console.error(err.stack);}  
        
        if (result.length===0){
            post['medianDelayCat'+y] = null;
            post['delay95Cat'+y] = null;
            post['delay5Cat'+y] = null;
        }

        else if (result.length ===1){
            post['medianDelayCat'+y] = result[0]['delay'];
            post['delay95Cat'+y] = result[0]['delay'];
            post['delay5Cat'+y] = result[0]['delay'];

        }
            
        else {
            var numRows = result.length;
            var midPoint = Math.floor(numRows/2);
            var pctl95 = Math.floor(numRows * .95);
            var pctl5 = Math.ceil(numRows * .05);

            post['medianDelayCat'+y] = result[midPoint]['delay'];
            post['delay95Cat'+y] = result[pctl95]['delay'];
            post['delay5Cat'+y] = result[pctl5]['delay'];

        }
        y++;
        if (y<6){
            callback (y, startSelect, toBlock, medianPctlDelayCat);
            }
        else {
            medianPctlDelayCatTime(1,startSelect,toBlock,medianPctlDelayCatTime);
            console.log('14');
        }
        

    });

};

function medianPctlDelayCatTime (y, startSelect, toBlock, callback){   
   
    connection.query('SELECT (minedtransactions.tsMined - transactions.tsPosted) as time FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.tsPosted IS NOT NULL AND transactions.postedBlock > ? AND transactions.postedBlock < ? AND transactions.gasPriceCat = ? ORDER BY time ASC',[startSelect, toBlock, y], function (err, result){


        if (err){
            console.error(err.stack);}  
        
        if (result.length===0){
            post['medianDelayCatTime'+y] = null;
            post['delay95CatTime'+y] = null;
            post['delay5CatTime'+y] = null;
        }

        else if (result.length ===1){

            post['medianDelayCatTime'+y] = result[0]['time'];
            post['delay95CatTime'+y] = result[0]['time'];
            post['delay5CatTime'+y] = result[0]['time'];
        }
            
        else {
            var numRows = result.length;
            var midPoint = Math.floor(numRows/2);
            var pctl95 = Math.floor(numRows * .95);
            var pctl5 = Math.ceil(numRows * .05);

            post['medianDelayCatTime'+y] = result[midPoint]['time'];
            post['delay95CatTime'+y] = result[pctl95]['time'];
            post['delay5CatTime'+y] = result[pctl5]['time'];

        }
        y++;
        if (y<6){
            callback (y, startSelect, toBlock, medianPctlDelayCatTime);
            }
        else {
            countAllBlocks(startSelect,toBlock);
            console.log('15');
        }
        

    });

};

//Miner analysis: Number of blocks/emptyblocks by top miners, min price accepted

function getTopMiners (startSelect, toBlock, totalBlocksInDataset){
    
    connection.query('SELECT miner, COUNT(DISTINCT (minedBlock)) AS cnt FROM minedtransactions WHERE minedBlock > ? AND minedBlock < ? GROUP BY miner ORDER BY cnt DESC LIMIT 10 ', [startSelect,toBlock], function (err, result){

        if (err){
            console.error(err.stack);
        }
        if (result.length < 10)
        {
            avgGasUsed(startSelect,toBlock);
        }
        for (var x=0; x<result.length; x++){
            
            var minerId = result[x]['miner'];

            var totalBlocksFromMiner = result[x]['cnt'];
            var percentMinerOfTotal = totalBlocksFromMiner/totalBlocksInDataset;

            if (minerTable[minerId]){
                var minerName = minerTable[minerId];
            }
            else {
                minerName = minerId; 
            }

            post['miner'+x]=minerName;
            post['pctTot'+x] = percentMinerOfTotal; //Percent of total blocks mined by top 10 miner
            getMinerEmptyBlock (startSelect,toBlock,minerId,x,totalBlocksFromMiner);
        }
    });
}

function getMinerEmptyBlock (startSelect,toBlock,minerId,x,totalBlocksFromMiner){
   
    connection.query('SELECT COUNT(DISTINCT (minedBlock)) AS cnt2 FROM minedtransactions WHERE minedBlock > ? AND minedBlock < ? AND miner = ? AND emptyBlock = TRUE', [startSelect,toBlock,minerId], function (err,result){

                if (err){
                    console.error(err.stack);
                }
                var emptyBlocksFromMiner = result[0]['cnt2'];
                var percentOfMinerEmpty = emptyBlocksFromMiner/totalBlocksFromMiner;
        
                post['pctEmp'+x] = percentOfMinerEmpty; //Percent of miner's blocks that are empty
                getMinerMinPrice (startSelect,toBlock,minerId,x);

    });
}
    
function getMinerMinPrice (startSelect,toBlock,minerId,x){

    connection.query('SELECT miner, MIN (minedGasPrice) as minprice FROM minedtransactions WHERE minedBlock > ? AND minedBlock < ? AND miner = ? AND emptyBlock = FALSE', [startSelect,toBlock,minerId], function (err,result){
                
        if (err){
            console.error(err.stack);
        }
        var minPrice = result[0]['minprice'];
       
        post['minp'+x] = minPrice;//Lowest Price accepted by miner;
        if (x==9){
            avgGasUsed(startSelect,toBlock);
            console.log('16a');
        }

    });
}
    

function countAllBlocks(startSelect,toBlock){

    connection.query('SELECT COUNT(DISTINCT(minedBlock)) AS cnt FROM minedtransactions WHERE minedBlock > ? AND minedBlock < ?', [startSelect,toBlock], function (err,result2){
        if (err){
            console.error(err.stack);
        }
        post['totalBlocksInDataset']= result2[0]['cnt'];  //should equal toBlock-startSelect

        getTopMiners(startSelect,toBlock,result2[0]['cnt']);
        console.log('16b');

    });


};

//Average gas used in transactions overall

function avgGasUsed (startSelect,toBlock){
    connection.query('SELECT AVG(gasused) as avg FROM minedtransactions WHERE minedblock > ? AND minedblock < ?', [startSelect,toBlock], function (err, result){
        if (err){
            console.error(err.stack);
        }

        post['avgGasUsed']=result[0]['avg'];

        cheapestStdTx(startSelect, toBlock);
        

        console.log('17');

    });

}

//Cheapest/MostExpensive StdTx

function cheapestStdTx (startSelect, toBlock) {
    connection.query('SELECT txhash, (gasused*minedGasPrice) as cheap FROM minedtransactions WHERE minedblock > ? and minedblock < ? and gasused = 21000 ORDER BY cheap ASC LIMIT 1', [startSelect, toBlock], function (err, result){

        if (err){
            console.error(err.stack);
        }

            post['cheapTx']=result[0]['cheap'];
            post['cheapTxID']= result[0]['txhash'];

            dearestStdTx(startSelect, toBlock);

            console.log('18');
        });
}

function dearestStdTx (startSelect, toBlock) {
    connection.query('SELECT txhash, (gasused*minedGasPrice) as dear FROM minedtransactions WHERE minedblock > ? and minedblock < ? and gasused = 21000 ORDER BY dear DESC LIMIT 1', [startSelect, toBlock], function (err, result){

        if (err){
            console.error(err.stack);
        }
    

        post['dearTx']=result[0]['dear']
        post['dearTxID']= result[0]['txhash'];

        highestFee(startSelect, toBlock);

        console.log('19');

        });


}

function highestFee (startSelect, toBlock) {
    connection.query('SELECT txhash, (gasused*minedGasPrice) as dear FROM minedtransactions WHERE minedblock > ? and minedblock < ? ORDER BY dear DESC LIMIT 1', [startSelect, toBlock], function (err, result){

        if (err){
            console.error(err.stack);
        }

            post['dearConTx']=result[0]['dear'];
            post['dearConTxID']= result[0]['txhash'];

            longestWait(startSelect, toBlock);

            console.log('20');
        });
}

function longestWait (startSelect, toBlock) {
    connection.query('SELECT minedtransactions.txhash, (minedtransactions.tsMined - transactions.tsPosted) as wait FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > ? AND transactions.postedBlock < ? ORDER BY wait desc LIMIT 1', [startSelect, toBlock], function (err, result){

        if (err){
            console.error(err.stack);
        }

        post['longWait']=result[0]['wait'];
        post['longWaitID']= result[0]['txhash'];

        console.log('21');
        
        avgMinedTime(startSelect, toBlock); //everything should be in post
    });
}

function avgMinedTime (startSelect, toBlock) {
    connection.query('SELECT avg(tsMined - tsPosted) as time FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > ? AND transactions.postedBlock < ?', [startSelect, toBlock], function (err, result){
        if (err){
            console.error(err.stack);
        }
        post['minedtime'] = result[0]['time'];
        console.log('22');

        medianTransferFee(startSelect, toBlock);
    });

}

function medianTransferFee (startSelect, toBlock) {
    connection.query('SELECT (gasused*minedgasprice) as fee FROM minedtransactions WHERE gasused = 21000 AND minedblock > ? AND minedblock <? AND minedgasprice IS NOT NULL ORDER BY fee ASC', [startSelect , toBlock], function (err, result){

    if (err){
            console.error(err.stack);
    }

    var numRows = result.length;
    var midPoint = Math.ceil(numRows/2);

    post['medianTxFee'] = result[midPoint]['fee'];
    console.log('23');

    medContractFee(startSelect, toBlock);

    });

}

function medContractFee (startSelect, toBlock) {
    connection.query('SELECT (gasused*minedgasprice) as fee FROM minedtransactions WHERE gasused > 21000 AND minedblock > ? AND minedblock <? AND minedgasprice IS NOT NULL AND gasused IS NOT NULL', [startSelect , toBlock], function (err, result){

    if (err){
            console.error(err.stack);
    }

    var numRows = result.length;
    var midPoint = Math.ceil(numRows/2);

    post['avgContractFee'] = result[midPoint]['fee'];
    console.log('24');

    medContractGas(startSelect, toBlock);

    });

}

function medContractGas (startSelect, toBlock) {
    connection.query('SELECT gasused as gas FROM minedtransactions WHERE gasused > 21000 AND minedblock > ? AND minedblock <? AND gasused IS NOT NULL', [startSelect , toBlock], function (err, result){

    if (err){
            console.error(err.stack);
    }
    var numRows = result.length;
    var midPoint = Math.ceil(numRows/2);

    post['avgContractGas'] = result[midPoint]['gas'];
    console.log('25');

    min50(startSelect, toBlock);

    });

}

//minimum gas price with at least 50 transactions mined
function min50 (startSelect, toBlock){
    connection.query('SELECT minedgasprice from minedtransactions WHERE minedblock > ? AND minedblock <? AND minedgasprice IS NOT NULL ORDER BY minedgasprice ASC LIMIT 50', [startSelect , toBlock], function (err, result){
        
        if (err){
            console.error(err.stack);
        }
    
        post['min50'] = result[49]['minedgasprice'];
        console.log('26');
        countEmpty (startSelect, toBlock);
        
    });

}

//Count empty blocks
function countEmpty (startSelect, toBlock){
    connection.query('SELECT COUNT(*) as cnt FROM minedtransactions WHERE minedblock > ? AND minedblock <? and emptyBlock = 1', [startSelect , toBlock], function (err, result){
        
        if (err){
            console.error(err.stack);
        }
    
        post['emptyBlocks'] = result[0]['cnt'];
        console.log('27');
        countFull(startSelect, toBlock);
    });
}
function countFull (startSelect, toBlock){
    connection.query('SELECT speed FROM speedo WHERE blockNum > ? AND blockNum <? and speed >0.99', [startSelect , toBlock], function (err, result){
        
        if (err){
            console.error(err.stack);
        }
    
        post['fullBlocks'] = result[0]['speed'];
        console.log('28');
        getETHprice();
    });
}


function getETHprice (){

   var options = {
    hostname: 'min-api.cryptocompare.com',
    path: '/data/price?fsym=ETH&tsyms=USD,EUR,GBP,CNY',
    method: 'GET'};


const req = https.request(options, (res) =>{
    res.setEncoding('utf8');
    var str = "";
    res.on('data', (chunk) => {
        str += chunk;
    })
    res.on('end', () => {
        var pricej = JSON.parse(str);
        post['priceUSD'] = pricej['USD'];
        post['priceEUR'] = pricej['EUR'];
        post['priceCNY'] = pricej['CNY'];
        post['priceGBP'] = pricej['GBP'];
        console.log('29');
        errorCheck('txData');
    }) 

})

req.on('error', (e) => {
    console.log(`problem with request: ${e.message}`);
    }); 

req.end();
}

function startDiscrete (start2,toBlock){

    connection.query('SELECT SUM (gasused * minedGasPrice) as eth FROM minedtransactions WHERE minedBlock > ? AND minedBlock < ?', [start2,toBlock], function (err,result2){
        if (err){
            console.error(err.stack);
        }
        
        post2['ethConsumedLast100']= result2[0]['eth'];

        getMedianDelay(start2,toBlock);
        console.log('a')
    });
}

function getMedianDelay(start2,toBlock){

    connection.query('SELECT (minedtransactions.tsMined-transactions.tsPosted) AS delay FROM transactions INNER JOIN minedtransactions ON transactions.txHash = minedtransactions.txHash WHERE transactions.postedBlock > ? AND transactions.postedBlock < ? AND transactions.tsPosted IS NOT NULL ORDER BY delay ASC', [start2,toBlock], function (err,result2){
        if (err){
            console.error(err.stack);
        }

        var numRows = result2.length;
        var midPoint = Math.ceil(numRows/2);

        if (result2.length>2)
        {
            post2['medianDelayLast100']= result2[midPoint]['delay'];
        }
        errorCheck('last100b');
        console.log('b');
      
    });

};

   

function errorCheck(table){
    if (table ==='txData')
    {
        if (post.emptyBlocks === null || post.avgGasUsed === null || post.medianTime === null)
        {
            return;
        }
        else 
        {
            writeData10k();
        }

    }
    else if (table === 'last100b')
    {
        if (post.ethConsumedLast100 === null)
        {
            return
        }
        else
        {
            writeData100b();
        }
    }
    
}

function writeData10k () {

 var cleanPost = {
    latestblockNum:post.latestBlockNum,
    startSelect:post.startSelect,
    rowsChanged:post.changedRows,
    totalBlocks:post.totalBlocksInDataset,
    emptyBlocks:post.emptyBlocks,
    fullBlocks:post.fullBlocks,

    totalTx: post.totalTx,
    totalTimed: post.totalTimed,
    totalTransfers: post.totalTransfers,
    totalConCalls: post.totalConCalls,

    avgGasUsed: post.avgGasUsed,
 
    maxMinedGasPrice: post.maxMinedGasPrice,
    minMinedGasPrice: post.minMinedGasPrice,
    medianGasPrice: post.medianGasPrice,
    maxMineDelay: post.maxMineDelay,
    minMineDelay: post.minMineDelay,
    meanMineDelay: post.avgMineDelay,
    medianMinedDelay: post.medianDelay,
    medianTime: post.medianTime,
    mine5delay: post.delay5,
    mine5delaytime: post.delay5time,
    mine95delay: post.delay95,
    mine95delaytime: post.delay95time,
    minedtime: post.minedtime,
    medianTxFee: post.medianTxFee,
    avgContractFee: post.avgContractFee,
    avgContractGas: post.avgContractGas,
    min50: post.min50,
    
    ETHpriceUSD: post.priceUSD,
    ETHpriceEUR: post.priceEUR,
    ETHpriceCNY: post.priceCNY,
    ETHpriceGBP: post.priceGBP,


    cat1gasTotTx: post.totalCatTx1, 
    cat1gasMeanDelay: post.avgCatTx1, 
    cat1gasMedianDelay: post.medianDelayCat1,
    cat1gasMedianTime: post.medianDelayCatTime1,
    cat1gas5Delay: post.delay5Cat1,
    cat1gas5DelayTime: post.delay5CatTime1,
    cat1gas95Delay: post.delay95Cat1,
    cat1gas95DelayTime: post.delay95CatTime1,

    cat2gasTotTx: post.totalCatTx2, 
    cat2gasMeanDelay: post.avgCatTx2, 
    cat2gasMedianDelay: post.medianDelayCat2,
    cat2gasMedianTime: post.medianDelayCatTime2,
    cat2gas5Delay: post.delay5Cat2,
    cat2gas5DelayTime: post.delay5CatTime2,
    cat2gas95Delay: post.delay95Cat2,
    cat2gas95DelayTime: post.delay95CatTime2,

    cat3gasTotTx: post.totalCatTx3, 
    cat3gasMeanDelay: post.avgCatTx3, 
    cat3gasMedianDelay: post.medianDelayCat3,
    cat3gasMedianTime: post.medianDelayCatTime3,
    cat3gas5Delay: post.delay5Cat3,
    cat3gas5DelayTime: post.delay5CatTime3,
    cat3gas95Delay: post.delay95Cat3,
    cat3gas95DelayTime: post.delay95CatTime3,

    cat4gasTotTx: post.totalCatTx4, 
    cat4gasMeanDelay: post.avgCatTx4, 
    cat4gasMedianDelay: post.medianDelayCat4,
    cat4gasMedianTime: post.medianDelayCatTime4,
    cat4gas5Delay: post.delay5Cat4,
    cat4gas5DelayTime: post.delay5CatTime4,
    cat4gas95Delay: post.delay95Cat4,
    cat4gas95DelayTime: post.delay95CatTime4,

    cat5gasTotTx: post.totalCatTx5, 
    cat5gasMeanDelay: post.avgCatTx5, 
    cat5gasMedianDelay: post.medianDelayCat5,
    cat5gasMedianTime: post.medianDelayCatTime5,
    cat5gas5Delay: post.delay5Cat5,
    cat1gas5DelayTime: post.delay5CatTime5,
    cat5gas95Delay: post.delay95Cat5,
    cat5gas95DelayTime: post.delay95CatTime5,

    miner1name: post.miner0,
    miner1pctTot: post.pctTot0,
    miner1pctEmp: post.pctEmp0,
    miner1minP: post.minp0,

    miner2name: post.miner1,
    miner2pctTot: post.pctTot1,
    miner2pctEmp: post.pctEmp1,
    miner2minP: post.minp1,

    miner3name: post.miner2,
    miner3pctTot: post.pctTot2,
    miner3pctEmp: post.pctEmp2,
    miner3minP: post.minp2,

    miner4name: post.miner3,
    miner4pctTot: post.pctTot3,
    miner4pctEmp: post.pctEmp3,
    miner4minP: post.minp3,

    miner5name: post.miner4,
    miner5pctTot: post.pctTot4,
    miner5pctEmp: post.pctEmp4,
    miner5minP: post.minp4,

    miner6name: post.miner5,
    miner6pctTot: post.pctTot5,
    miner6pctEmp: post.pctEmp5,
    miner6minP: post.minp5,

    miner7name: post.miner6,
    miner7pctTot: post.pctTot6,
    miner7pctEmp: post.pctEmp6,
    miner7minP: post.minp6,

    miner8name: post.miner7,
    miner8pctTot: post.pctTot7,
    miner8pctEmp: post.pctEmp7,
    miner8minP: post.minp7,

    miner9name: post.miner8,
    miner9pctTot: post.pctTot8,
    miner9pctEmp: post.pctEmp8,
    miner9minP: post.minp8,

    miner10name: post.miner9,
    miner10pctTot: post.pctTot9,
    miner10pctEmp: post.pctEmp9,
    miner10minP: post.minp9,

    cheapestTx: post.cheapTx,
    cheapestTxID: post.cheapTxID,
    dearestTx: post.dearTx,
    dearestTxID: post.dearTxID,
    dearConTx: post.dearConTx,
    dearConTxID: post.dearConTxID,
    longestWait: post.longWait,
    longestWaitID: post.longWaitID

 }


 connection.query('INSERT IGNORE INTO txDataLast10k SET ?', cleanPost, function(err,result){
        if (err){
            console.error(err.stack);}
        
        post = {};
 });

 connection.end();


};


function writeData100b () {

connection.query('INSERT IGNORE INTO txDataLast100b SET ?', post2, function(err,result){
        if (err){
            console.error(err.stack);}
        
        post2 = {};
 });


}

function writeSpeedo (blockObj){
    // Data for the speedometer- written every block

    post3['blockNum']= blockObj.number;
    post3['speed'] = blockObj.gasUsed / blockObj.gasLimit;

    connection.query('INSERT IGNORE INTO speedo SET ?', post3, function(err, result){
        if (err){
            console.error(err.stack);}
            post3={};

        })
}

