<!-- egs header starts -->
  <div class="top_nav">
    <div class="nav_menu">
      <nav>
        <div class="nav toggle">
          <a id="menu_toggle"><i class="fa fa-bars"></i></a>
        </div>
        <div class="header_left_contents">
          <div  class="social_links">
            <div class="social_link">
                <a href="https://discord.gg/mzDxADE" target="_blank"><img class="social_icon primary" src="/images/discord.svg"></a>
                <a href="https://discord.gg/mzDxADE" target="_blank"><img class="social_icon secondary" src="/images/discord-green.svg"></a>
            </div>
            <div class="social_link">
                <a href="https://twitter.com/ethgasstation" target="_blank"><img class="social_icon primary" src="/images/twitter.svg"></a>
                <a href="https://twitter.com/ethgasstation" target="_blank"><img class="social_icon secondary" src="/images/twitter-green.svg"></a>
            </div>
          </div>
        </div>

        <ul class="nav navbar-nav navbar-right">
          <li class="dropdown">
            <a href="#" class="user-profile dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-globe"></i><span class="change_currency_text"> Change Currency <img class='down_arrow' src='/images/down-arrow.svg'></span>
            </a>
            <ul class="dropdown-menu">
              <li id="usd"><a href="#"> USD<?php if($currency=='usd'){echo'<span class="pull-right"><i class="fa fa-check"></i></span>';}?></a></li>
              <li id="eur"><a href="#"> EUR<?php if($currency=='eur'){echo'<span class="pull-right"><i class="fa fa-check"></i></span>';}?></a></li>
              <li id="gbp"><a href="#"> GBP<?php if($currency=='gbp'){echo'<span class="pull-right"><i class="fa fa-check"></i></span>';}?></a></li>
              <li id="cny"><a href="#"> CNY<?php if($currency=='cny'){echo'<span class="pull-right"><i class="fa fa-check"></i></span>';}?></a></li>
            </ul>
          </li>
      </ul>
      </nav>
    </div>
  </div>
<!-- /egs header ends -->