#!/bin/bash
set -e

# Run following command to execute the script:
# cd /usr/local/SettleFinance/ethgasstation-frontend && git fetch --all && git reset --hard origin/master && git pull && chmod -R 777 /usr/local/SettleFinance/ethgasstation-frontend/upgrade.sh && ./upgrade.sh

echo "####################################"
echo "# ETH GAS STARTION FRONEND UPGRADE #"
echo "####################################"


rm -v /usr/local/SettleFinance/common.php || echo "Backup common file was probably already removed.";
rm -r -f -v /usr/local/SettleFinance/json || echo "Backup json files were probably already removed.";

mkdir -p -v /var/www/ethgasstation.settle.host/public_html/json
mkdir -p -v /usr/local/SettleFinance/json
cp /var/www/ethgasstation.settle.host/public_html/build/php/common.php /usr/local/SettleFinance/common.php
cp /var/www/ethgasstation.settle.host/public_html/json/* /usr/local/SettleFinance/json

echo "Stopping Apache and Backend..."
systemctl stop apache2
systemctl stop ethgassbackend

rm -r -f -v /var/www/ethgasstation.settle.host/public_html/*

cp -v -r /usr/local/SettleFinance/ethgasstation-frontend/* /var/www/ethgasstation.settle.host/public_html/

rm -f -v /var/www/ethgasstation.settle.host/public_html/build/php/common.php

cp -v /usr/local/SettleFinance/common.php /var/www/ethgasstation.settle.host/public_html/build/php/common.php

mkdir -p -v /var/www/ethgasstation.settle.host/public_html/json
cp /usr/local/SettleFinance/json/* /var/www/ethgasstation.settle.host/public_html/json

chmod -R 777 /var/www/ethgasstation.settle.host/public_html/json

echo "Startting Apache and Backend..."

systemctl start apache2
systemctl start ethgassbackend
systemctl daemon-reload






