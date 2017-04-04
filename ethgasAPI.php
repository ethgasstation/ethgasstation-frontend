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

//Get data for Transaction confirmation by gas price graph
$totTx = $row['totalTx'];

$cat1Tx = $row['cat1gasTotTx'];
$cat1TimeMed = $row['cat1gasMedianTime'];
$cat1Time95 = $row['cat1gas95DelayTime'];

$cat2Tx = $row['cat2gasTotTx'];
$cat2TimeMed = $row['cat2gasMedianTime'];
$cat2Time95 = $row['cat2gas95DelayTime'];

$cat3Tx = $row['cat3gasTotTx'];
$cat3TimeMed = $row['cat3gasMedianTime'];
$cat3Time95 = $row['cat3gas95DelayTime'];

$cat4Tx = $row['cat4gasTotTx'];
$cat4TimeMed = $row['cat4gasMedianTime'];
$cat4Time95 = $row['cat4gas95DelayTime'];

$cat5Tx = $row['cat5gasTotTx'];
$cat5TimeMed = $row['cat5gasMedianTime'];
$cat5Time95 = $row['cat5gas95DelayTime'];

if ($cat1Tx == null)
{
	$cat1tx = 0 ;
}


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
foreach ($miners as $key => $val)
{
	$price[$key] = $val['minP'];
	$empty[$key] = $val['pctEmp'];
}

array_multisort($price, SORT_ASC, $empty, SORT_ASC, $miners);


//Calculate Miner's Empty-block Adjusted Haspower

/*First determine if empty block percentage is higher than expected based on minimum price.  If it is then the empty-adjusted rate is the pecent of total blocks * (1-%empty blocks).  i.e. if a miner mines 10% of blocks but has 40% of blocks empty and has a mininum price that should allow for 99% of transactions to be mined, then then empty adjusted haspower as a pecent of total blocks mined is .1 * (1-.4) = 6%.  Howerver, if a miner mines 10% of all blocks and has 40% blocks empty but has a minimum price that only includes 10% of transactions (so 90% of blocks could be empty), then the empty-adjusted hashpower is the same as their total hashpower (i.e 10%). */

foreach ($miners as $key => $val)
{
	if ($val['minP'] < 10) //In this category, we assume that there should be no empty blocks
	{
		
		$miners[$key]['emptyAdjustedRate'] = $val['pctTot'] * (1-$val['pctEmp']);
		echo "$key ". " hi ". $val['name'] . " ". $miners[$key]['emptyAdjustedRate'];
	}
	elseif ($val['minP'] >=10 && $val['minP'] < 20)
	{
		$eligibleTransactions = ($cat2Tx+$cat3Tx+$cat4Tx+$cat5Tx)/$totTx - .0001;

		$observedExpectedRatio = $val['pctEmp']/(1-$eligibleTransactions);

		if ($observedExpectedRatio > 1) 
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'] * (1-$val['pctEmp']);
		}
		else
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'];
		}

	}
	elseif ($val['minP'] >=10 && $val['minP'] == 20)
	{
		$eligibleTransactions = ($cat3Tx+$cat4Tx+$cat5Tx)/$totTx - 0.0001;
		$observedExpectedRatio = $val['pctEmp']/(1-$eligibleTransactions);
		
		if ($observedExpectedRatio > 1) 
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'] * (1-$val['pctEmp']);
		}
		else
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'];
		}
		
	}
	elseif ($val['minP'] >20 && $val['minP'] <= 30)
	{
		$eligibleTransactions = ($cat4Tx+$cat5Tx)/$totTx - 0.0001;
		$observedExpectedRatio = $val['pctEmp']/(1-$eligibleTransactions);
		
		if ($observedExpectedRatio > 1 ) 
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'] * (1-$val['pctEmp']);
		}
		else
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'];
		}

	}
	else
	{
		$eligibleTransactions = ($cat5Tx)/$totTx -0.0001;
		$observedExpectedRatio = $val['pctEmp']/(1-$eligibleTransactions);
		
		if ($observedExpectedRatio > 1) 
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'] * (1-$val['pctEmp']);
		}
		else
		{
			$miners[$key]['emptyAdjustedRate'] = $val['pctTot'];
		}
	
	}
	
	
}


// Now find the lowest gas price accepted by miners with 5% adjusted hashpower


$hashPower = 0;
$found = false;
foreach ($miners as $key => $val) //$miners is sorted by minP
{
	$minerGP = $val['minP'];

		foreach ($miners as $key2 => $val2)
		{	echo "a ". "$minerGP ". $val2['name']. " ddd ". $val2['minP'];
			if ($val2['minP'] <= $minerGP)
			{
				$hashPower += $val2['emptyAdjustedRate'];
				if ($hashPower >= 0.05)
				{
					$found = true;
					$gasPrice5Mining = $val2['minP'];
					break;
				}
			}
		}
	if ($found)
	{
		break;
	}
	$hashPower = 0;
		
}




//find gas price accepted by 50% of top 10 miners

function recPrice ($miners)
{
	$cumblocks =0;
	foreach ($miners as $key => $val)
	{
		$cumblocks += $val['pctTot'];
		if ($cumblocks > .5){
			return $miners[$key]['minP'];
		}
	}
}

function safeCheap ($min50, $gasPrice5Mining) 

{
	if ($min50 <= $gasPrice5Mining)
	{
		return $gasPrice5Mining;
	}
	else
	{
		return $min50;
	}

}

//Assign recommended prices (cheapest = lowest price accepted); (fastest = highest min price accepted by all to 10 miners);

echo "\n ttt $gasPrice5Mining ff" . $row['min50'];

$recPrice = recPrice($miners);
$safeLow = safeCheap( $row['min50'], $gasPrice5Mining);
$lowPrice = $miners[0]['minP'];
$highPrice = $miners[9]['minP'];

//free memory associated with result
$result->close();

//close connection
$mysqli->close();

$abi = array(
	"Cheapest"=>$lowPrice,
	"SafeLow"=>$safeLow,
	"Average"=>$recPrice,
	"Fastest"=>$highPrice
);

print json_encode($abi);


?>