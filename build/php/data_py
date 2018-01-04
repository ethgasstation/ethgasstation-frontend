<?php

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

$rowString = file_get_contents("http://localhost/json/txData10k.json");
$row = json_decode($rowString, true);

// Get values for Misc transactions table

$latestblock = $row['latestblockNum'];
$ethprice = $row['ETHpriceUSD'];
$ethpriceEUR = $row['ETHpriceEUR'];
$ethpriceCNY = $row['ETHpriceCNY'];
$ethpriceGBP = $row['ETHpriceGBP'];

$mediantxfee = $row['avgTxFee'];
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

settype($medianfeeusd, "float");
$medianwaitsec = $row['medianDelayTime'];
$medianwaitblock = $row['medianDelay'];
$gaspricehigh = $row['maxMinedGasPrice'];
$gaspricelow = $row['minMinedGasPrice']/1000;
$gaspricemedian = $row['medianGasPrice'];

$cheapestTx = $row['cheapestTx'];
$cheapestTxId= $row['cheapestTxID'];
$dearestTx = $row['dearestTx'];
$dearestTxId = $row['dearestTxID'];
$dearestCon = $row['dearConTx'];
$dearestConId = $row['dearConTxID'];




//Get data for Transaction confirmation by gas price graph

$cat1Tx = $row['totalCatTx1'];
$cat2Tx = $row['totalCatTx2'];
$cat3Tx = $row['totalCatTx3'];
$cat4Tx = $row['totalCatTx4'];
$cat5Tx = $row['totalCatTx5'];


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