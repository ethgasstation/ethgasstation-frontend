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

$graphData = array();
$query2 = "SELECT * FROM txDataLast100b ORDER BY id DESC LIMIT 11";
$result2 = $mysqli->query($query2);

while ($row2 = $result2->fetch_assoc()){
	array_push($graphData,$row2);
}

$x1 = $graphData[10]['latestblockNum'];
$x2 = $graphData[9]['latestblockNum'];
$x3 = $graphData[8]['latestblockNum'];
$x4 = $graphData[7]['latestblockNum'];
$x5 = $graphData[6]['latestblockNum'];
$x6 = $graphData[5]['latestblockNum'];
$x7 = $graphData[4]['latestblockNum'];
$x8 = $graphData[3]['latestblockNum'];
$x9 = $graphData[2]['latestblockNum'];
$x10 = $graphData[1]['latestblockNum'];
$x11 = $graphData[0]['latestblockNum'];


//convert to ETH from gwei (1e9) and divide by 100 to get average ETH per block over last 100 blocks

$ya1 = round($graphData[10]['ethConsumedLast100']/1e11,4);
$ya2 = round($graphData[9]['ethConsumedLast100']/1e11,4);
$ya3 = round($graphData[8]['ethConsumedLast100']/1e11,4);
$ya4 = round($graphData[7]['ethConsumedLast100']/1e11,4);
$ya5 = round($graphData[6]['ethConsumedLast100']/1e11,4);
$ya6 = round($graphData[5]['ethConsumedLast100']/1e11,4);
$ya7 = round($graphData[4]['ethConsumedLast100']/1e11,4);
$ya8 = round($graphData[3]['ethConsumedLast100']/1e11,4);
$ya9 = round($graphData[2]['ethConsumedLast100']/1e11,4);
$ya10 = round($graphData[1]['ethConsumedLast100']/1e11,4);
$ya11 = round($graphData[0]['ethConsumedLast100']/1e11,4);



$yb1 = round($graphData[10]['medianDelayLast100'],2);
$yb2 = round($graphData[9]['medianDelayLast100'],2);
$yb3 = round($graphData[8]['medianDelayLast100'],2);
$yb4 = round($graphData[7]['medianDelayLast100'],2);
$yb5 = round($graphData[6]['medianDelayLast100'],2);
$yb6 = round($graphData[5]['medianDelayLast100'],2);
$yb7 = round($graphData[4]['medianDelayLast100'],2);
$yb8 = round($graphData[3]['medianDelayLast100'],2);
$yb9 = round($graphData[2]['medianDelayLast100'],2);
$yb10 = round($graphData[1]['medianDelayLast100'],2);
$yb11 = round($graphData[0]['medianDelayLast100'],2);


// Get values for Misc transactions table

$latestblock = $row['latestblockNum'];
$ethprice = $row['ETHpriceUSD'];
$ethpriceEUR = $row['ETHpriceEUR'];
$ethpriceCNY = $row['ETHpriceCNY'];
$ethpriceGBP = $row['ETHpriceGBP'];

$mediantxfee = $row['mediantxfee'];
$medianfeeUSD = $ethprice * $mediantxfee / 1e9;
$medianfeeEUR = $ethpriceEUR * $mediantxfee /1e9;
$medianfeeGBP = $ethpriceGBP * $mediantxfee /1e9;
$medianfeeCNY = $ethpriceCNY * $mediantxfee /1e9;

$avgContractFee = $row['avgContractFee'];
$avgConFeeUSD = $ethprice * $avgContractFee / 1e9;
$avgConFeeEUR = $ethpriceEUR * $avgContractFee /1e9;
$avgConFeeGBP = $ethpriceGBP * $avgContractFee /1e9;
$avgConFeeCNY = $ethpriceCNY * $avgContractFee /1e9;

if(isset($_GET['curr']) && !empty($_GET['curr'])){
	$currency = $_GET['curr'];
} 
else {$currency = 'usd';}

