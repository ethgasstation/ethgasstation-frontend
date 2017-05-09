# EthGasStation

EthGasStation is a tool for monitoring the time transactions take to be confirmed on the ETH network.  It also monitors
and estimates miner policies with respect to gas prices and formats the data for viewing over http.

It requires the following:
  1) LAMP set up if you want to use the webpage
  2) Node.js for running the scripts to monitor a local ETH node
  3) Python for the scripts that analyze data.
  4) Mysql database with tables created using the commands in /backend/txtables.sql 
  5) A local ethereum node 
 
Once the mysql tables are created:
 
You can run:  node gasStation.js
 
This script monitors the  node and calls gasStationAnalyze.js and gascalc.py periodically to update the analyses for the webpage and calculate the gas price recommendations
 
 
