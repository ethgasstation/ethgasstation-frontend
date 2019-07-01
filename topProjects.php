<?php 

  /**
  *
  * @author arman
  * @since 5/20/19
  */

  $ch = curl_init();
  $url = 'http://gasburners-jsapi-prod.us-west-1.elasticbeanstalk.com/api/leaderboard';

  function _shortenContract($contract) {
    return substr($contract, 0, 6) . '...' . substr($contract, strlen($contract) - 4);
  }

  curl_setopt_array(
  $ch, array(
    CURLOPT_URL => $url,
    CURLOPT_RETURNTRANSFER => true
  ));

  $output = curl_exec($ch);
  $decodedData = json_decode($output);
  $counter = 1;

  foreach($decodedData as $data) {
    $etherscanLink = "https://etherscan.io/address/" . $data->contract;

    if ($data->project == "unknown") {
      echo "<tr><td>" . $counter++ . ".</td><td><a href=" . $etherscanLink . " class='etherscan_link' target='_blank'>" . _shortenContract($data->contract) . "</a></td><td>". $data->costETH . "</td><td>" . $data->avgGwei . "</td><td>$" . $data->costUsd . "</td></tr>";
    } else {
      echo "<tr><td>". $counter++ .".</td><td>". $data->project ."</td><td>". $data->costETH ."</td><td>". $data->avgGwei ."</td><td>$". $data->costUsd ."</td></tr>";
    }
  }
 
?>