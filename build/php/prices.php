<?php

require_once 'common.php';

//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

if(!$mysqli){
	die("Connection failed: " . $mysqli->error);
}

$query = "SELECT ETHpriceUSD, ETHpriceEUR, ETHpriceCNY, ETHpriceGBP, mediantxfee from txDataLast10k ORDER BY id DESC LIMIT 1";
$result = $mysqli->query($query);
$prices = $result->fetch_assoc();

$array = array ($prices);

print json_encode($array);

?>
