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

$query = "SELECT * FROM txDataLast10k ORDER BY id DESC LIMIT 1";
$result = $mysqli->query($query);
$dataRow = $result->fetch_assoc();
$latestblock = $dataRow['latestblockNum'];
try{
$minerString = file_get_contents("http://localhost/json/miners.json");
$minersArray = json_decode($minerString, true);

$priceString = file_get_contents("http://localhost/json/price3.json");
$priceArray = json_decode($priceString, true);

$predictString = file_get_contents("http://localhost/json/predictTable.json");
$predictArray = json_decode($predictString, true);

$voteString = file_get_contents("http://localhost/json/minerVotes.json");
$voteArray = json_decode($voteString, true);

$validatedString = file_get_contents("http://localhost/json/validated.json");
$validatedArray = json_decode($validatedString, true);
} catch (Exception $e){
	echo 'keep waiting';
}
?>