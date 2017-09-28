import time
import sys
import json
import urllib
import pandas as pd
import numpy as np
from web3 import Web3, HTTPProvider
from sqlalchemy import create_engine

web3 = Web3(HTTPProvider('http://localhost:8545'))
engine = create_engine(
    'mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)
pending = pd.DataFrame(columns = ['hash', 'block_posted', 'to_address', 'from_address', 'ts', 'gp', 'gas_offered', 'gp_10gwei'])



def round_gp_10gwei(gp):
    """Rounds the gas price to gwei"""
    gp = gp/1e8
    if gp >=1 and gp<10:
        gp = np.floor(gp)
    elif gp >= 10:
        gp = gp/10
        gp = np.floor(gp)
        gp = gp*10
    else:
        gp = 0
    return gp



class Tx ():
    def __init__(self, tx_obj, block):
        self.hash = [tx_obj.hash]
        self.block_posted = [block]
        self.to_address = [tx_obj['to']]
        self.from_address = [tx_obj['from']]
        self.ts = [time.time()]
        self.gp = [tx_obj['gasPrice']]
        self.gas_offered = [tx_obj['gas']]
        self.gp_10gwei = [round_gp_10gwei(tx_obj['gasPrice'])]

    def to_dataframe(self):
        dataframe = pd.DataFrame.from_dict(self.__dict__)
        return dataframe

def new_tx_callback(tx_hash):
    global pending
    try:
        block = web3.eth.blockNumber
        tx_obj = web3.eth.getTransaction(tx_hash)
        clean_tx = Tx(tx_obj, block)
        temp = clean_tx.to_dataframe()
        pending = pending.append(temp, ignore_index=True)
        print(pending)
    except:
        print(e)


def filter():
    print(pending)
    tx_filter = web3.eth.filter('pending')
    while True:
        tx_filter.watch(new_tx_callback)
        response = input("type q to quit \n")
        if response == 'q':
            break

filter()