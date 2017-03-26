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

$query = "SELECT * FROM txDataLast10k ORDER BY id DESC LIMIT 1";
$result = $mysqli->query($query);
$row = $result->fetch_assoc();


$miners = array (
	array (
	'name' => $row['miner1name'],
	'pctTot' => $row['miner1pctTot'],
	'pctEmp' => $row['miner1pctEmp'],
	'minP' => $row['miner1minP']
	),

	array (
	'name' => $row['miner2name'],
	'pctTot' => $row['miner2pctTot'],
	'pctEmp' => $row['miner2pctEmp'],
	'minP' => $row['miner2minP']
	),


	array (
	'name' => $row['miner3name'],
	'pctTot' => $row['miner3pctTot'],
	'pctEmp' => $row['miner3pctEmp'],
	'minP' => $row['miner3minP']
	),

	array (
	'name' => $row['miner4name'],
	'pctTot' => $row['miner4pctTot'],
	'pctEmp' => $row['miner4pctEmp'],
	'minP' => $row['miner4minP']
	),

	array (
	'name' => $row['miner5name'],
	'pctTot' => $row['miner5pctTot'],
	'pctEmp' => $row['miner5pctEmp'],
	'minP' => $row['miner5minP']
	),

	array (
	'name' => $row['miner6name'],
	'pctTot' => $row['miner6pctTot'],
	'pctEmp' => $row['miner6pctEmp'],
	'minP' => $row['miner6minP']
	),

	array (
	'name' => $row['miner7name'],
	'pctTot' => $row['miner7pctTot'],
	'pctEmp' => $row['miner7pctEmp'],
	'minP' => $row['miner7minP']
	),

	array (
	'name' => $row['miner8name'],
	'pctTot' => $row['miner8pctTot'],
	'pctEmp' => $row['miner8pctEmp'],
	'minP' => $row['miner8minP']
	),

	array (
	'name' => $row['miner9name'],
	'pctTot' => $row['miner9pctTot'],
	'pctEmp' => $row['miner9pctEmp'],
	'minP' => $row['miner9minP']
	),

	array (
	'name' => $row['miner10name'],
	'pctTot' => $row['miner10pctTot'],
	'pctEmp' => $row['miner10pctEmp'],
	'minP' => $row['miner10minP']
	)
);

//sort miners based on low price and % empty blocks

$price = array();
foreach ($miners as $key => $row)
{
	$price[$key] = $row['minP'];
	$empty[$key] = $row['pctEmp'];
}

array_multisort($price, SORT_ASC, $empty, SORT_ASC, $miners);


//find gas price accepted by 50% of top 10 miners

function recPrice ($miners)
{
	$cumblocks =0;
	$x = 0;
	foreach ($miners as $key => $val)
	{
		$cumblocks += $val['pctTot'];
		if ($cumblocks > .5){
			return $miners[$x]['minP'];
		}
	$x++;
	}
}

function safeCheap ($miners, $min50) //price with at least 25 transactions and accepted by two miners with close to full blocks
{
	$cumblocks =0;
	$x =0;
	$y =0;
	foreach ($miners as $key => $val)
	{
		if ($val['pctEmp'] < .15) //miner has less than 15% emptyblocks
		{
			$y++;
			if ($y>=2 && $miners[$x]['minP']>= $min50)  /*Minimum price from second miner mining nearly full blocks and at least 50 transactions mined at or below this price in last 10,000 blocks*/
			
			{
				return $miners[$x]['minP'];
			}
            elseif ($x ==9)
            {
                return $miners[$x]['minP'];
            }

		}
	$x++;
	}
}

//Assign recommended prices (cheapest = lowest price accepted); (fastest = highest min price accepted by all to 10 miners);

$recPrice = recPrice($miners);
$safeLow = safeLow($miners, $row['min50']);
$lowPrice = $miners[0]['minP'];
$highPrice = $miners[9]['minP'];

//free memory associated with result
$result->close();

//close connection
$mysqli->close();

$array = array ('cheapest'=>$lowPrice, 'safeLow'=> $safeLow, 'average'=>$recPrice, 'fastest'=>$highPrice);

print json_encode($array);

?>


