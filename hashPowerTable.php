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
    <?php include 'build/php/minerT.php'; ?>

   


  </head>

  <body class="nav-md">
    <div class="container body">
      <div class="main_container">

<!-- Sidebar -->

        <div class="col-md-3 left_col">
          <div class="left_col scroll-view">

            <div class="navbar nav_title" style="border: 0;">
              <a href="index.php" class="site_title"><img src="images/ETHgas.png" style="height:32px;width:32px"> <span>ETH Gas Station</span></a>
            </div>
            
            <div class="clearfix"></div>
            <br />

          <div id="sidebar-menu" class="main_menu_side hidden-print main_menu">
              <div class="menu_section">
                <h3>General</h3>
                <ul class="nav side-menu">
                  <li><a href="index.php"><i class ="fa fa-home"></i>Main Page</a></li>
                  <li><a href="calculator.php"><i class ="fa fa-calculator"></i>Gas-Time Calculator</a></li>
                  <li><a href="minerTable.php"><i class ="fa fa-cubes"></i>Miner Stats</a></li>
                  <li><a href="hashPowerTable.php"><i class ="fa fa-cubes"></i>Hash Power by Gas Price</a></li>
                  <li><a href="validatedTable.php"><i class ="fa fa-cubes"></i>Low Gas Price Watch List</a></li>
                  <li><a><i class="fa fa-bookmark-o"></i>FAQ<span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="about.html">What Is This Site?</a></li>
                      <li><a href="FAQcalc.html">Calculator</a></li>
                      <li><a href="gasrecs.html">Gas Price Recommendations</a></li>
                      <li><a href="FAQpage.html">Other FAQ</a></li>
                    </ul>
                  </li>
                  <li><a><i class="fa fa-link"></i> External Links <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="https://coincenter.org/entry/what-is-ethereum" target="_blank">What is Ethereum?</a></li>
                      <li><a href="https://www.ethereum.org/ether" target="_blank">Ethereum FAQ</a></li>
                      <li><a href="https://media.consensys.net/ethereum-gas-fuel-and-fees-3333e17fe1dc#.krqnhnkav" target="_blank">What is gas?</a></li>
                      <li><a href="https://blog.ethereum.org/2016/10/31/uncle-rate-transaction-fee-analysis/" target="_blank">Gas Market: Advanced reading</a></li>
                    </ul>
                  </li>
                </ul>
              </div>
            </div>
            <!-- /sidebar -->
        </div>
      </div>

        <!-- top navigation -->
        <div class="top_nav">
          <div class="nav_menu">
            <nav>
              <div class="nav toggle">
                <a id="menu_toggle"><i class="fa fa-bars"></i></a>
              </div>
              <ul class="nav navbar-nav navbar-right">
              <p class="navbar-text navbar-left" style="padding-left: 5px"><strong><?php echo "Stats over last 10,000 blocks - Last update: Block <span style = 'color:#1ABB9C'> $latestblock" ?></strong></span>  
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
                <div class="x_panel">
                  <div class="x_title">
                    <h4>Blocks Mined by Minimum Gas Price Accepted</h4>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                  <table class="table table-striped">
                      <thead>
                        <tr>
                          <th>Gas Price <br>(Gwei)</th>
                          <!--<th>% of Total<br>Blocks</th>
                          <th>% of Non-Empty<br>Blocks</th>-->
                          <th>Percent of<br>Total Blocks</th>
                          <th>Percent of<br> Non-empty Blocks</th>
                        </tr>
                      </thead>
                      <tbody>
                      <?php
                      foreach ($priceArray as $row){
                        echo('<tr>');
                        echo("<td> ≥ ". $row['minPrice']. "</td>");
                        #echo("<td>". round($row['pctTotBlocks'],1). "</td>");
                        #echo("<td>". round($row['pctTxBlocks'],1). "</td>");
                        echo("<td>". round($row['cumPctTotBlocks'],1). "</td>");
                        echo("<td>". round($row['cumPctTxBlocks'],1). "</td>");
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
