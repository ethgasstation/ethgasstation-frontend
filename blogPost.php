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
  $content = $decodedData[0]->excerpt->rendered;
  echo "<h2 class='post_title'>".$decodedData[0]->title->rendered."</h2>";

  echo $content."<a href=".$decodedData[0]->guid->rendered." target='_blank' style='text-decoration: underline;'>Read more...</a>";
?>