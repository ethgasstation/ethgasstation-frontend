<?php 
  $ch = curl_init();
  curl_setopt_array(
  $ch, array(
  CURLOPT_URL => 'https://ethgasstation.info/blog/wp-json/wp/v2/posts?per_page=1',
  CURLOPT_RETURNTRANSFER => true
  ));

  function strLastReplace($mainStr, $search, $replace) {
    return strrev(implode(strrev($replace), explode(strrev($search), strrev($mainStr, 2))));
  }

  $output = curl_exec($ch);
  $decodedData = json_decode($output);
  $link = "https://ethgasstation.info" . $decodedData[0]->link;

  echo "<a href=". $link. " class='post_title' target='_blank'> .$decodedData[0]->title->rendered. "</a>";
?>