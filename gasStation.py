import time
from web3 import Web3, HTTPProvider
from sqlalchemy import create_engine

web3 = Web3(HTTPProvider('http://localhost:8545'))

engine = create_engine(
    'mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)




class Tx ():
    def __init__(self, tx_obj):
        self.hash = tx_obj.hash
        self.block_posted = tx_obj.blockNumber
        self.to_address = tx_obj.to
        self.from_address = tx_obj.from
        self.ts = time.time()
        self.gp = tx_obj.gasPrice/1e6
        self.gas_offered = tx_obj.gas

    




def new_tx_callback(tx_hash):
    try:
        tx_obj = web3.eth.getTransactions(tx_hash)
        clean_tx = Tx(tx_obj)
        print(clean_tx)
    except:
        print(e)


def filter():
    tx_filter = web3.eth.filter('pending')
    while True:
        tx_filter.watch(new_tx_callback)
        response = input("type q to quit \n")
        if response == 'q':
            break

filter()