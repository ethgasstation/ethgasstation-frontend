from web3 import Web3, HTTPProvider
from sqlalchemy import create_engine

web3 = Web3(HTTPProvider('http://localhost:8545'))

engine = create_engine(
    'mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)

def new_block_callback(block_hash):
    print (block_hash)

new_block_filter = web3.eth.filter('latest')


while True:
    new_block_filter.watch(new_block_callback)
    response = input("type q to quit")
    if response == q:
        break