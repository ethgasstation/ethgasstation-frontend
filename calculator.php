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
     <?php include 'build/php/datacalc.php'; ?>

   


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
                      <li><a href="about.html"><i class="fa fa-question"></i> What Is This Site?</a></li>
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
                <p class="navbar-text navbar-left" style="padding-left: 5px"><strong><?php echo "Estimates over last 10,000 blocks - Last update: Block <span style = 'color:#1ABB9C'> $latestblock" ?></strong></span>  
              </p>
            </ul>
            </nav>
          </div>
         </div>

        <!-- /top navigation -->

        <!-- page content -->
        <div class="right_col" role="main">

        
          <div class="row">
              <div class="col-md-6 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h4>Transaction Inputs</h4>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <br />
                    <form class="form-horizontal form-label-left input_mask">
                      <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">Gas Used<span class="required">*</span></label>
                        <div class="col-md-9 col-sm-9 col-xs-12">
                          <input type="number" class="form-control" placeholder="21000" id="gas_used">
                        </div>
                      </div>
                      
                      <div class="form-group">
                        <label class="col-md-3 col-sm-3 col-xs-12 control-label">Gas Price<span class="required">*</span></label>

                      <div class="col-md-6 col-sm-6 col-xs-12">
                        <div class="checkbox">
                          <label>
                          <input type="checkbox" class="flat" id="fast"> Fastest
                          <?php echo ("(".$gasPriceRecs['Fastest']." Gwei)") ?></label>
                        </div>
                      <div class="checkbox">
                        <label>
                        <input type="checkbox" class="flat" checked="checked" id="avg"> Average
                        <?php echo ("(".$gasPriceRecs['Average']." Gwei)") ?></label>
                    </div>
                    <div class="checkbox">
                        <label>
                        <input type="checkbox" class="flat" id="cheap"> Cheapest
                        <?php echo ("(".$gasPriceRecs['Cheapest']." Gwei)") ?></label>
                    </div>
                     <div class="checkbox">
                        <label>
                        <input type="checkbox" class="flat" id="other"> Other
                        </label>
                    </div>
                    <div>
                      <input type="number" class="form-control" placeholder="(Gwei)" id="oth_val">
                    </div>
                  </div>
                </div>
                      <div class="ln_solid"></div>
                      <div class="form-group">
                        <div class="col-md-9 col-sm-9 col-xs-12 col-md-offset-3">
						              <button class="btn btn-primary" type="reset" id="reset">Reset</button>
                          <button type="submit" class="btn btn-success">Submit</button>
                        </div>
                      </div>

                    </form>
                  </div>
                </div>
            </div>

                 <div class="col-md-6 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h4 id="txArgs">Predictions:</h4>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <table class="table table-bordered">
                      <thead>
                        <tr>
                          <th>Outcome</th>
                          <th></th>
                
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>Mean Time to Confirm (Blocks)</td>
                          <td id="meanBlocks"></td>
                        </tr>
                        <tr>
                          <td>Mean Time to Confirm (Seconds)</td>
                          <td id="meanSecs"></td>
                        </tr>
                         <tr>
                          <td>Transaction fee (ETH)</td>
                          <td id="txEth"></td>
                        </tr>
                         <tr>
                          <td>Transaction fee (Fiat)</td>
                          <td id="txFiat"></td>
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


      //Curency Support
      
            $("#eur").click(function(){     
                location = "http://ethgasstation.info/calculator.php?curr=eur";                              
            });
            
            $("#usd").click(function(){
                location = "http://ethgasstation.info/calculator.php?curr=usd";
            });
          
            $("#cny").click(function(){
                location = "http://ethgasstation.info/calculator.php?curr=cny";                                      
            });

            $("#gbp").click(function(){
                location = "http://ethgasstation.info/calculator.php?curr=gbp";                       
            });

            $('input.flat').change(function(){
                $('input.flat').not(this).prop('checked',false);
            })
            $('#oth_val').change(function(){
               $('input.flat').prop('checked',false);
                $('#other').prop('checked',true);
            })
            $('#reset').click(function(){
              $('#meanBlocks').html("");
              $('#meanSecs').html("");
              $('#txEth').html("");
              $('#txFiat').html("");
              $('#txArgs').html("Predictions:");
              $("#oth_val").parent().next(".validation").remove();
              $("#gas_used").parent().next(".validation").remove();
            })
  
            function estimateWait (gCat, pCat)
            {
              paramPriceCat1 = <?php echo ($calcParams['priceCat1']) ?>;
              paramPriceCat3 = <?php echo ($calcParams['priceCat3']) ?>;
              paramPriceCat4 = <?php echo ($calcParams['priceCat4']) ?>;
              paramCons = <?php echo ($calcParams['const']) ?>;
              paramGasCat2 = <?php echo ($calcParams['gasCat2']) ?>;
              paramGasCat3 = <?php echo ($calcParams['gasCat3']) ?>;
              paramGasCat4 = <?php echo ($calcParams['gasCat4']) ?>;

              exp = paramCons + (paramPriceCat1*pCat['cat1']) + (paramPriceCat3*pCat['cat3']) + (paramPriceCat4*pCat['cat4']) + (paramGasCat2*gCat['gas2']) + (paramGasCat3*gCat['gas3']) + (paramGasCat4*gCat['gas4']); 
              
              wait = (Math.exp(exp));
              return Number(wait.toFixed(2));
            }
            
            function getPriceCats(gasPrice)
            {
              pCats= {};
              if ((gasPrice >= <?php echo($gasPriceRecs['safeLow']) ?>) && (gasPrice < <?php echo($gasPriceRecs['Average']) ?>))
              {
                pCats['cat1'] = 1;
                pCats['cat3'] = 0;
                pCats['cat4'] = 0;
              }
              else if (gasPrice == <?php echo($gasPriceRecs['Average']) ?>)
              {
                pCats['cat1'] = 0;
                pCats['cat3'] = 0;
                pCats['cat4'] = 0;
              }
              else if ((gasPrice > <?php echo($gasPriceRecs['Average']) ?>) && (gasPrice < <?php echo($gasPriceRecs['Fastest']) ?>))
              {
                pCats['cat1'] = 0;
                pCats['cat3'] = 1;
                pCats['cat4'] = 0;
              }
              else if (gasPrice >= <?php echo($gasPriceRecs['Fastest']) ?>)
              {
                pCats['cat1'] = 0;
                pCats['cat3'] = 0;
                pCats['cat4'] = 1;
              }
              return pCats;
            }

            function getGasUsedCats (gasUsed)
            { gCats={};
              if (gasUsed <= 21000)
              {
                gCats['gas2']=0;
                gCats['gas3']=0;
                gCats['gas4']=0;
              }
              else if (gasUsed > 21000 && gasUsed <= <?php echo ($calcParams['75pct'])?>)
              {
                gCats['gas2']=1;
                gCats['gas3']=0;
                gCats['gas4']=0;
              }
              else if (gasUsed > <?php echo ($calcParams['75pct'])?> && gasUsed < <?php echo ($calcParams['90pct'])?>)
              {
                gCats['gas2']=0;
                gCats['gas3']=1;
                gCats['gas4']=0;
              }
              else if (gasUsed >= <?php echo ($calcParams['90pct'])?>)
              {
                gCats['gas2']=0;
                gCats['gas3']=0;
                gCats['gas4']=1;
              }
              return gCats;
            }


            $('form').submit(function(event){
              
              //Error Check
              if(!$('#gas_used').val()){
                $("#gas_used").parent().next(".validation").remove();
                txGasUsed = 21000;
              }
              else if ($('#gas_used').val() > 4000000){
                if ($("#gas_used").parent().next(".validation").length == 0){
                  $string = "<div class='validation' style='color:red;margin-bottom: 20px;'>Please enter gas used less than 4,000,000 (block limit)";
                  $("#gas_used").parent().after($string);
                }
                event.preventDefault(); // prevent form from POST to server
                $('#gas_used').focus();
                focusSet = true;
                return;
              }
              else {
                $("#gas_used").parent().next(".validation").remove();
                txGasUsed = $('#gas_used').val();
              }
              //Gas Used Set - Now find Gas Price
              if($('#other').prop('checked')===true){
                otherGasPrice = $('#oth_val').val();
                if (!otherGasPrice || otherGasPrice < <?php echo($gasPriceRecs['safeLow']) ?>)
                {
                    if ($("#oth_val").parent().next(".validation").length == 0){ // only add if not added
                      $("#oth_val").parent().after("<div class='validation' style='color:red;margin-bottom: 20px;'>Please enter gas price >= <?php echo($gasPriceRecs['Cheapest'])?> gwei</div>");
                    }
                    event.preventDefault(); // prevent form from POST to server
                    $('#oth_val').focus();
                    focusSet = true;
                    return;
                } 
                else {
                $("#oth_val").parent().next(".validation").remove();//remove it
                txGasPrice = $("#oth_val").val();
                gCats = getGasUsedCats(txGasUsed);
                pCats = getPriceCats(txGasPrice);
                blocksWait = estimateWait(gCats, pCats);
                }
              }
              else {
                if ($('#fast').prop('checked')===true){
                  txGasPrice = <?php echo($gasPriceRecs['Fastest']) ?>;
                  gCats = getGasUsedCats(txGasUsed);
                  pCats = getPriceCats(txGasPrice);
                  blocksWait = estimateWait(gCats, pCats);
                }
                else if ($('#avg').prop('checked')===true){
                  txGasPrice = <?php echo($gasPriceRecs['Average']) ?>;
                  gCats = getGasUsedCats(txGasUsed);
                  pCats = getPriceCats(txGasPrice);
                  blocksWait = estimateWait(gCats, pCats);
                  console.log(blocksWait);
                }
                else if ($('#cheap').prop('checked')===true){
                  txGasPrice = <?php echo($gasPriceRecs['safeLow']) ?>;
                  gCats = getGasUsedCats(txGasUsed);
                  pCats = getPriceCats(txGasPrice);
                  blocksWait = estimateWait(gCats, pCats);
                }
               $('#oth_val').val("");
               $("#oth_val").parent().next(".validation").remove();
              }

              event.preventDefault();
              txArgs = "Predictions: <small><span style='color:red'> Gas Used = "+ txGasUsed + "; Gas Price = " + txGasPrice + " gwei</span></small>";
              $('#txArgs').html(txArgs);
              

              currency = '<?php echo ($currency) ?>';
              console.log(currency);
              exchangeRate =<?php echo ($exchangeRate) ?>;
              blockInterval = <?php echo ($calcParams['blockInterval']) ?>;
          

              txMeanSecs = Math.round(blocksWait*blockInterval);
              txFeeEth = txGasPrice/1e9 * txGasUsed;
              txFeeEth = Number((txFeeEth).toFixed(6))
              txFeeFiat = txFeeEth * exchangeRate;
              txFeeFiat = Number((txFeeFiat).toFixed(3));

              $('#meanBlocks').html(blocksWait);
              $('#meanSecs').html(txMeanSecs);
              $('#txEth').html(txFeeEth);
              if (currency=='usd'){
                string="$"+txFeeFiat
              $('#txFiat').html(string);
            }
              else if (currency=='eur'){
                string="€"+txFeeFiat
              $('#txFiat').html(string);
            }
              else if (currency=='cny'){
                string="¥"+txFeeFiat
              $('#txFiat').html(string);
            }
              else if (currency=='gbp'){
                string="£"+txFeeFiat
              $('#txFiat').html(string);
            }

          })



 </script>



    <script src="build/js/custom3.js"></script>
    
	
  </body>
</html>
