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
$minerString = file_get_contents("http://localhost/json/miners_py.json");
$minersArray = json_decode($minerString, true);

$predictString = file_get_contents("http://localhost/json/predictTable_py.json");
$predictArray = json_decode($predictString, true);

$gpRecsString2 = file_get_contents("http://localhost/json/ethgasAPI_py.json");
$gpRecs2 = json_decode($gpRecsString2, true);

$gasGuzzRaw = file_get_contents("http://localhost/json/gasguzz_py.json");
$gasGuzzTable = json_decode($gasGuzzRaw, true);

$memPoolString = file_get_contents("http://localhost/json/memPool_py.json");
$memPoolArray = json_decode($memPoolString, true);

$validatedString = file_get_contents("http://localhost/json/validated.json");
$validatedArray = json_decode($validatedString, true);
} catch (Exception $e){
	echo 'keep waiting';
}
?>