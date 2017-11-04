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
                <p class="navbar-text navbar-left" style="padding-left: 5px"><strong><?php echo "Last update: Block <span style = 'color:#1ABB9C'> $bnum" ?></strong></span>  
              </p>
            </ul>
            </nav>
          </div>
         </div>

        <!-- /top navigation -->

        <!-- page content -->
        <div class="right_col" role="main">
          <div class="row">
              <div class="col-md-12 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h4>Search for Transaction in the Txpool</h4>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <br />
                    <form class="form-horizontal form-label-left input_mask">
                      <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">Tx Hash<span class="required">*</span></label>
                        <div class="col-md-9 col-sm-9 col-xs-12">
                          <input type="text" class="form-control" placeholder="0x...." id="txhash">
                        </div>
                      </div> 
                  </div>
                </div>
            </div>
            
                      <div class="ln_solid"></div>
                      <div class="form-group">
                        <div class="col-md-12 col-sm-12 col-xs-12 col-md-offset-3">
						              <button class="btn btn-primary" type="reset" id="reset">Reset</button>
                          <button type="submit" class="btn btn-success">Submit</button>
                        </div>
                      </div>
                      </div>
                      </br>
                    </form>

        <div class="row">
                 <div class="col-md-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h4 id="txArgs">Pending Transaction Report:</h4>
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
                          <td>Block Posted</td>
                          <td id="bp"></td>
                        </tr>
                        <tr>
                          <td>Actual Blocks Waiting</td>
                          <td id="blockswaiting"></td>
                        </tr>
                        <tr>
                          <td>Predicted Blocks Waiting for Confirmation</td>
                          <td id="meanBlocks"></td>
                        </tr>
                        <tr>
                          <td>Probability mined in less than 1 hour</td>
                          <td id="minedprob"></td>
                        </tr>
                        <tr>
                          <td>Gas Price (Gwei)</td>
                          <td id="gp"></td>
                        </tr>
                        <tr>
                          <td>Gas Offered</td>
                          <td id="go"></td>
                        </tr>
                        <tr>
                          <td>% of last 200 blocks accpeting this gas price</td>
                          <td id="hp"></td>
                        </tr>
                        <tr>
                          <td>Transactions At or Above in Current Txpool</td>
                          <td id="txatabove"></td>
                        </tr>
                        <tr>
                          <td>Max Transaction fee (ETH)</td>
                          <td id="txEth"></td>
                        </tr>
                         <tr>
                          <td>Max Transaction fee (Fiat)</td>
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
                    url: "json/txpoolblock.json",
		            method: "GET",
                    dataType: "json",
		            success: function(data) {
                    txpoolarray = data;
                    }
                })
                $('#txhash').focus();
            })


      //Curency Support
      
            $("#eur").click(function(){     
                location = "http://ethgasstation.info/pendingTxReport.php?curr=eur";                              
            });
            
            $("#usd").click(function(){
                location = "http://ethgasstation.info/pendingTxReport?curr=usd";
            });
          
            $("#cny").click(function(){
                location = "http://ethgasstation.info/pendingTxReport?curr=cny";                                      
            });

            $("#gbp").click(function(){
                location = "http://ethgasstation.info/pendingTxReport?curr=gbp";                       
            });
            $('#reset').click(function(){
              $('#txhash').html("");
              $('#bp').html("");
              $('#blockswaiting').html("");
              $('#meanBlocks').html("");
              $('#minedprob').html("");
              $('#gp').html("");
              $('#go').html("");
              $('#hp').html("");
              $('#txatabove').html("");
              $('#txEth').html("");
              $('#txFiat').html("");
              $('#txArgs').html("Pending Transaction Report:")

              $('#txhash').focus();
            })
  
            function estimateWait (gasprice, gasoffered)
            {
                for(var i=0; i < txpoolarray.length; i++){  
                    if (txpoolarray[i]['index'] == txhash){
                        hit = 1;
                        break;
                    }
                    else{
                        hit = 0;
                    }
                }
                if (hit){
                    return [txpoolarray[i]['block_posted'], txpoolarray[i]['gas_offered'], txpoolarray[i]['hashpower_accepting'], txpoolarray[i]['tx_atabove'], txpoolarray[i]['mined_probability'], txpoolarray[i]['gasprice'], txpoolarray[i]['expectedWait'], txpoolarray[i]['wait_blocks']];
                    }
                else {
                        return ["", "", "", "", "", "", "", ""];
                    }
            }

            $('form').submit(function(event){
              
              //Error Check
              if(!$('#txhash').val()){
                event.preventDefault(); // prevent form from POST to server
                $('#txhash').focus();
                focusSet = true;
                return;
              }
              else {
                txhash = $('#txhash').val();
              }
              //txhash set
              
              event.preventDefault();
              pdValues = estimateWait(txhash);
              console.log(pdValues);
              blockposted = pdValues[0];
              gasoffered = pdValues[1];
              hashpower = pdValues[2];
              txatabove = pdValues[3];
              minedprob = pdValues[4];
              if (minedprob != ""){
                minedprob = Number(pdValues[4].toFixed(2))*100;
              }
        
              gasprice = pdValues[5];
              expectedWait = pdValues[6];
              blocksWait = pdValues[7];

              currency = '<?php echo ($currency) ?>';
              console.log(currency);
              exchangeRate =<?php echo ($exchangeRate) ?>;
              blockInterval = <?php echo ($gpRecs2['block_time']) ?>;
              txMeanSecs = blocksWait * blockInterval;
              txMeanSecs = Number(txMeanSecs.toFixed(0))
      
              
              txFeeEth = gasprice/1e9 * gasoffered;
              txFeeEth = Number((txFeeEth).toFixed(7))
              txFeeFiat = txFeeEth * exchangeRate;
              txFeeFiat = Number(txFeeFiat.toFixed(5));

              if (blockposted == ""){
                  blockposted = "Not Found";
                  txFeeEth = "";
                  txFeeFiat = "";
                  reportString = "<small><span style='color:red'> Not found: This tx may not bave been received by our node, it may have already been mined, or there may be another tx with a lower nonce pending from this account</small></span>";
                  $('#txArgs').html(reportString);

              }
              

              $('#bp').html(blockposted);
              $('#hp').html(hashpower);
              $('#gp').html(gasprice);
              $('#blockswaiting').html(blocksWait);
              $('#meanBlocks').html(expectedWait);
              $('#txatabove').html(txatabove);
              $('#minedprob').html(minedprob);
              $('#go').html(gasoffered);
              $('#txEth').html(txFeeEth);
              if (blockposted == "Not Found"){
                return;
              }
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
