<?php

require_once 'common.php';

//query to get data from the table


try{
$memPoolString = get_json_file("memPool.json");
$memPoolArray = json_decode($memPoolString, true);

$voteString = get_json_file("vote.json");
$voteArray = json_decode($voteString, true);

$gp2 = get_json_file("ethgasAPI.json");
$gp2data = json_decode($gp2, true);


} catch (Exception $e){
	echo 'keep waiting';
}


?>