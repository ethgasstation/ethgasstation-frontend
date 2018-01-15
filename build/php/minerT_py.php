<?php

require_once 'common.php';

//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

if(!$mysqli){
	die("Connection failed: " . $mysqli->error);
}

//query to get data from the table

try{
$minerString = get_json_file("miners.json");
$minersArray = json_decode($minerString, true);

$predictString = get_json_file("predictTable.json");
$predictArray = json_decode($predictString, true);

$safeLowString = get_json_file("hourago.json");
$safeLowArray = json_decode($safeLowString, true);

$gpRecsString2 = get_json_file("ethgasAPI.json");
$gpRecs2 = json_decode($gpRecsString2, true);
$latestBlock = $gpRecs2['blockNum'];
$bnum = $gpRecs2['blockNum'];
$gasGuzzRaw = get_json_file("gasguzz.json");
$gasGuzzTable = json_decode($gasGuzzRaw, true);

$memPoolString = get_json_file("memPool.json");
$memPoolArray = json_decode($memPoolString, true);

$rowString = get_json_file("txDataLast10k.json");
$row = json_decode($rowString, true);

$txpoolString = get_json_file("txpoolblock.json");
$txpoolArray = json_decode($txpoolString, true);

$validatedString = get_json_file("validated.json");
$validatedArray = json_decode($validatedString, true);
} catch (Exception $e){
	echo 'keep waiting';
}

$latestblock = $row['latestblockNum'];
$ethprice = $row['ETHpriceUSD'];
$ethpriceEUR = $row['ETHpriceEUR'];
$ethpriceCNY = $row['ETHpriceCNY'];
$ethpriceGBP = $row['ETHpriceGBP'];

if(isset($_GET['curr']) && !empty($_GET['curr'])){
	$currency = $_GET['curr'];

} 
else {$currency = 'usd';}

if ($currency == 'usd'){
    $exchangeRate = $ethprice;
}
elseif ($currency == 'eur'){
    $exchangeRate = $ethpriceEUR;
}
elseif ($currency == 'cny'){
    $exchangeRate = $ethpriceCNY;
}
elseif ($currency == 'gbp'){
    $exchangeRate = $ethpriceGBP;
}

?>