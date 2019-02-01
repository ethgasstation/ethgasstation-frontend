#!/bin/bash
set -e

# before starting this script:
# cd /usr/local/SettleFinance/ethgasstation-frontend
# git pull

echo "####################################"
echo "# ETH GAS STARTION FRONEND UPGRADE #"
echo "####################################"


rm -v /usr/local/SettleFinance/common.php || echo "Backup common file was probably already removed.";

cp /var/www/ethgasstation.settle.host/public_html/build/php/common.php /usr/local/SettleFinance/common.php

#cp -v /usr/local/ethgasstation-backend/settings.conf /usr/local/ethgasstation-backend-settings.conf
#cp -v -r /usr/local/SettleFinance/ethgasstation-frontend/* /var/www/ethgasstation.settle.host/public_html/




