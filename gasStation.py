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

def round_gp_gwei(gp):
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
    def __init__(self, tx_obj):
        self.hash = tx_obj.hash
        self.block_posted = tx_obj['blockNumber']
        self.to_address = tx_obj['to']
        self.from_address = tx_obj['from']
        self.ts = time.time()
        self.gp = tx_obj['gasPrice']
        self.gas_offered = tx_obj['gas']
        self.gp_gwei = round_gp_gwei(tx_obj['gasPrice'])

    




def new_tx_callback(tx_hash):
    try:
        tx_obj = web3.eth.getTransaction(tx_hash)
        clean_tx = Tx(tx_obj)

        print(clean_tx.gp_gwei)
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