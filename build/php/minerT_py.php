<?php

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

try{
$minerString = file_get_contents("http://localhost/json/miners.json");
$minersArray = json_decode($minerString, true);

$predictString = file_get_contents("http://localhost/json/predictTable.json");
$predictArray = json_decode($predictString, true);

$safeLowString = file_get_contents("http://localhost/json/hourago.json");
$safeLowArray = json_decode($safeLowString, true);

$gpRecsString2 = file_get_contents("http://localhost/json/ethgasAPI.json");
$gpRecs2 = json_decode($gpRecsString2, true);
$latestBlock = $gpRecs2['blockNum'];
$bnum = $gpRecs2['blockNum'];
$gasGuzzRaw = file_get_contents("http://localhost/json/gasguzz.json");
$gasGuzzTable = json_decode($gasGuzzRaw, true);

$memPoolString = file_get_contents("http://localhost/json/memPool.json");
$memPoolArray = json_decode($memPoolString, true);

$rowString = file_get_contents("http://localhost/json/txDataLast10k.json");
$row = json_decode($rowString, true);

$txpoolString = file_get_contents("http://localhost/json/txpoolblock.json");
$txpoolArray = json_decode($txpoolString, true);

$validatedString = file_get_contents("http://localhost/json/validated.json");
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