$totalBlocks = $row['totalBlocks'];
$emptyBlocks = $row['emptyBlocks'];
$percentEmpty = round($emptyBlocks/$totalBlocks*100);


$avgContractGas = $row['avgContractGas'];

$totTx = $row['totalTx'];
$totalTransfers = $row['totalTransfers'];
$totalConCalls = $row['totalConCalls'];
$totalTimed= $row['totalTimed'];

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

$cheapestTxUSD = $cheapestTx * $ethprice / 1e9;
$cheapestTxEUR = $cheapestTx * $ethpriceEUR / 1e9;
$cheapestTxCNY = $cheapestTx * $ethpriceCNY / 1e9;
$cheapestTxGBP = $cheapestTx * $ethpriceGBP / 1e9;

$dearestTxUSD = $dearestTx * $ethprice / 1e9;
$dearestTxEUR = $dearestTx * $ethpriceEUR / 1e9;
$dearestTxCNY = $dearestTx * $ethpriceCNY / 1e9;
$dearestTxGBP = $dearestTx * $ethpriceGBP / 1e9;

$dearestConUSD = $dearestCon * $ethprice / 1e9;
$dearestConEUR = $dearestCon * $ethpriceEUR / 1e9;
$dearestConCNY = $dearestCon * $ethpriceCNY / 1e9;
$dearestConGBP = $dearestCon * $ethpriceGBP / 1e9;


$longestWait = round($longestWait/3600,1);

if ($currency == 'eur'){
	$medianfeeDisplay = '€' . round($medianfeeEUR,4);
	$cheapestTxDisplay = '€' . round($cheapestTxEUR,4);
    $dearestTxDisplay = '€' . round($dearestTxEUR,2);
    $dearestConDisplay = '€' . round($dearestConEUR,2);
    $avgConFeeDisplay = '€' . round($avgConFeeEUR,3);
}
elseif ($currency == 'cny'){
	$medianfeeDisplay = '¥' . round($medianfeeCNY,4);
	$cheapestTxDisplay = '¥' . round($cheapestTxCNY,4);
    $dearestTxDisplay = '¥' . round($dearestTxCNY,2);
    $dearestConDisplay = '¥' . round($dearestConCNY,2);
    $avgConFeeDisplay = '¥' . round($avgConFeeCNY,3);
}
elseif ($currency == 'gbp'){
	$medianfeeDisplay = '£' . round($medianfeeGBP,4);
	$cheapestTxDisplay = '£' . round($cheapestTxGBP,4);
    $dearestTxDisplay = '£' . round($dearestTxGBP,2);
    $dearestConDisplay = '£' . round($dearestConGBP,2);
    $avgConFeeDisplay = '£' . round($avgConFeeGBP,3);
	
}
else {
	$medianfeeDisplay = '$' . round($medianfeeUSD,4);
	$cheapestTxDisplay = '$' . round($cheapestTxUSD,4);
    $dearestTxDisplay = '$' . round($dearestTxUSD,2);
    $dearestConDisplay = '$' . round($dearestConUSD,2);
    $avgConFeeDisplay = '$' . round($avgConFeeUSD,3);


}


//Get data for Transaction confirmation by gas price graph

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

//Data for miner ranking table

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

//sort miners based on low price and % empty blocks

$price = array();
foreach ($miners as $key => $val)
{
	$price[$key] = $val['minP'];
	$empty[$key] = $val['pctEmp'];
}

array_multisort($price, SORT_ASC, $empty, SORT_ASC, $miners);

//Calculate Miner's Empty-block Adjusted Haspower and Miners Low Price Category

/*First determine if empty block percentage is higher than expected based on minimum price.  If it is then the empty-adjusted rate is the pecent of total blocks * (1-%empty blocks).  i.e. if a miner mines 10% of blocks but has 40% of blocks empty and has a mininum price that should allow for 99% of transactions to be mined, then then empty adjusted haspower as a pecent of total blocks mined is .1 * (1-.4) = 6%.  Howerver, if a miner mines 10% of all blocks and has 40% blocks empty but has a minimum price that only includes 10% of transactions (so 90% of blocks could be empty), then the empty-adjusted hashpower is the same as their total hashpower (i.e 10%). */

