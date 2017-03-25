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
    <!-- NProgress -->
    <link href="vendors/nprogress/nprogress.css" rel="stylesheet">
    <!-- iCheck -->
    <link href="vendors/iCheck/skins/flat/green.css" rel="stylesheet">

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
	
    <!-- bootstrap-progressbar -->
    <link href="vendors/bootstrap-progressbar/css/bootstrap-progressbar-3.3.4.min.css" rel="stylesheet">
    <!-- JQVMap -->
    <link href="vendors/jqvmap/dist/jqvmap.min.css" rel="stylesheet"/>
    <!-- bootstrap-daterangepicker -->
    <link href="vendors/bootstrap-daterangepicker/daterangepicker.css" rel="stylesheet">

    <!-- Custom Theme Style -->
    <link href="build/css/custom.css" rel="stylesheet">
     <?php include 'build/js/data.php'; ?>

    <script type="text/javascript" src="speedometer/xcanvas.js"></script>
    <script type="text/javascript" src="speedometer/tbe.js"></script>

    <script type="text/javascript" src="speedometer/digitaldisplay.js"></script>
    <script type="text/javascript" src="speedometer/speedometer.js"></script>
    <script type="text/javascript" src="speedometer/themes/default.js"></script>
    <script type="text/javascript" src="speedometer/controls.js"></script>


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
                  <li><a><i class="fa fa-paw"></i> Gas Blog<span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="speeding_up_tx.html">Speeding up ETH transactions</a></li>
                    </ul>
                  </li>
                  <li><a><i class="fa fa-question"></i> About This Site <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="FAQpage.html">FAQ</a></li>
                    </ul>
                  </li>
                  <li><a><i class="fa fa-link"></i> External Links <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="https://coincenter.org/entry/what-is-ethereum" target="_blank">What is Ethereum?</a></li>
                      <li><a href="https://www.ethereum.org/" target="_blank">Ethereum Foundation</a></li>
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
                <li class="dropdown">
                  <a href="#" class="user-profile dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-globe"></i><span style="color:#768399"> Change Currency</span>
                    <span class=" fa fa-angle-down"></span>
                  </a>
                  <ul class="dropdown-menu">
                    <li id="usd"><a href="#"> USD<span class="pull-right"><i class="fa fa-check"></i></span></a></li>
                    <li id="eur"><a href="#"> EUR</a></li>
                    <li id="gbp"><a href="#"> GBP</a></li>
                    <li id="cny"><a href="#"> CNY</a></li>
                  </ul>
                </li>
              <p class="navbar-text navbar-left" style="padding-left: 5px"><strong><?php echo "Estimates over last 10,000 blocks - Last update: Block <span style = 'color:#1ABB9C'> $latestblock" ?></strong></span>  
              </p>
            </ul>
            </nav>
          </div>
         </div>

        <!-- /top navigation -->

        <!-- page content -->
        <div class="right_col" role="main">

          <!-- top tiles -->
          <div class="row tile_count">
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
              <span class="count_top"><i class="fa fa-space-shuttle"></i>Median Cost for Transfer</span>
              <div class="count" id="medTx"><> </div>
            </div>
             <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
              <span class="count_top"><i class="fa fa-clock-o"></i> Median Wait (s)</span>
              <div class="count"><?php echo "$medianwaitsec" ?></div>
            </div>
             <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
              <span class="count_top"><i class="fa fa-clock-o"></i> Median Wait (blocks)</span>
              <div class="count"><?php echo "$medianwaitblock" ?></div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
              <span class="count_top"><i class="fa fa-tachometer"></i> Gas Price High (Gwei)</span>
              <div class="count red"><?php echo "$gaspricehigh" ?></div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
              <span class="count_top"><i class="fa fa-tachometer"></i> Gas Price Mid (Gwei)</span>
              <div class="count"><?php echo "$gaspricemedian" ?></div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
              <span class="count_top"><i class="fa fa-tachometer"></i> Gas Price Low (Gwei)</span>
              <div class="count green"><?php echo "$gaspricelow" ?></div>
            </div>
          </div>
          <!-- /top tiles -->

          <div class="row">

          <!-- Network Activity Graph -->
             <div class="col-md-8 col-sm-12 col-xs-12">
                 <div class="x_panel tile fixed_height_320">
                     <div class="x_title">
                        <h4>Recent Network Activity: <small>Gas Demand / Average Wait Time (100 block intervals)</small></h4>
                        <div class="clearfix"></div>
                     </div>
                     <div class="x_content">
                        <canvas id="lineChart" height="100" ></canvas> 
                        <div class="clearfix"></div> 
                    </div> 
                </div>
            </div>
          <!-- /network activity graph -->

          <!-- Speedometer -->
            <div class="col-md-4 col-sm-4 col-xs-12">
              <div class="x_panel tile fixed_height_320">
                <div class="x_title">
                  <h4>Real Time Gas Use: <small>% Block Limit (last 10)</small></h4>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                    <div id="speedometer" class="speedometer"></div>
                    <p id="blockNum">Last Block: </p> 
                </div>
              </div>
            </div>
          <!--/Speedometer -->

       </div>

       <!-- Transactions by Gas Price -->

        <div class="row">

            <div class="col-md-4 col-sm-6 col-xs-12">
              <div class="x_panel tile fixed_height_320">
                <div class="x_title">
                  <h4>Transaction Count by Gas Price</h4>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <canvas id="mybarChart2" height="200"></canvas>
                </div>
              </div>
            </div>
        <!-- /Transaction by Gas Price -->

        <!-- Confirmation Time by Gas Price -->

            <div class="col-md-4 col-sm-4 col-xs-12">
              <div class="x_panel tile fixed_height_320 overflow_hidden">
                <div class="x_title">
                  <h4>Confirmation Time by Gas Price</h4>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                        <canvas id="mybarChart" height="200"></canvas>
                  </div>
                </div>
              </div>

        <!-- /confirmation time -->

          <!-- Recommended User Gas Prices-->
           
             <div class="col-md-4 col-sm-4 col-xs-12">
              <div class="x_panel tile fixed_height_320">
                <div class="x_title">
                      <h4>Recommended User Gas Prices</h4>
                      <div class="clearfix"></div>
                    </div>
                    <div class="x_content">
                    <table class="table table-bordered">
                      <thead>
                        <tr>
                          <th>Desired Tx Speed</th>
                          <th>Gas Price (gwei)</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>Cheapest</td>
                          <td style = "color:#03586A" ><?php echo "$lowPrice" ?></td>
                        </tr>
                        <tr>
                          <td>At cost</td>
                          <td style = "color:#03586A" ><?php echo "15" ?></td>
                        </tr>
                        <tr>
                          <td>Average</td>
                          <td style = "color:#03586A"><?php echo "$recPrice" ?></td>
                        </tr>
                        <tr>
                          <td>Fastest</td>
                          <td style = "color:red"><?php echo "$highPrice" ?></td>
                        </tr>
                      </tbody>
                    </table>
                </div>
             </div> 
          </div>
          <div class="clearfix"></div>
        </div>

        <!-- /Recommended prices -->


  <div class="row">

        <!-- Miner Rankings -->

            <div class="col-md-8 col-sm-12 col-xs-12">
              <div class="x_panel tile fixed_height_420">
                <div class="x_title">
                  <h4>Miner Rankings: <small> Support for user transactions</small></h4>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <table class="table table-bordered">
                      <thead>
                        <tr>
                          <th>Miner</th>
                          <th>Lowest gas price (gwei)</th>
                          <th>% of blocks empty</th>
                          <th>% of total blocks</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td><?php echo "{$miners[0]['name']}" ?></td>
                          <td><?php echo "{$miners[0]['minP']}" ?></td>
                          <td><?php $pct = round($miners[0]['pctEmp'],2)*100 ; echo"$pct"; ?></td>
                          <td><?php $pct = round($miners[0]['pctTot'],2)*100 ; echo"$pct"; ?></td>
                        </tr>
                        <tr>
                          <td><?php echo "{$miners[1]['name']}" ?></td>
                          <td><?php echo "{$miners[1]['minP']}" ?></td>
                          <td><?php $pct = round($miners[1]['pctEmp'],2)*100 ; echo"$pct"; ?></td>
                          <td><?php $pct = round($miners[1]['pctTot'],2)*100 ; echo"$pct"; ?></td>
                        </tr>
                         <tr>
                          <td><?php echo "{$miners[2]['name']}" ?></td>
                          <td><?php echo "{$miners[2]['minP']}" ?></td>
                          <td><?php $pct = round($miners[2]['pctEmp'],2)*100 ; echo"$pct"; ?></td>
                          <td><?php $pct = round($miners[2]['pctTot'],2)*100 ; echo"$pct"; ?></td>
                        </tr>
                         <tr>
                          <td><?php echo "{$miners[3]['name']}" ?></td>
                          <td><?php echo "{$miners[3]['minP']}" ?></td>
                          <td><?php $pct = round($miners[3]['pctEmp'],2)*100 ; echo"$pct"; ?></td>
                          <td><?php $pct = round($miners[3]['pctTot'],2)*100 ; echo"$pct"; ?></td>
                        </tr>
                          <tr>
                          <td><?php echo "{$miners[4]['name']}" ?></td>
                          <td><?php echo "{$miners[4]['minP']}" ?></td>
                          <td><?php $pct = round($miners[4]['pctEmp'],2)*100 ; echo"$pct"; ?></td>
                          <td><?php $pct = round($miners[4]['pctTot'],2)*100 ; echo"$pct"; ?></td>
                        </tr>
                         <tr>
                          <td><?php echo "{$miners[5]['name']}" ?></td>
                          <td><?php echo "{$miners[5]['minP']}" ?></td>
                          <td><?php $pct = round($miners[5]['pctEmp'],2)*100 ; echo"$pct"; ?></td>
                          <td><?php $pct = round($miners[5]['pctTot'],2)*100 ; echo"$pct"; ?></td>
                        </tr>
                         <tr>
                          <td><?php echo "{$miners[6]['name']}" ?></td>
                          <td><?php echo "{$miners[6]['minP']}" ?></td>
                          <td><?php $pct = round($miners[6]['pctEmp'],2)*100 ; echo"$pct"; ?></td>
                          <td><?php $pct = round($miners[6]['pctTot'],2)*100 ; echo"$pct"; ?></td>
                        </tr>
                         <tr>
                          <td><?php echo "{$miners[7]['name']}" ?></td>
                          <td><?php echo "{$miners[7]['minP']}" ?></td>
                          <td><?php $pct = round($miners[7]['pctEmp'],2)*100 ; echo"$pct"; ?></td>
                          <td><?php $pct = round($miners[7]['pctTot'],2)*100 ; echo"$pct"; ?></td>
                        </tr>
                         <tr>
                          <td><?php echo "{$miners[8]['name']}" ?></td>
                          <td><?php echo "{$miners[8]['minP']}" ?></td>
                          <td><?php $pct = round($miners[8]['pctEmp'],2)*100 ; echo"$pct"; ?></td>
                          <td><?php $pct = round($miners[8]['pctTot'],2)*100 ; echo"$pct"; ?></td>
                        </tr>
                         <tr>
                          <td><?php echo "{$miners[9]['name']}" ?></td>
                          <td><?php echo "{$miners[9]['minP']}" ?></td>
                          <td><?php $pct = round($miners[9]['pctEmp'],2)*100 ; echo"$pct"; ?></td>
                          <td><?php $pct = round($miners[9]['pctTot'],2)*100 ; echo"$pct"; ?></td>
                        </tr>
                      </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- /miner rankings -->

        <!-- Misc Transaction Table -->

            <div class="col-md-4 col-sm-4 col-xs-12">
              <div class="x_panel tile fixed_height_420">
                <div class="x_title">
                  <h4>Misc Transactions</h4>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <table class="table table-bordered">
                      <thead>
                        <tr>
                          <th>Category</th>
                          <th>Value</th>
                        </tr>
                      </thead>
                      <tbody> 
                        <tr>
                          <td>Cheapest Transfer Fee</td>
                          <td id="cheapestTransfer"><?php echo '<a href="https://etherscan.io/tx/' .$cheapestTxId.'"'; echo "target=\"_blank\">$cheapUSD</a>";?></td>
                    
                        </tr>
                        <tr>
                          <td>Priciest Transfer Fee</td>
                          <td id="priciestTransfer"><?php echo '<a href="https://etherscan.io/tx/' .$dearestTxId.'"'."target=\"_blank\">$dearUSD</a>"?></td>
                          
                        </tr>
                        <tr>
                          <td>Priciest Transaction Fee</td>
                          <td id="priciestTransaction"><?php echo '<a href="https://etherscan.io/tx/' .$dearestConId.'"'."target=\"_blank\" >$dearconUSD</a>"?></td>
                          
                        </tr>
                        <tr>
                          <td>Contracts: Median Gas Used</td>
                          <td><?php echo "$medianContractGas";?></td>
                        </tr>
                        <tr>
                          <td>Contracts: Median Fee</td>
                          <td id="medianContractFee"><?php setlocale(LC_MONETARY, "en_US.UTF-8");echo money_format('%.2n', $medianConFeeUSD);?></td>
                        </tr>
                        <tr>
                          <td>Total Transactions (last 10k blocks)</td>
                          <td><?php echo "$totTx";?></td>
                        </tr>
                        <tr>
                          <td>Total Transfers</td>
                          <td><?php echo "$totalTransfers"; $perTr =round($totalTransfers/$totTx*100); echo " ("."$perTr"."%)"?></td>
                        </tr>
                        <tr>
                          <td>Total Contract Calls</td>
                          <td><?php echo "$totalConCalls"; $perCon =round($totalConCalls/$totTx*100); echo " ("."$perCon"."%)"?></td>
                        </tr>
                        <tr>
                          <td>Total Timed Transactions</td>
                          <td><?php echo "$totalTimed"; $perTimed =round($totalTimed/$totTx*100); echo " ("."$perTimed"."%)"?></td>
                        </tr>
                      </tbody>
                    </table>
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

    //Data for Transaction Count by Gas Price Graph

        if ($('#mybarChart2').length ){ 
			  
			  var ctx = document.getElementById("mybarChart2");
			  var mybarChart = new Chart(ctx, {
				type: 'bar',
				data: {
				  labels: ["<15", "15-20", "20", ">20-30", ">30"],
				  datasets: [{
                    label: "Percent of transactions",  
					backgroundColor: "#26B99A",
					data: <?php echo '[' . $cat1TxPct. ',' . $cat2TxPct . ',' . $cat3TxPct . ',' . $cat4TxPct . ','. $cat5TxPct .']'; ?>
				  }], 
				},

				options: {
                    legend: {
                        display: false
                    },
				  scales: {
					yAxes: [{
					  ticks: {
						beginAtZero: true
					  },
						scaleLabel:{
							display:true,
							labelString:"% of transactions"
						}
					}],
					xAxes:[{
						scaleLabel:{
							display:true,
							labelString:"Gas price category"
						}

					}]
				  }
				}
			  });
        }

        //Data for Confirmation Time by Gas Price Graph

        if ($('#mybarChart').length ){ 
			  
			  var ctx = document.getElementById("mybarChart");
			  var mybarChart = new Chart(ctx, {
				type: 'bar',
				data: {
				  labels: ["<15","15-20", "20", "20-30", ">30"],
				  datasets: [{
					label: 'Median- Time to Confirm',
					backgroundColor: "#26B99A",
					data: <?php echo '[' . $cat1TimeMedMin. ',' . $cat2TimeMedMin . ',' . $cat3TimeMedMin . ',' . $cat4TimeMedMin . ','. $cat5TimeMedMin .']'; ?>
				  }, {
					label: '95pctl- Time to Confirm',
					backgroundColor: "#03586A",
					data: <?php echo '[' . $cat1Time95Min. ',' . $cat2Time95Min . ',' . $cat3Time95Min . ',' . $cat4Time95Min . ','. $cat5Time95Min .']'; ?>
				  }]
				},

				options: {
                    legend: {
                        display: false
                    },
				  scales: {
					yAxes: [{
					  ticks: {
						beginAtZero: true
					  },
						scaleLabel:{
							display:true,
							labelString:"Time to Confirm (min)"
						}
					}],
					xAxes:[{
						scaleLabel:{
							display:true,
							labelString:"Gas price category"
						}

					}]
				  }
				}
			  });
			  
			} 

      //Data for Network Activity Graph
      			 
			if ($('#lineChart').length ){	
			
			  var ctx = document.getElementById("lineChart");
			  var lineChart = new Chart(ctx, {
				type: 'line',
				data: {
				  labels: <?php echo '[' . $x1. ',' . ' ' . ','. ' '. ','. ' ' . ',' . ' '. ',' . ' ' . ','. ' '. ','. ' ' . ',' . ' '. ','. $x10 . ',' . ' ' . ','. ' '. ','. ' ' . ',' . ' '. ','. ' ' . ','. ' '. ','. ' ' . ',' . ' '. ','. ' '. ','. $x20.']'; ?>,
				  datasets: [{
					label: "Avg Tx Fees Per Block (ETH)",
					yAxisID: 'A',
					backgroundColor: "rgba(38, 185, 154, 0.31)",
					borderColor: "rgba(38, 185, 154, 0.7)",
					pointBorderColor: "rgba(38, 185, 154, 0.7)",
					pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
					pointHoverBackgroundColor: "#fff",
					pointHoverBorderColor: "rgba(220,220,220,1)",
					pointBorderWidth: 1,
					pointHoverRadius:5,
					pointHitRadius:10,
					data: <?php echo '[' . $ya1. ',' . $ya2 . ',' . $ya3 . ',' . $ya4 . ',' . $ya5 . ',' . $ya6 . ',' . $ya7 .',' . $ya8 . ',' . $ya9 . ',' . $ya10. ',' .$ya11. ',' .$ya12. ',' . $ya13 . ',' . $ya14 . ',' . $ya15 .',' . $ya16 . ',' . $ya17 . ',' . $ya18. ',' .$ya19. ',' .$ya20. ']'; ?>
				  }, {
					label: "Median Confirm Time (s)",
					yAxisID: 'B',
					backgroundColor: "rgba(3, 88, 106, 0.3)",
					borderColor: "rgba(3, 88, 106, 0.70)",
					pointBorderColor: "rgba(3, 88, 106, 0.70)",
					pointBackgroundColor: "rgba(3, 88, 106, 0.70)",
					pointHoverBackgroundColor: "#fff",
					pointHoverBorderColor: "rgba(151,187,205,1)",
					pointBorderWidth: 1,
					data: <?php echo '[' . $yb1. ',' . $yb2 . ',' . $yb3 . ',' . $yb4 . ',' . $yb5 . ',' . $yb6 . ',' . $yb7 .',' . $yb8 . ',' . $yb9 . ',' . $yb10. ','. $yb11. ',' .$yb12. ',' . $yb13 . ',' . $yb14 . ',' . $yb15 .',' . $yb16 . ',' . $yb17 . ',' . $yb18. ',' .$yb19. ',' .$yb20. ']'; ?>
				  }]
				},
				options: {
                    legend: {
                        display: false
                    },
    			scales: {
      			yAxes: [{
       			 id: 'A',
        		 type: 'linear',
       			 position: 'left',
             ticks: {
							beginAtZero: false },
						 scaleLabel: {
							display:true,
							labelString: 'Avg Tx Fees Per Block (ETH)'	
						 }
      }, {
        		id: 'B',
        		type: 'linear',
       			position: 'right',
						ticks: {
							beginAtZero: false },
						scaleLabel: {
							display:true,
							labelString: 'Time to confirm (s)'	
						 }
					
        		
      }]
    }
  }
});

			
};

    //Speedometer
			  
          if ($('#speedometer').length ){
              var speedometer;
              speedometer = new Speedometer ('speedometer', {theme: 'default'});
              speedometer.draw ();
              getSpeed();
              setInterval(getSpeed,5000);
              
               }


          function getSpeed (){

          
                    $.ajax({
		                      url: "build/js/speedo.php",
		                      method: "GET",
                              dataType: "json",
		                      success: function(data) {
			                    var blockNum = data[0]['blockNum'];
                                var speed = data[1]['average'];
                                var speedFloat = parseFloat(speed,10) * 100;
                                var speedInt = Math.round(speedFloat);
                                updateSpeedo (speedInt,blockNum);
                                var out = "Last Block: " + blockNum;
                                $('#blockNum').text(out);
                                
                          }               
                
                    });
          };

          function updateSpeedo (speedInt, blockNum){

            var curSpeed = speedometer.value();

            if (curSpeed === speedInt){
                return;

            } 
            else {
                speedometer.animatedUpdate(speedInt,1000);
            }
            


          }

      //Curency Support

      $(document).ready(function(){

        var currency = <?php echo "$currency";?>;
        console.log("currency" + currency);

        if (currency === "eur"){
          currencyEUR();}
        else if (currency === "gbp"){
          currencyGBP();}
        else if (currency === "cny"){
          currencyCNY();}
        else {currencyUSD();} 

      });


      function currencyEUR(){
                var eurfee = <?php echo "$medianfeeEUR";?>;
                var cheapestTxEUR = <?php echo "$cheapestTxEUR";?>;
                var dearestTxEUR = <?php echo "$dearestTxEUR";?>;
                var dearestConEUR = <?php echo "$dearestConEUR";?>;
                var conFeeEUR = <?php echo "$medianConFeeEUR";?>;

                eurfee = eurfee.toFixed(4);
                cheapestTxEUR = cheapestTxEUR.toFixed(4);
                dearestTxEUR = dearestTxEUR.toFixed(2);
                dearestConEUR = dearestConEUR.toFixed(2);
                conFeeEUR = conFeeEUR.toFixed(2);

                $('#medTx').text("€" + eurfee);

                $('#cheapestTransfer').text("€" + cheapestTxEUR);
                $('#priciestTransfer').text("€" + dearestTxEUR);
                $('#priciestTransaction').text("€" + dearestConEUR);
                $('#medianContractFee').text("€" + conFeeEUR);

                $('#usd').html('<a href="#"> USD</a>');
                $('#eur').html('<a href="#"> EUR<span class="pull-right"><i class="fa fa-check"></i></span></a>');
                $('#gbp').html('<a href="#"> GBP</a>');
                $('#cny').html('<a href="#"> CNY</a>');
                                                                     

      }

      function currencyUSD(){
                var usdfee = <?php echo "$medianfeeUSD";?>;
                var cheapestTxUSD = <?php echo "$cheapestTxUsd";?>;
                var dearestTxUSD = <?php echo "$dearestTxUsd";?>;
                var dearestConUSD = <?php echo "$dearestConUsd";?>;
                var conFeeUSD = <?php echo "$medianConFeeUSD";?>;

                usdfee = usdfee.toFixed(4);
                cheapestTxUSD = cheapestTxUSD.toFixed(4);
                dearestTxUSD = dearestTxUSD.toFixed(2);
                dearestConUSD = dearestConUSD.toFixed(2);
                conFeeUSD = conFeeUSD.toFixed(2);

                $('#medTx').text("$" + usdfee);

                $('#cheapestTransfer').text("$" + cheapestTxUSD);
                $('#priciestTransfer').text("$" + dearestTxUSD);
                $('#priciestTransaction').text("$" + dearestConUSD);
                $('#medianContractFee').text("$" + conFeeUSD);

                $('#usd').html('<a href="#"> USD<span class="pull-right"><i class="fa fa-check"></i></span></a>');
                $('#eur').html('<a href="#"> EUR</a>');
                $('#gbp').html('<a href="#"> GBP</a>');
                $('#cny').html('<a href="#"> CNY</a>');


      }

      function currencyCNY(){
                var cnyfee = <?php echo "$medianfeeCNY";?>;
                var cheapestTxCNY = <?php echo "$cheapestTxCNY";?>;
                var dearestTxCNY = <?php echo "$dearestTxCNY";?>;
                var dearestConCNY = <?php echo "$dearestConCNY";?>;
                var conFeeCNY = <?php echo "$medianConFeeCNY";?>;

                cnyfee = cnyfee.toFixed(4);
                cheapestTxCNY = cheapestTxCNY.toFixed(4);
                dearestTxCNY = dearestTxCNY.toFixed(2);
                dearestConCNY = dearestConCNY.toFixed(2);
                conFeeCNY = conFeeCNY.toFixed(2);

                $('#medTx').text("¥" + cnyfee);
                $('#cheapestTransfer').text("¥" + cheapestTxCNY);
                $('#priciestTransfer').text("¥" + dearestTxCNY);
                $('#priciestTransaction').text("¥" + dearestConCNY);
                $('#medianContractFee').text("¥" + conFeeCNY);

                $('#usd').html('<a href="#"> USD</a>');
                $('#eur').html('<a href="#"> EUR</a>');
                $('#gbp').html('<a href="#"> GBP</a>');
                $('#cny').html('<a href="#"> CNY<span class="pull-right"><i class="fa fa-check"></i></span></a>');
      }

      function currencyGBP(){
                var gbpfee = <?php echo "$medianfeeGBP";?>;
                var cheapestTxGBP = <?php echo "$cheapestTxGBP";?>;
                var dearestTxGBP = <?php echo "$dearestTxGBP";?>;
                var dearestConGBP = <?php echo "$dearestConGBP";?>;
                var conFeeGBP = <?php echo "$medianConFeeGBP";?>;

                gbpfee = gbpfee.toFixed(4);
                cheapestTxGBP = cheapestTxGBP.toFixed(4);
                dearestTxGBP = dearestTxGBP.toFixed(2);
                dearestConGBP = dearestConGBP.toFixed(2);
                conFeeGBP = conFeeGBP.toFixed(2);

                $('#medTx').text("£" + gbpfee);
                $('#cheapestTransfer').text("£" + cheapestTxGBP);
                $('#priciestTransfer').text("£" + dearestTxGBP);
                $('#priciestTransaction').text("£" + dearestConGBP);
                $('#medianContractFee').text("£" + conFeeGBP);
                

                $('#usd').html('<a href="#"> USD</a>');
                $('#eur').html('<a href="#"> EUR</a>');
                $('#gbp').html('<a href="#"> GBP<span class="pull-right"><i class="fa fa-check"></i></span></a>');
                $('#cny').html('<a href="#"> CNY</a>');
      }
      
            $("#eur").click(function(){
                 
                location = "http://24.218.144.115/index.php?curr=eur";
			          var eurfee = <?php echo "$medianfeeEUR";?>;
                var cheapestTxEUR = <?php echo "$cheapestTxEUR";?>;
                var dearestTxEUR = <?php echo "$dearestTxEUR";?>;
                var dearestConEUR = <?php echo "$dearestConEUR";?>;
                var conFeeEUR = <?php echo "$medianConFeeEUR";?>;

                eurfee = eurfee.toFixed(4);
                cheapestTxEUR = cheapestTxEUR.toFixed(4);
                dearestTxEUR = dearestTxEUR.toFixed(2);
                dearestConEUR = dearestConEUR.toFixed(2);
                conFeeEUR = conFeeEUR.toFixed(2);

                $('#medTx').text("€" + eurfee);

                $('#cheapestTransfer').text("€" + cheapestTxEUR);
                $('#priciestTransfer').text("€" + dearestTxEUR);
                $('#priciestTransaction').text("€" + dearestConEUR);
                $('#medianContractFee').text("€" + conFeeEUR);

                $('#usd').html('<a href="#"> USD</a>');
                $('#eur').html('<a href="#"> EUR<span class="pull-right"><i class="fa fa-check"></i></span></a>');
                $('#gbp').html('<a href="#"> GBP</a>');
                $('#cny').html('<a href="#"> CNY</a>');
                                                                     
            });
            
            $("#usd").click(function(){
                 
                
			          var usdfee = <?php echo "$medianfeeUSD";?>;
                var cheapestTxUSD = <?php echo "$cheapestTxUsd";?>;
                var dearestTxUSD = <?php echo "$dearestTxUsd";?>;
                var dearestConUSD = <?php echo "$dearestConUsd";?>;
                var conFeeUSD = <?php echo "$medianConFeeUSD";?>;

                usdfee = usdfee.toFixed(4);
                cheapestTxUSD = cheapestTxUSD.toFixed(4);
                dearestTxUSD = dearestTxUSD.toFixed(2);
                dearestConUSD = dearestConUSD.toFixed(2);
                conFeeUSD = conFeeUSD.toFixed(2);

                $('#medTx').text("$" + usdfee);

                $('#cheapestTransfer').text("$" + cheapestTxUSD);
                $('#priciestTransfer').text("$" + dearestTxUSD);
                $('#priciestTransaction').text("$" + dearestConUSD);
                $('#medianContractFee').text("$" + conFeeUSD);

                $('#usd').html('<a href="#"> USD<span class="pull-right"><i class="fa fa-check"></i></span></a>');
                $('#eur').html('<a href="#"> EUR</a>');
                $('#gbp').html('<a href="#"> GBP</a>');
                $('#cny').html('<a href="#"> CNY</a>');
                                                                     
            });
          
            $("#cny").click(function(){
                               
			          var cnyfee = <?php echo "$medianfeeCNY";?>;
                var cheapestTxCNY = <?php echo "$cheapestTxCNY";?>;
                var dearestTxCNY = <?php echo "$dearestTxCNY";?>;
                var dearestConCNY = <?php echo "$dearestConCNY";?>;
                var conFeeCNY = <?php echo "$medianConFeeCNY";?>;

                cnyfee = cnyfee.toFixed(4);
                cheapestTxCNY = cheapestTxCNY.toFixed(4);
                dearestTxCNY = dearestTxCNY.toFixed(2);
                dearestConCNY = dearestConCNY.toFixed(2);
                conFeeCNY = conFeeCNY.toFixed(2);

                $('#medTx').text("¥" + cnyfee);
                $('#cheapestTransfer').text("¥" + cheapestTxCNY);
                $('#priciestTransfer').text("¥" + dearestTxCNY);
                $('#priciestTransaction').text("¥" + dearestConCNY);
                $('#medianContractFee').text("¥" + conFeeCNY);

                $('#usd').html('<a href="#"> USD</a>');
                $('#eur').html('<a href="#"> EUR</a>');
                $('#gbp').html('<a href="#"> GBP</a>');
                $('#cny').html('<a href="#"> CNY<span class="pull-right"><i class="fa fa-check"></i></span></a>');
                                                                     
            });

            $("#gbp").click(function(){
                 
                
			          var gbpfee = <?php echo "$medianfeeGBP";?>;
                var cheapestTxGBP = <?php echo "$cheapestTxGBP";?>;
                var dearestTxGBP = <?php echo "$dearestTxGBP";?>;
                var dearestConGBP = <?php echo "$dearestConGBP";?>;
                var conFeeGBP = <?php echo "$medianConFeeGBP";?>;

                gbpfee = gbpfee.toFixed(4);
                cheapestTxGBP = cheapestTxGBP.toFixed(4);
                dearestTxGBP = dearestTxGBP.toFixed(2);
                dearestConGBP = dearestConGBP.toFixed(2);
                conFeeGBP = conFeeGBP.toFixed(2);

                $('#medTx').text("£" + gbpfee);
                $('#cheapestTransfer').text("£" + cheapestTxGBP);
                $('#priciestTransfer').text("£" + dearestTxGBP);
                $('#priciestTransaction').text("£" + dearestConGBP);
                $('#medianContractFee').text("£" + conFeeGBP);
                

                $('#usd').html('<a href="#"> USD</a>');
                $('#eur').html('<a href="#"> EUR</a>');
                $('#gbp').html('<a href="#"> GBP<span class="pull-right"><i class="fa fa-check"></i></span></a>');
                $('#cny').html('<a href="#"> CNY</a>');
                                                                     
            });

         



 </script>



    <script src="build/js/custom3.js"></script>
    
	
  </body>
</html>
