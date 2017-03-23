<?php
//setting header to json
//header('Content-Type: application/json');

//database
define('DB_HOST', '127.0.0.1');
define('DB_USERNAME', 'ethgas');
define('DB_PASSWORD', 'station');
define('DB_NAME', 'tx');

//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

if(!$mysqli){
	die("Connection failed: " . $mysqli->error);
}

//query to get data from the table

$query = "SELECT * FROM txDataLast10k ORDER BY id DESC LIMIT 1";
$result = $mysqli->query($query);
$row = $result->fetch_assoc();

if ($row['medianMinedDelay'] == null)
{
	$query = "SELECT * FROM txDataLast10k ORDER BY id DESC LIMIT 2,1";
	$result= makeQuery($mysqli,$query);
}

$graphData = array();
$query2 = "SELECT * FROM txDataLast100b ORDER BY id DESC LIMIT 20";
$result2 = $mysqli->query($query2);

while ($row2 = $result2->fetch_assoc()){
	array_push($graphData,$row2);
}

$x1 = $graphData[19]['latestblockNum'];
$x2 = $graphData[18]['latestblockNum'];
$x3 = $graphData[17]['latestblockNum'];
$x4 = $graphData[16]['latestblockNum'];
$x5 = $graphData[15]['latestblockNum'];
$x6 = $graphData[14]['latestblockNum'];
$x7 = $graphData[13]['latestblockNum'];
$x8 = $graphData[12]['latestblockNum'];
$x9 = $graphData[11]['latestblockNum'];
$x10 = $graphData[10]['latestblockNum'];
$x11 = $graphData[9]['latestblockNum'];
$x12 = $graphData[8]['latestblockNum'];
$x13 = $graphData[7]['latestblockNum'];
$x14 = $graphData[6]['latestblockNum'];
$x15 = $graphData[5]['latestblockNum'];
$x16 = $graphData[4]['latestblockNum'];
$x17 = $graphData[3]['latestblockNum'];
$x18 = $graphData[2]['latestblockNum'];
$x19 = $graphData[1]['latestblockNum'];
$x20 = $graphData[0]['latestblockNum'];

//convert to ETH from gwei and divide by 100 to get average per block over last 100 blocks

$ya1 = round($graphData[19]['ethConsumedLast100']/100000000000,2);
$ya2 = round($graphData[18]['ethConsumedLast100']/100000000000,2);
$ya3 = round($graphData[17]['ethConsumedLast100']/100000000000,2);
$ya4 = round($graphData[16]['ethConsumedLast100']/100000000000,2);
$ya5 = round($graphData[15]['ethConsumedLast100']/100000000000,2);
$ya6 = round($graphData[14]['ethConsumedLast100']/100000000000,2);
$ya7 = round($graphData[13]['ethConsumedLast100']/100000000000,2);
$ya8 = round($graphData[12]['ethConsumedLast100']/100000000000,2);
$ya9 = round($graphData[11]['ethConsumedLast100']/100000000000,2);
$ya10 = round($graphData[10]['ethConsumedLast100']/100000000000,2);
$ya11 = round($graphData[9]['ethConsumedLast100']/100000000000,2);
$ya12 = round($graphData[8]['ethConsumedLast100']/100000000000,2);
$ya13 = round($graphData[7]['ethConsumedLast100']/100000000000,2);
$ya14 = round($graphData[6]['ethConsumedLast100']/100000000000,2);
$ya15 = round($graphData[5]['ethConsumedLast100']/100000000000,2);
$ya16 = round($graphData[4]['ethConsumedLast100']/100000000000,2);
$ya17 = round($graphData[3]['ethConsumedLast100']/100000000000,2);
$ya18 = round($graphData[2]['ethConsumedLast100']/100000000000,2);
$ya19 = round($graphData[1]['ethConsumedLast100']/100000000000,2);
$ya20 = round($graphData[0]['ethConsumedLast100']/100000000000,2);


