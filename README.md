# EthGasStation
Monitor Ethereum Transaction Confirmation Times and Gas Prices

EthGasStation is a tool for monitoring the time transactions take to be confirmed on the ETH network.  It also monitors
and analyzes miner behavior and formats the data for viewing.

It requires the following:
  1) LAMP set up if you want to use the webpage
  2) Node.js for running the scripts to monitor a local ETH node
  3) Python for the scripts that analyze data.
 
 You will need to set up a mysql database with appropriate tables in order to use the scripts.  All of the monitoring/analysis
 scripts including the commands to set up the mysql databases are in the 'backend' folder
 
 Once mysql tables are created:
 
 You can run:  node gasStation.js
 
 This script monitors the node and calls gasStationAnalyze.js and gascalc.py periodically to update the analyses and calculate the gas price recommendations
 
 
