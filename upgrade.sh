#!/bin/bash
set -e

# before starting this script:
# cd /usr/local/SettleFinance/ethgasstation-frontend
# git pull
# chmod -R 777 /usr/local/SettleFinance/ethgasstation-frontend/upgrade.sh

echo "####################################"
echo "# ETH GAS STARTION FRONEND UPGRADE #"
echo "####################################"


rm -v /usr/local/SettleFinance/common.php || echo "Backup common file was probably already removed.";

cp /var/www/ethgasstation.settle.host/public_html/build/php/common.php /usr/local/SettleFinance/common.php

echo "Stopping Apache..."
apachectl stop

rm -r -f -v /var/www/ethgasstation.settle.host/public_html/*

cp -v -r /usr/local/SettleFinance/ethgasstation-frontend/* /var/www/ethgasstation.settle.host/public_html/

rm -f -v /var/www/ethgasstation.settle.host/public_html/build/php/common.php

cp -v /usr/local/SettleFinance/common.php /var/www/ethgasstation.settle.host/public_html/build/php/common.php

mkdir -p -v /var/www/ethgasstation.settle.host/public_html/json

chmod -R 777 /var/www/ethgasstation.settle.host/public_html/json

echo "Startting Apache..."

/etc/init.d/apache2 start
/etc/init.d/apache2 reload

echo "Restarting Backend..."

systemctl restart ethgassbackend