foreach ($miners as $key => $val)
{
	if ($val['minP'] < 10) //In this category, we assume that there should be no empty blocks
	{
		$miners[$key]['emptyAdjustedRate'] = $val['pctTot'] * (1-$val['pctEmp']);
	}
	elseif ($val['minP'] >=10 && $val['minP'] < 20)
	{
		$eligibleTransactions = ($cat2Tx+$cat3Tx+$cat4Tx+$cat5Tx)/$totTx;
		$observedExpectedRatio = $val['pctEmp']/(1-$eligibleTransactions);

		if ($observedExpectedRatio < 0.7) //allow for variance
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'] * (1-$val['pctEmp']);
		}
		else
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'];
		}
		$miners[$key]['minpCat'] = 2;
	}
	elseif ($val['minP'] >=10 && $val['minP'] == 20)
	{
		$eligibleTransactions = ($cat3Tx+$cat4Tx+$cat5Tx)/$totTx;
		$observedExpectedRatio = $val['pctEmp']/(1-$eligibleTransactions);
		
		if ($observedExpectedRatio < 0.7) //allow for variance
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'] * (1-$val['pctEmp']);
		}
		else
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'];
		}
		
	}
	elseif ($val['minP'] >20 && $val['minP'] <= 30)
	{
		$eligibleTransactions = ($cat4Tx+$cat5Tx)/$totTx;
		$observedExpectedRatio = $val['pctEmp']/(1-$eligibleTransactions);
		
		if ($observedExpectedRatio < 0.7) //allow for variance
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'] * (1-$val['pctEmp']);
		}
		else
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'];
		}

	}
	else
	{
		$eligibleTransactions = ($cat5Tx)/$totTx;
		$observedExpectedRatio = $val['pctEmp']/(1-$eligibleTransactions);
		
		if ($observedExpectedRatio < 0.7) //allow for variance
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'] * (1-$val['pctEmp']);
		}
		else
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'];
		}
		$miners[$key]['minpCat'] = 2;
	}
	
	echo ($key . " " . $val['pctTot'] . " ". $val['pctEmp']. " " . $miners[$key]['emptyAdjustedRate']. "break ");
}


// Now find the lowest gas price accepted by miners with 5% adjusted hashpower


$hashPower = 0;
$found = false;
foreach ($miners as $key => $val) //$miners is sorted by minP
{
	$minerGP = $val['minP'];

		foreach ($miners as $key2 => $val2)
		{
			if ($val['minP'] <= $minerGP)
			{
				$hashPower += $val['emptyAdjustedRate'];
				if ($hashPower >= 0.05)
				{
					$found = true;
					$gasPrice5Mining = $val['minP'];
					break;
				}
			}
		}
	if ($found)
	{
		break;
	}
	$hashPower = 0;
		
}




//find gas price accepted by 50% of top 10 miners

function recPrice ($miners)
{
	$cumblocks =0;
	foreach ($miners as $key => $val)
	{
		$cumblocks += $val['pctTot'];
		if ($cumblocks > .5){
			return $miners[$key]['minP'];
		}
	}
}

function safeCheap ($min50, $gasPrice5Mining) 

{
	if ($min50 <= $gasPrice5Mining)
	{
		return $gasPrice5Mining;
	}
	else
	{
		return $min50;
	}

}

//Assign recommended prices (cheapest = lowest price accepted); (fastest = highest min price accepted by all to 10 miners);

$recPrice = recPrice($miners);
$safeLow = safeCheap( $row['min50'], $gasPrice5Mining);
$lowPrice = $miners[0]['minP'];
$highPrice = $miners[9]['minP'];

//free memory associated with result
$result->close();

//close connection
$mysqli->close();




?>