<?php

require_once 'common.php';

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
$minerString = get_json_file("miners.json");
$minersArray = json_decode($minerString, true);

$priceString = get_json_file("price3.json");
$priceArray = json_decode($priceString, true);

$predictString = get_json_file("predictTable.json");
$predictArray = json_decode($predictString, true);

$voteString = get_json_file("minerVotes.json");
$voteArray = json_decode($voteString, true);

$validatedString = get_json_file("validated.json");
$validatedArray = json_decode($validatedString, true);
} catch (Exception $e){
	echo 'keep waiting';
}
?>