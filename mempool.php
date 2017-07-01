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
    <?php include 'build/php/mempoolload.php'; ?>

   


  </head>

  <body class="nav-md">
    <div class="container body">
      <div class="main_container">

<!-- Sidebar -->
      <?php include 'sidebar.php'; ?>

        <!-- top navigation -->
        <div class="top_nav">
          <div class="nav_menu">
            <nav>
              <div class="nav toggle">
                <a id="menu_toggle"><i class="fa fa-bars"></i></a>
              </div>
              <ul class="nav navbar-nav navbar-right">
              <p class="navbar-text navbar-left" style="padding-left: 5px"><strong><?php echo "Last update: Block <span style = 'color:#1ABB9C'>". $voteArray['blockNum']; ?></strong></span>  
              </p>
            </ul>
            </nav>
          </div>
         </div>

        <!-- /top navigation -->

        <!-- page content -->
        <div class="right_col" role="main">
          <div class="row">
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel tile fixed_height_420">
                  <div class="x_title">
                    <h4>Transaction Pool Status By Gas Price</h4>
                    <p class="nav navbar-right"><span style = 'color:red'>Miner: </span><?php echo($voteArray['miner']); ?></br><span style = 'color:red'> Prior Block Gas Used: </span><?php echo($voteArray['priorGasused']);?></br><span style = 'color:red'> Gas Used: </span><?php echo($voteArray['gasUsed']);?></br><span style = 'color:red'> Gas Limit: </span><?php echo($voteArray['gasLimit']);?></br><span style = 'color:red'> Gas Limit Vote: </span><?php echo($voteArray['vote']);?></p> 
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                  <table class="table table-striped">
                      <thead>
                        <tr>
                          <th>Gas Price (Gwei)</th>
                          <th>TxPool</br>Total Gas (1e6)</th>
                          <th>TxPool</br>Total Transactions</th>
                          <th>Mean Time in </br>TxPool (Min)</th>
                          <th></th>
                          <th><span style = 'color:#1ABB9C'>Gas Mined (1e6)</span></th>
                          <th><span style = 'color:#1ABB9C'>Gas Removed (1e6)</span></th>
                          <th><span style = 'color:#1ABB9C'>Transactions Mined</span></th>
                        </tr>
                      </thead>
                      <tbody>
                      <?php
                      foreach ($memPoolArray as $row){
                        echo('<tr>');
                        echo("<td>". $row['gasPrice']. "</td>");
                        echo("<td>". $row['gasOffered']. "</td>");
                        echo("<td>". $row['numTxPending']. "</td>");
                        if ($row['numTxPending']>10){
                          echo("<td>". round($row['waitTime']/60, 1). "</td>");
                        }
                        else{
                          echo("<td>". '..' . "</td>");
                        }
                        
                        echo("<td>". "</td>");
                        echo("<td>". $row['gasused']. "</td>");
                        echo("<td>". $row['gasRemoved']. "</td>");
                        echo("<td>". $row['numTxMined']. "</td>");
                        echo('</tr>');

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
   <script>


 </script>



    <script src="build/js/custom3.js"></script>
    
	
  </body>
</html>
