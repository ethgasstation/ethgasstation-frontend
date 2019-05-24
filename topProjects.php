<?php 

  /**
  *
  * @author arman
  * @since 5/20/19
  */

  $ch = curl_init();
  $url = 'http://gasburners-jsapi-prod.us-west-1.elasticbeanstalk.com/api/leaderboard';

  curl_setopt_array(
  $ch, array(
    CURLOPT_URL => $url,
    CURLOPT_RETURNTRANSFER => true
  ));

  $output = curl_exec($ch);
  $decodedData = json_decode($output);
  $counter = 1;

  foreach($decodedData as $data) {
    if ($data->project == "unknown") {
      echo "<tr><td>". $counter++ .".</td><td>". $data->contracts[0]->contract ."</td><td>". $data->gas ."</td><td>". $data->costETH . "ETH ($" . $data->costUsd .")</td><td>3.4%</td></tr>";
    } else {
      echo "<tr><td>". $counter++ .".</td><td>". $data->project ."</td><td>". $data->gas ."</td><td>". $data->costETH . "ETH ($" . $data->costUsd .")</td><td>3.4%</td></tr>";
    }
  }
 
?>