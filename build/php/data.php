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

$result->close();



$graphData = array();
$query2 = "SELECT * FROM txDataLast100b ORDER BY id DESC LIMIT 11";
$result2 = $mysqli->query($query2);

while ($row2 = $result2->fetch_assoc()){
	array_push($graphData,$row2);
}
$result2->close();
$mysqli->close();

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
$fullBlocks = $row['fullBlocks'];
$percentEmpty = round($emptyBlocks/$totalBlocks*100);
$percentFull = round($fullBlocks/$totalBlocks*100);


$avgContractGas = $row['avgContractGas'];

$totTx = $row['totalTx'];
$totalTransfers = $row['totalTransfers'];
$totalConCalls = $row['totalConCalls'];
$totalTimed= $row['totalTimed'];

settype($medianfeeusd, "float");
$medianwaitsec = $row['medianTime'];
$medianwaitblock = $row['medianMinedDelay'];
$gaspricehigh = $row['maxMinedGasPrice'];
$gaspricelow = $row['minMinedGasPrice']/1000;
$gaspricemedian = $row['medianGasPrice'];

$cheapestTx = $row['cheapestTx'];
$cheapestTxId= $row['cheapestTxID'];
$dearestTx = $row['dearestTx'];
$dearestTxId = $row['dearestTxID'];
$dearestCon = $row['dearConTx'];
$dearestConId = $row['dearConTxID'];
$longestWait = $row['longestWait'];
$longestWaitId = $row['longestWaitID'];




//Get data for Transaction confirmation by gas price graph

$cat1Tx = $row['cat1gasTotTx'];
$cat2Tx = $row['cat2gasTotTx'];
$cat3Tx = $row['cat3gasTotTx'];
$cat4Tx = $row['cat4gasTotTx'];
$cat5Tx = $row['cat5gasTotTx'];


if ($cat1Tx == null)
{
	$cat1tx = 0 ;
}


$cat1TxPct = round($cat1Tx/$totTx, 4) *100;
$cat2TxPct = round($cat2Tx/$totTx, 4) *100;
$cat3TxPct = round($cat3Tx/$totTx, 4) *100;
$cat4TxPct = round($cat4Tx/$totTx, 4) *100;
$cat5TxPct = round($cat5Tx/$totTx, 4) *100;


if ($currency == 'eur'){
    $exchangeRate = $ethpriceEUR;
    $currString = '€';
}
elseif ($currency == 'cny'){
    $exchangeRate = $ethpriceCNY;
    $currString = '¥';

}
elseif ($currency == 'gbp'){
    $exchangeRate = $ethpriceGBP;
    $currString = '£';
}
else{
    $exchangeRate = $ethprice;
    $currString = '$';
}




//Data for miner ranking table
try{
    $minerString = file_get_contents("http://localhost/json/topMiners.json");
    $topMiners = json_decode($minerString, true);

    $priceWaitString = file_get_contents("http://localhost/json/priceWait.json");
    $priceWait = json_decode($priceWaitString, true);
    $priceWaitData = '';
    $priceWaitLabels = '';
    foreach($priceWait as $row)
    {
        if ($row['minedGasPrice']==0){
            $row['minedGasPrice']= '<1';
        }
        if ($row['minedGasPrice']==40){
            $row['minedGasPrice'] = '>40';
        }
        $priceWaitLabels = $priceWaitLabels. "'". $row['minedGasPrice']."'".',';
        $priceWaitData = $priceWaitData. round($row['delay'],1). ',';
    }
    $priceWaitData = rtrim($priceWaitData,',');
    $priceWaitLabels = rtrim($priceWaitLabels, ',');
    
    $gpRecsString = file_get_contents("http://localhost/json/ethgas.json");
    $gpRecs = json_decode($gpRecsString, true);

    $gpRecsString2 = file_get_contents("http://localhost/json/ethgasAPI.json");
    $gpRecs2 = json_decode($gpRecsString2, true);

    $predictString = file_get_contents("http://localhost/json/predictTable.json");
    $predictTable = json_decode($predictString, true);

    function sliderValue ($gasPrice){
        if ($gasPrice < 1){
            return ($gasPrice*10);
        }
        else{
            return ($gasPrice+9);
        }
    }
    $avgRef = sliderValue ($gpRecs2['average']);
    $fastestRef = sliderValue($gpRecs2['fastest']);
    $minRef = sliderValue($gpRecs2['safeLow']);


    $calcParamString = file_get_contents("http://localhost/json/calc.json");
    $calcParams = json_decode($calcParamString, true);

    $sWait = exp($calcParams['Intercept'] + $calcParams['priceCat1']);
    $aWait = exp($calcParams['Intercept'] + $calcParams['priceCat2']);
    $fWait = exp($calcParams['Intercept'] + $calcParams['priceCat4']);
    $safeLowWait = round($sWait*$calcParams['blockInterval']/60,1);
    $lowTransfer = $currString . number_format($gpRecs2['safeLow']/1e9*21000*$exchangeRate,3);
    $avgWait = round($aWait*$calcParams['blockInterval']/60,1);
    $fastWait = round($fWait*$calcParams['blockInterval']/60,1);
} catch (Exception $e){
    echo 'waith for tables to be populated';
}
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

?>