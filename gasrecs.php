<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <!-- Meta, title, CSS, favicons, etc. -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title><?php echo EGS_TITLE; ?> | FAQ </title>

    <!-- Bootstrap -->
    <link href="vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,600,800" rel="stylesheet">

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
    


  </head>

  <body class="nav-md">
  <?php include 'unofficial.php'; ?>
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
            </nav>
          </div>
         </div>

        

        <!-- /top navigation -->
  <div class="right_col" role="main">
            <div class="row">
              <div class="col-md-9 col-sm-12 col-xs-12">
                <div class="x_panel">
                  <div class="blog_title">
                    <h2>FAQ</h2>

                    <div class="clearfix"></div>
                  </div>
                 <div class="blog_content">

                  <h4 id="recs"><b> What are the recommended user gas prices?</b></h4>
                  <p>Many people use the default gas price from their wallet when they make a transaction, and this is generally OK.  However, sometimes it makes sense to pay more if you want the transaction mined quickly or you may want to save some money and offer a cheap gas price, especially if you don't care how quickly it is mined. In these cases, its hard to know what gas price to use unless you are monitoring the network (or checking this site frequently).  
                  <p>Therefore, we publish these recommendations (<a href="/json/ethgasAPI.json">ETHgasAPI</a>) to simplify the gas price choice based on <em>desired transaction speed and cost:</em><p></br> 
                  <p>1) <b>Safe low</b> - This is a gas price that is intended to be both cheap and successful.  It may take a bit longer to get a confirmation with this price (e.g. 5minutes), but it is safe to use and should be confirmed propmpty. This price is determined by the lowest price where at least 5% of the network hash power will accept it.  It requires that at least 50 transactions have been mined in the last 24 hours at this price.  Furthermore, we monitor the network in real time and will update this price if a transaction at or above does not confirm within 50 blocks</p></br>
                  <p>2) <b>Average</i></b> - This is the price accepted by top miners who account for at leat 50% of the blocks mined- safe and prompt. Usually reflects the wallet defaults.</p></br>
                  <p>3) <b>Fastest</b> - This is the lowest gas price that is accepted by all top miners (estimated over the last two days). Therefore, transactions with this gas price should be accepted by all the top pools. Paying more than this price is unlikely to increase transaction confirmation time under normal circumstances.</p>
                  <p><br></p>
                  <p><br></p>
                 
                 
                  </div>
                  <div class="clearfix"></div>
                </div>
                <div class="clearfix"></div>
              </div>
              <div class="clearfix"></div>
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
    <script src="build/js/custom3.js"></script>
	
  </body>
</html>
