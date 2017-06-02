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
    <?php include 'build/php/profits.php'; ?>

   


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
                <li class="dropdown">
                  <a href="#" class="user-profile dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-globe"></i><span style="color:#768399"> Change Currency</span>
                    <span class=" fa fa-angle-down"></span>
                  </a>
                  <ul class="dropdown-menu">
                    <li id="usd"><a href="#"> USD<?php if($currency=='usd'){echo'<span class="pull-right"><i class="fa fa-check"></i></span>';}?></a></li>
                    <li id="eur"><a href="#"> EUR<?php if($currency=='eur'){echo'<span class="pull-right"><i class="fa fa-check"></i></span>';}?></a></li>
                    <li id="gbp"><a href="#"> GBP<?php if($currency=='gbp'){echo'<span class="pull-right"><i class="fa fa-check"></i></span>';}?></a></li>
                    <li id="cny"><a href="#"> CNY<?php if($currency=='cny'){echo'<span class="pull-right"><i class="fa fa-check"></i></span>';}?></a></li>
                  </ul>
                </li>
                <p class="navbar-text navbar-left" style="padding-left: 5px"><strong><?php $latestblock = $latestblock - ($latestblock % 1000); echo "Estimates over last 100,000 blocks - Last update: Block <span style = 'color:#1ABB9C'> $latestblock" ?></strong></span>  
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
                    <h4>Miner Block Gas Stats <small>(gas x 1e6 per block)</small></h4>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                  <table class="table table-striped">
                      <thead>
                        <tr>
                          <th>Miner</th>
                          <th>Total Blocks</th>
                          <th>Total Uncles</th>
                          <th>Uncle Rate</th>
                          <th>Low Gas</th>
                          <th>High Gas</th>
                          <th>Median Gas</th>
                          <th>Avg Gas</th>
                          <th>Avg Gas<br>Main Block</th>
                          <th>Avg Gas<br>Uncle</th>
                        </tr>
                      </thead>
                      <tbody>
                      <?php
                      foreach ($profitTable as $row){
                        echo('<tr>');
                        echo("<td>". $row['miner']. "</td>");
                        echo("<td>". $row['totalBlocks']). "</td>";
                        echo("<td>". $row['uncles']). "</td>";
                        echo("<td>". number_format($row['uncRate'],3). "</td>");
                        echo("<td>". number_format($row['minGas'],3). "</td>");
                        echo("<td>". number_format($row['maxGas'],3). "</td>");
                        echo("<td>". number_format($row['medGas'],3). "</td>");
                        echo("<td>". number_format($row['avgmGas'],3). "</td>"); 
                        echo("<td>". number_format($row['avgMainGas'],3). "</td>");
                        echo("<td>". number_format($row['avgUncleGas'],3). "</td>");
                        echo('</tr>');

                      }
                      ?>
                      </tbody>
                    </table>

                 </div>
        </div>

            <div class="row">
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel tile fixed_height_420">
                  <div class="x_title">
                    <h4>Miner Gas Profits <small> Note: differences in miner break even price may be due to random chance</small></h4>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                  <table class="table table-striped">
                      <thead>
                        <tr>
                          <th>Miner</th>
                          <th>Uncle Award</th>
                          <th>Main Award w/o Gas Fees</th>
                          <th>Predicted All Empty Award<sup>1</sup></th>
                          <th>Block Award at Avg Gas Used<sup>2</sup></th>
                          <th>Gas Revenue (ETH)<sup>3</sup></th>
                          <th>Gas Profit (ETH)<sup>3</sup></th>
                          <th>Gas Profit (Fiat)</th>
                          <th>Gas Profit % of Total<sup>6</sup></th>
                        </tr>
                      </thead>
                      <tbody>
                      <?php
                      foreach ($profitTable as $row){
                        echo('<tr>');
                        echo("<td>". $row['miner']. "</td>");
                        echo("<td>". number_format($row['avgUncleReward'],2). "</td>");
                        echo("<td>". number_format($row['avgMainRewardwoFee'],3). "</td>");
                        echo("<td>". number_format($row['predictEmpAward'],3). "</td>");
                        echo("<td>". number_format($row['actualTxAward'],3). "</td>"); 
                        echo("<td>". number_format($row['avgTxFees'],3). "</td>");
                        echo("<td>". number_format($row['profit'],3). "</td>");
                        $profitFiat = $row['profit']*$exchangeRate;
                        echo("<td>". $currSymbol.number_format($profitFiat,2). "</td>");
                        echo("<td>". number_format($row['profitPct'],3). "</td>");
                        echo('</tr>');

                      }
                      ?>
                      </tbody>
                    </table>
                    <p>Notes:</p>
                    <p>1: The weighted average block award at the expected ratio of uncles/main blocks if mining all empty blocks</p>
                    <p>2: The weigthed average block award at the miner's observed ratio of uncles/main blocks in the dataset</p>
                    <p>3: The average gross revenue per block from transaction fees </p>
                    <p>4: The profit per block from mining gas after adjusting for its impact on the miner's uncle rate</p>
                    <p>5: The % of the miner's total block revenue coming from the uncle-adjusted profit of gas mining</p>

             </div>    
        </div>
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

            $("#eur").click(function(){     
                location = "http://ethgasstation.info/minerProfits.php?curr=eur";                              
            });
            
            $("#usd").click(function(){
                location = "http://ethgasstation.info/minerProfits.php?curr=usd";
            });
          
            $("#cny").click(function(){
                location = "http://ethgasstation.info/minerProfits.php?curr=cny";                                      
            });

            $("#gbp").click(function(){
                location = "http://ethgasstation.info/minerProfits.php?curr=gbp";                       
            });
      
      </script>



    <script src="build/js/custom3.js"></script>
    
	
  </body>
</html>
