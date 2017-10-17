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
              <p class="navbar-text navbar-left" style="padding-left: 5px"><strong><?php echo "Stats over last 1500 blocks - Last update: Block <span style = 'color:#1ABB9C'> $latestBlock" ?></strong></span>  
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
                    <h4>Miner Gas Policies and Block Stats</h4>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                  <table class="table table-striped">
                      <thead>
                        <tr>
                          <th>Miner</th>
                          <th>Min Gas Price<br>Accepted<sup>*</sup> (Gwei)</th>
                          <th>Total <br> Blocks</th>
                          <th>Empty <br>Blocks</th>
                          <th>% of Total <br>Blocks</th>
                          <th>% of Non-empty<br> Blocks</th>
                        </tr>
                      </thead>
                      <tbody>
                      <?php
                      $minerNames = array(
    '0xea674fdde714fd979de3edf0f56aa9716b898ec8'=>'Ethermine',
    '0x1e9939daaad6924ad004c2560e90804164900341'=>'ethfans',
    '0xb2930b35844a230f00e51431acae96fe543a0347'=>'miningpoolhub',
    '0x4bb96091ee9d802ed039c4d1a5f6216f90f81b01'=>'Ethpool',
    '0x52bc44d5378309ee2abf1539bf71de1b7d7be3b5'=>'Nanopool',
    '0x2a65aca4d5fc5b5c859090a6c34d164135398226'=>'Dwarfpool',
    '0x61c808d82a3ac53231750dadc13c777b59310bd9'=>'f2pool',
    '0xa42af2c70d316684e57aefcc6e393fecb1c7e84e'=>'Coinotron',
    '0x6c7f03ddfdd8a37ca267c88630a4fee958591de0'=>'alpereum'

                      );
                      foreach ($minersArray as $row){
                        echo('<tr>');
                        if(array_key_exists ($row['miner'],$minerNames)){
                        $row['miner'] = $minerNames[$row['miner']];}
                        echo("<td>". $row['miner']. "</td>");
                        echo("<td>". $row['minGasPrice']. "</td>");
                        echo("<td>". $row['totBlocks']. "</td>");
                        echo("<td>". $row['emptyBlocks']. "</td>");
                        echo("<td>". round($row['pctTot'],1). "</td>");
                        echo("<td>". round($row['pctTxBlocks'],1). "</td>");

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