$yb1 = round($graphData[19]['meanDelayLast100'],2);
$yb2 = round($graphData[18]['meanDelayLast100'],2);
$yb3 = round($graphData[17]['meanDelayLast100'],2);
$yb4 = round($graphData[16]['meanDelayLast100'],2);
$yb5 = round($graphData[15]['meanDelayLast100'],2);
$yb6 = round($graphData[14]['meanDelayLast100'],2);
$yb7 = round($graphData[13]['meanDelayLast100'],2);
$yb8 = round($graphData[12]['meanDelayLast100'],2);
$yb9 = round($graphData[11]['meanDelayLast100'],2);
$yb10 = round($graphData[10]['meanDelayLast100'],2);
$yb11 = round($graphData[9]['meanDelayLast100'],2);
$yb12 = round($graphData[8]['meanDelayLast100'],2);
$yb13 = round($graphData[7]['meanDelayLast100'],2);
$yb14 = round($graphData[6]['meanDelayLast100'],2);
$yb15 = round($graphData[5]['meanDelayLast100'],2);
$yb16 = round($graphData[4]['meanDelayLast100'],2);
$yb17 = round($graphData[3]['meanDelayLast100'],2);
$yb18 = round($graphData[2]['meanDelayLast100'],2);
$yb19 = round($graphData[1]['meanDelayLast100'],2);
$yb20 = round($graphData[0]['meanDelayLast100'],2);


$latestblock = $row['latestblockNum'];
$ethprice = $row['ETHpriceUSD'];
$mediantxfee = $row['mediantxfee'];
$medianfeeusd = $ethprice * $mediantxfee / 1000000000;
settype($medianfeeusd, "float");
$medianwaitsec = $row['medianTime'];
$medianwaitblock = $row['medianMinedDelay'];
$gaspricehigh = $row['maxMinedGasPrice'];
$gaspricelow = $row['minMinedGasPrice'];
$gaspricemedian = $row['medianGasPrice'];

$cheapestTx = $row['cheapestTx'];
$cheapestTxId= $row['cheapestTxID'];
$dearestTx = $row['dearestTx'];
$dearestTxId = $row['dearestTxID'];
$dearestCon = $row['dearConTx'];
$dearestConId = $row['dearConTxID'];
$longestWait = $row['longestWait'];
$longestWaitId = $row['longestWaitID'];

$cheapestTxUsd = $cheapestTx * $ethprice / 1000000000;
setlocale(LC_MONETARY, "en_US.UTF-8");
$cheapUSD = money_format('%.4n', $cheapestTxUsd);
$dearestTxUsd = $dearestTx * $ethprice / 1000000000;
$dearUSD = money_format('%.2n', $dearestTxUsd);
$dearestConUsd = $dearestCon * $ethprice / 1000000000;
$dearconUSD = money_format('%.2n', $dearestConUsd);

$longestWait = round($longestWait/3600,1);

$totTx = $row['totalTx'];


$cat1Tx = $row['cat1gasTotTx'];
$cat1TimeMed = $row['cat1gasMedianTime'];
$cat1Time95 = $row['cat1gas95DelayTime'];

$cat2Tx = $row['cat2gasTotTx'];
$cat2TimeMed = $row['cat2gasMedianTime'];
$cat2Time95 = $row['cat2gas95DelayTime'];

$cat3Tx = $row['cat3gasTotTx'];
$cat3TimeMed = $row['cat3gasMedianTime'];
$cat3Time95 = $row['cat3gas95DelayTime'];

$cat4Tx = $row['cat4gasTotTx'];
$cat4TimeMed = $row['cat4gasMedianTime'];
$cat4Time95 = $row['cat4gas95DelayTime'];

$cat5Tx = $row['cat5gasTotTx'];
$cat5TimeMed = $row['cat5gasMedianTime'];
$cat5Time95 = $row['cat5gas95DelayTime'];

