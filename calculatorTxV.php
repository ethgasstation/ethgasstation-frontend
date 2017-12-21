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
                <p class="navbar-text navbar-left" style="padding-left: 5px"><strong><?php echo "Last update: Block <span style = 'color:#1ABB9C'> $latestblock" ?></strong></span>  
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
                          <?php echo ("(".($gpRecs2['fastest']/10)." Gwei)") ?></label>
                        </div>
                      <div class="checkbox">
                        <label>
                        <input type="checkbox" class="flat" checked="checked" id="avg"> Average
                        <?php echo ("(".($gpRecs2['average']/10)." Gwei)") ?></label>
                    </div>
                    <div class="checkbox">
                        <label>
                        <input type="checkbox" class="flat" id="cheap"> Cheap
                        <?php if ($gpRecs2['safeLow'] ==0){$gpRecs2['safeLow']=1;} echo ("(".($gpRecs2['safeLow']/10)." Gwei)") ?></label>
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
                          <td>% of last 200 blocks accpeting this gas price</td>
                          <td id="hp"></td>
                        </tr>
                        <tr>
                          <td>Transactions At or Above in Current Txpool</td>
                          <td id="txatabove"></td>
                        </tr>
                        <tr>
                          <td>Probability mined in less than 1 hour</td>
                          <td id="minedprob"></td>
                        </tr>
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

            $(document).ready(function(){
                $.ajax({
                    url: "json/predictTable.json",
		            method: "GET",
                    dataType: "json",
		            success: function(data) {
                    predictArray = data;
                    }
                })
            })


      //Curency Support
      
            $("#eur").click(function(){     
                location = "http://ethgasstation.info/calculatorTxV.php?curr=eur";                              
            });
            
            $("#usd").click(function(){
                location = "http://ethgasstation.info/calculatorTxV.php?curr=usd";
            });
          
            $("#cny").click(function(){
                location = "http://ethgasstation.info/calculatorTxV.php?curr=cny";                                      
            });

            $("#gbp").click(function(){
                location = "http://ethgasstation.info/calculatorTxV.php?curr=gbp";                       
            });

            $('input.flat').change(function(){
                $('input.flat').not(this).prop('checked',false);
            })
            $('#oth_val').change(function(){
               $('input.flat').prop('checked',false);
                $('#other').prop('checked',true);
            })
            $('#reset').click(function(){
              $('#txatabove').html("");
              $('#minedprob').html("");
              $('#hp').html("");
              $('#meanBlocks').html("");
              $('#meanSecs').html("");
              $('#txEth').html("");
              $('#txFiat').html("");
              $('#txArgs').html("Predictions:");
              $("#oth_val").parent().next(".validation").remove();
              $("#gas_used").parent().next(".validation").remove();
            })
  
            function estimateWait (gasprice, gasoffered)
            {
                for(var i=0; i < predictArray.length; i++){
                    if (predictArray[i]['gasprice'] == gasprice){
                        break;
                    }
                }
                intercept = 4.2794;
                hpa = .0329;
                hgo = -3.2836;
                wb = -0.0048;
                tx = -0.0004;

                intercept2 = 1.9611;
                hpa_coef = -0.0147;
                txatabove_coef= 0.0007;
                high_gas_coef = .2592;

                if (gasoffered > 1000000){    
                  sum1 = intercept + (predictArray[i]['hashpower_accepting'] * hpa) + hgo  + (predictArray[i]['tx_atabove'] * tx);

                  sum2 = intercept2 + (predictArray[i]['hashpower_accepting'] * hpa_coef) + (predictArray[i]['tx_atabove'] * txatabove_coef) + high_gas_coef;
                }
                else {
                  sum1 = intercept + (predictArray[i]['hashpower_accepting'] * hpa) + (predictArray[i]['tx_atabove'] * tx);

                  sum2 = intercept2 + (predictArray[i]['tx_atabove'] * txatabove_coef) + (predictArray[i]['hashpower_accepting'] * hpa_coef);
                }

                factor = Math.exp(-1*sum1);
                prob = 1 / (1+factor);
                if (prob > .95){
                  minedProb = 'Very High';
                }
                else if (prob > .9 && prob <=.95){
                  minedProb = 'Medium'
                }
                else{
                  minedProb = 'Low';
                }
                expectedWait = Math.exp(sum2);
                if (expectedWait < 2){
                  expectedWait = 2;
                }
            
                if (gasoffered > 2000000){
                  expectedWait += 100;
                }

                return [expectedWait, predictArray[i]['hashpower_accepting'], predictArray[i]['tx_atabove'], minedProb];
            }

            $('form').submit(function(event){
              
              //Error Check
              if(!$('#gas_used').val()){
                $("#gas_used").parent().next(".validation").remove();
                txGasUsed = 21000;
              }
              else if ($('#gas_used').val() > 6700000){
                if ($("#gas_used").parent().next(".validation").length == 0){
                  $string = "<div class='validation' style='color:red;margin-bottom: 20px;'>Please enter gas used less than 6,700,000 (block limit)";
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
                if (!otherGasPrice || otherGasPrice < <?php echo($gpRecs2['safeLow']/10) ?>)
                {
                    if ($("#oth_val").parent().next(".validation").length == 0){ // only add if not added
                      $("#oth_val").parent().after("<div class='validation' style='color:red;margin-bottom: 20px;'>Please enter gas price >= <?php echo($gpRecs2['safeLow']/10)?> gwei</div>");
                    }
                    event.preventDefault(); // prevent form from POST to server
                    $('#oth_val').focus();
                    focusSet = true;
                    return;
                } 
                else {
                $("#oth_val").parent().next(".validation").remove();//remove it
                txGasPrice = $("#oth_val").val();
                }
              }
              else {
                if ($('#fast').prop('checked')===true){
                  txGasPrice = <?php echo($gpRecs2['fastest']/10) ?>;
                }
                else if ($('#avg').prop('checked')===true){
                  txGasPrice = <?php echo($gpRecs2['average']/10) ?>;
                  
                }
                else if ($('#cheap').prop('checked')===true){
                  txGasPrice = <?php echo($gpRecs2['safeLow']/10) ?>;
                }
               $('#oth_val').val("");
               $("#oth_val").parent().next(".validation").remove();
              }

              event.preventDefault();
              txArgs = "Predictions: <small><span style='color:red'> Gas Used = "+ txGasUsed + "; Gas Price = " + txGasPrice + " gwei</span></small>";
              $('#txArgs').html(txArgs);
              
              pdValues = estimateWait(txGasPrice, txGasUsed);
              console.log(pdValues);
              blocksWait = pdValues[0];
              hashpower = pdValues[1];
              txatabove = pdValues[2];
              minedprob = pdValues[3];
              console.log(blocksWait);

              currency = '<?php echo ($currency) ?>';
              console.log(currency);
              exchangeRate =<?php echo ($exchangeRate) ?>;
              blockInterval = <?php echo ($gpRecs2['block_time']) ?>;
              txMeanSecs = blocksWait * blockInterval;
              txMeanSecs = Number(txMeanSecs.toFixed(0));
              blocksWait = Number(blocksWait.toFixed(1));
      
              
              txFeeEth = txGasPrice/1e9 * txGasUsed;
              txFeeEth = Number((txFeeEth).toFixed(7))
              txFeeFiat = txFeeEth * exchangeRate;
              txFeeFiat = Number(txFeeFiat.toFixed(5));

              $('#meanBlocks').html(blocksWait);
              $('#hp').html(hashpower);
              $('#txatabove').html(txatabove);
              $('#minedprob').html(minedprob);
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
