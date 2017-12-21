<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <!-- Meta, title, CSS, favicons, etc. -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>ETH Gas Station | Consumer oriented metrics for the Ethereum gas market </title>

    <meta name="keywords" content="Ethereum ETH gas blockchain market price transactions miners users">
    <meta name="description" content="User oriented, real-time metrics on gas price, wait times, and miner policies on the Ethereum netowrk">
    
    <meta property="og:title" content="ETH Gas Station" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="images/ETHGasStation.png" />
    <meta property="og:url" content="http://ethgasstation.info" />


    <!-- Bootstrap -->
    <link href="vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">

    <!--Favicon-->
    <link rel="apple-touch-icon" sizes="57x57" href="images/apple-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="images/apple-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="images/apple-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="images/apple-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="images/apple-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="images/apple-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="images/apple-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="images/apple-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="images/apple-icon-180x180.png">
    <link rel="icon" type="image/png" sizes="192x192"  href="images/android-icon-192x192.png">
    <link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="96x96" href="images/favicon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="images/favicon-16x16.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="images/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">


    <!-- Custom Theme Style -->
    <link href="build/css/custom.css" rel="stylesheet">
    <?php include 'build/php/minerT_py.php'; ?>

   


  </head>

  <body class="nav-md">
    <div class="container body">
      <div class="main_container">

   <?php include 'sidebar.php'; ?>   

        <!-- top navigation -->
        <div class="top_nav">
          <div class="nav_menu">
            <nav>
              <div class="nav toggle">
                <a id="menu_toggle"><i class="fa fa-bars"></i></a>
              </div>
              <ul class="nav navbar-nav navbar-right">
              </ul>
            </nav>
          </div>
         </div>

        <!-- /top navigation -->

        <!-- page content -->
        <div class="right_col" role="main">
          <div class="row">
              <div class="col-md-8 col-sm-12 col-xs-12">
                <div class="x_panel tile fixed_height_420">
                  <div class="x_title">
                    <h4>Txpool Data At Block <span style = 'color:#1ABB9C'><?php echo $gpRecs2['blockNum']?></h4>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                  <table class="table table-striped">
                      <thead>
                        <tr>
                          <th>Gas Price (Gwei)</th>
                          <th>% of Last 200 Blocks Accepting </th>
                          <th>#Tx at/above in txpool</th>
                          <th>% of Tx Unmined > 5min</th>
                          <th>% of Tx Unmined > 60min</th>
                          <th>Mean Time to Confirm (Minutes)</th>
                          <th>95% Confidence Confirm Time (Minutes)</th>
                        </tr>
                      </thead>
                      <tbody>
                      <?php
                      foreach ($predictArray as $row){
                        if ($row['gasprice']>=0){
                        echo('<tr>');
                        $uciWait = $row['expectedTime'] * 2.5;
                        echo("<td>". $row['gasprice']. "</td>");
                        echo("<td>". round($row['hashpower_accepting'], 1) ."</td>");
                        echo("<td>". $row['tx_atabove']."</td>");
                        echo("<td>". $row['s5mago']. "</td>");
                        echo("<td>". $row['s1hago']. "</td>");
                        if ($row['expectedTime'] > 120){
                          echo("<td>". "> 2 hours". "</td>");
                        }
                        else {
                        echo("<td>". round($row['expectedTime'],1). "</td>");}
                        if ($uciWait > 120){
                          echo("<td>". "> 2 hours". "</td>");
                        }
                        else{
                        echo("<td>". round($uciWait, 1). "</td>");}
                        
                        echo('</tr>');}

                      }
                      ?>
                        </tbody>
                    </table>

                 </div>
        </div>
    </div>
                    

    <!-- /misc transactions -->

  </div>
</div>
             
<!-- /page content -->

        <!-- footer content -->
        <footer>
          <div class="pull-right">
            Gentelella - Bootstrap Admin Template by <a href="https://colorlib.com">Colorlib</a>
          </div>
          <div class="clearfix"></div>
        </footer>
        <!-- /footer content -->

      </div>
    </div>

 <!-- jQuery -->
    <script src="vendors/jquery/dist/jquery.min.js"></script>
 <!-- Bootstrap -->
    <script src="vendors/bootstrap/dist/js/bootstrap.min.js"></script>
 <!-- Chart.js -->
    <script src="vendors/Chart.js/dist/Chart.min.js"></script>
    

<!-- Custom Theme Scripts -->




    <script src="build/js/custom3.js"></script>
    
	
  </body>
</html>
