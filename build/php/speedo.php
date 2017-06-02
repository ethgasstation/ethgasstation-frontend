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

$query = "SELECT AVG(speed) AS average FROM (SELECT speed FROM speedo2 ORDER BY id DESC LIMIT 10) a";
$result = $mysqli->query($query);
$avgSpeed = $result->fetch_assoc();

$query2 = "SELECT blockNum FROM speedo2 ORDER BY id DESC LIMIT 1";
$result2 = $mysqli->query($query2);
$blockNum = $result2->fetch_assoc();

$array = array ($blockNum, $avgSpeed);

print json_encode($array);

?>
