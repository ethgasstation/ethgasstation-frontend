#!/bin/bash
set -e

# Run following command to execute the script:
# cd /usr/local/SettleFinance/ethgasstation-frontend && git fetch --all && git reset --hard origin/master && git pull && chmod -R 777 /usr/local/SettleFinance/ethgasstation-frontend/upgrade.sh && ./upgrade.sh

#For Initial Setup
#	mkdir -p -v /usr/local/SettleFinance && cd /usr/local/SettleFinance
#	git clone https://github.com/SettleFinance/ethgasstation-frontend.git
#	git clone https://github.com/SettleFinance/ethgasstation-backend.git
#	cd ethgasstation-frontend

echo "####################################"
echo "# ETH GAS STARTION FRONEND UPGRADE #"
echo "####################################"
echo "Replica PUBLIC IP Address:"
dig +short myip.opendns.com @resolver1.opendns.com

rm -v /usr/local/SettleFinance/common.php || echo "Backup common file was probably already removed.";
rm -r -f -v /usr/local/SettleFinance/json || echo "Backup json files were probably already removed.";

mkdir -p -v $json_output
touch $json_output/test
mkdir -p -v /usr/local/SettleFinance/json

cp /var/www/ethgasstation.settle.host/public_html/build/php/common.php /usr/local/SettleFinance/common.php
cp $json_output/* /usr/local/SettleFinance/json

echo "Stopping Frontend..."
touch $json_output/haltFile
systemctl stop apache2
echo 'Awaiting safety backend halt...' && sleep 200
systemctl stop ethgassbackend
rm -f -v $json_output/haltFile

rm -r -f -v /var/www/ethgasstation.settle.host/public_html/*

cp -v -r /usr/local/SettleFinance/ethgasstation-frontend/* /var/www/ethgasstation.settle.host/public_html/

rm -f -v /var/www/ethgasstation.settle.host/public_html/build/php/common.php

cp -v /usr/local/SettleFinance/common.php /var/www/ethgasstation.settle.host/public_html/build/php/common.php

mkdir -p -v $json_output
cp /usr/local/SettleFinance/json/* $json_output

chmod -R 777 $json_output

echo "Starting Frontend..."

systemctl start ethgassbackend
sleep 3
systemctl start apache2

echo "Checking Disk Space"
df

echo "Last Backend Startus: "
journalctl --unit=ethgassbackend -n 25 --no-pager

#PRO TIP's:

#echo "Geth Upgrade..."
#systemctl stop geth
#
#cd /usr/local/go-ethereum
#git reset --hard origin/release/1.8
#git checkout origin/release/1.8
#git pull origin release/1.8
#make geth
#
#systemctl restart geth

#geth status verify command:
#journalctl --unit=geth -n 100 --no-pager

#to edit geth service (use following command after applying changes: systemctl daemon-reload)
#nano /lib/systemd/system/geth.service

#to edit frontend config
#nano /var/www/ethgasstation.settle.host/public_html/build/php/common.php

#backed output json location:
#/var/www/ethgasstation.settle.host/public_html/json

#backed output cleanup & reboot
#rm -r -f -v /var/www/ethgasstation.settle.host/public_html/json/* && chmod -R 777 /var/www/ethgasstation.settle.host/public_html/json && systemctl restart ethgassbackend && systemctl restart geth

#backend status verify
#journalctl --unit=ethgassbackend -n 100 --no-pager

#ExecStart=/usr/local/go-ethereum/build/bin/geth --syncmode "fast" --rpc --rpcapi="db,eth,net,web3,personal,txpool" --cache 4096 --maxpeers 50 --verbosity 3 --rpcport 8545 --rpcaddr "127.0.0.1" --rpccorsdomain "*" --rpcvhosts "*"

