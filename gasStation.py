from web3 import Web3, HTTPProvider
from sqlalchemy import create_engine

web3 = Web3(HTTPProvider('http://localhost:8545'))

engine = create_engine(
    'mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)

def new_block_callback(block_hash):
    print (block_hash)

def new_tx_callback(tx_hash):
    print ('tx '+ tx_hash)

block_filter = web3.eth.filter('latest')
tx_filter = web3.eth.filter('pending')

while True:
    block_filter.watch(new_block_callback)
    tx_filter.watch(new_tx_callback)

    response = input("type q to quit /n")
    if response == 'q':
        break