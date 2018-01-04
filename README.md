# EthGasStation

EthGasStation is a tool for monitoring the time transactions take to be confirmed on the ETH network.  It also monitors
and estimates miner policies with respect to gas prices and formats the data for viewing over http.

It requires the following:
  1) LAMP set up if you want to use the webpage
  2) Python for the scripts that analyze data from the geth node.
  3) Mysql database
  4) A local geth node 

Add a user 'ethgas' with password 'station' to your local mysql database and create a database 'tx' to allow it to add the tables. 

requirements: pip3 install -r requirements.txt

usage: python3 backend/gasStationFull.py

 