if ($cat1Tx == null)
{
	$cat1tx = 0 ;
}


$cat1TxPct = round($cat1Tx/$totTx, 4) *100;
$cat2TxPct = round($cat2Tx/$totTx, 4) *100;
$cat3TxPct = round($cat3Tx/$totTx, 4) *100;
$cat4TxPct = round($cat4Tx/$totTx, 4) *100;
$cat5TxPct = round($cat5Tx/$totTx, 4) *100;

$cat1TimeMedMin = round($cat1TimeMed/60, 1);
$cat2TimeMedMin = round($cat2TimeMed/60, 1);
$cat3TimeMedMin = round($cat3TimeMed/60, 1);
$cat4TimeMedMin = round($cat4TimeMed/60, 1);
$cat5TimeMedMin = round($cat5TimeMed/60, 1);

$cat1Time95Min = round($cat1Time95/60, 1);
$cat2Time95Min = round($cat2Time95/60, 1);
$cat3Time95Min = round($cat3Time95/60, 1);
$cat4Time95Min = round($cat4Time95/60, 1);
$cat5Time95Min = round($cat5Time95/60, 1);


$miners = array (
	array (
	'name' => $row['miner1name'],
	'pctTot' => $row['miner1pctTot'],
	'pctEmp' => $row['miner1pctEmp'],
	'minP' => $row['miner1minP']
	),

	array (
	'name' => $row['miner2name'],
	'pctTot' => $row['miner2pctTot'],
	'pctEmp' => $row['miner2pctEmp'],
	'minP' => $row['miner2minP']
	),


	array (
	'name' => $row['miner3name'],
	'pctTot' => $row['miner3pctTot'],
	'pctEmp' => $row['miner3pctEmp'],
	'minP' => $row['miner3minP']
	),

	array (
	'name' => $row['miner4name'],
	'pctTot' => $row['miner4pctTot'],
	'pctEmp' => $row['miner4pctEmp'],
	'minP' => $row['miner4minP']
	),

	array (
	'name' => $row['miner5name'],
	'pctTot' => $row['miner5pctTot'],
	'pctEmp' => $row['miner5pctEmp'],
	'minP' => $row['miner5minP']
	),

	array (
	'name' => $row['miner6name'],
	'pctTot' => $row['miner6pctTot'],
	'pctEmp' => $row['miner6pctEmp'],
	'minP' => $row['miner6minP']
	),

	array (
	'name' => $row['miner7name'],
	'pctTot' => $row['miner7pctTot'],
	'pctEmp' => $row['miner7pctEmp'],
	'minP' => $row['miner7minP']
	),

	array (
	'name' => $row['miner8name'],
	'pctTot' => $row['miner8pctTot'],
	'pctEmp' => $row['miner8pctEmp'],
	'minP' => $row['miner8minP']
	),

	array (
	'name' => $row['miner9name'],
	'pctTot' => $row['miner9pctTot'],
	'pctEmp' => $row['miner9pctEmp'],
	'minP' => $row['miner9minP']
	),

	array (
	'name' => $row['miner10name'],
	'pctTot' => $row['miner10pctTot'],
	'pctEmp' => $row['miner10pctEmp'],
	'minP' => $row['miner10minP']
	)
);


$price = array();
foreach ($miners as $key => $row)
{
	$price[$key] = $row['minP'];
	$empty[$key] = $row['pctEmp'];
}

array_multisort($price, SORT_ASC, $empty, SORT_ASC, $miners);

function recPrice ($miners)
{
	$cumblocks =0;
	$x = 0;
	foreach ($miners as $key => $row)
	{
		$cumblocks += $row['pctTot'];
		if ($cumblocks > .5){
		return $miners[$x]['minP'];
		}
	$x++;
	}
}

$recPrice = recPrice($miners);
$lowPrice = $miners[0]['minP'];
$highPrice = $miners[9]['minP'];

//free memory associated with result
$result->close();

//close connection
$mysqli->close();


?>