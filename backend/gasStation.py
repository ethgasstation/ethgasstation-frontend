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
  


class Timers():
    def __init__(self, start_block):
        self.start_block = start_block
        self.current_block = start_block

    def update_time(self, block):
        self.current_block = block
    
    def check_newblock(self, block):
        if self.current_block >= block:
            return False
        elif self.current_block < block:
            self.update_time(block)
            return True

class CleanTx():
    def __init__(self, tx_obj, block_posted=None, time_posted=None, miner=None):
        self.hash = tx_obj.hash
        self.block_posted = block_posted
        self.block_mined = tx_obj.blockNumber
        self.to_address = tx_obj['to']
        self.from_address = tx_obj['from']
        self.time_posted = time_posted
        self.gas_price = tx_obj['gasPrice']
        self.gas_offered = tx_obj['gas']
        self.round_gp_10gwei()
        self.miner = miner

    def to_dataframe(self):
        data = {self.hash: {'block_posted':self.block_posted, 'block_mined':self.block_mined, 'to_address':self.to_address, 'from_address':self.from_address, 'time_posted':self.time_posted, 'time_mined': None, 'gas_price':self.gas_price, 'gas_offered':self.gas_offered, 'round_gp_10gwei':self.gp_10gwei}}
        return pd.DataFrame.from_dict(data, orient = 'index')

    def round_gp_10gwei(self):
        """Rounds the gas price to gwei"""
        gp = self.gas_price/1e8
        if gp >=1 and gp<10:
            gp = np.floor(gp)
        elif gp >= 10:
            gp = gp/10
            gp = np.floor(gp)
            gp = gp*10
        else:
            gp = 0
        self.gp_10gwei = gp

class CleanBlock():
    def __init__(self, block_obj, main, uncle, timemined, mingasprice = None, numtx = None, weightedgp = None, includedblock = None):
        self.block_number = block_obj.number 
        self.gasused = block_obj.gasUsed
        self.miner = block_obj.miner
        self.time_mined = timemined
        self.gaslimit = block_obj.gasLimit 
        self.numtx = numtx
        self.blockhash = block_obj.hash
        self.mingasprice = mingasprice
        self.uncsreported = len(block_obj.uncles)
        self.blockfee = block_obj.gasUsed * weightedgp / 1e10
        self.main = main
        self.uncle = uncle
        self.includedblock = includedblock

    def to_dataframe(self):
        data = {0:{'block_number':self.block_number, 'gasused':self.gasused, 'miner':self.miner, 'gaslimit':self.gaslimit, 'numtx':self.numtx, 'blockhash':self.blockhash, 'time_mined':self.time_mined, 'mingasprice':self.mingasprice, 'uncsreported':self.uncsreported, 'blockfee':self.blockfee, 'main':self.main, 'uncle':self.uncle, 'includedblock':self.includedblock}}
        return pd.DataFrame.from_dict(data, orient = 'index')

def filter_transactions():
    """filter and add to dataframe"""

    alltx = pd.DataFrame()
    txpool = pd.DataFrame()
    blockdata = pd.DataFrame()

    timer = Timers(web3.eth.blockNumber)
    tx_filter = web3.eth.filter('pending')

    def manage_dataframes(block):
        nonlocal alltx
        if timer.check_newblock(block):
            (mined_blockdf, block_obj) = process_block_transactions(block - 1)
            alltx = alltx.combine_first(mined_blockdf)
            block_sumdf = process_block_data(mined_blockdf, block_obj)
            blockdata = blockdata.append(block_sumdf, ignore_index = True)
            get_txpool(block)
            analyzed_block = analyze_txpool(block-1)
            alltx = alltx.combine_first(analyzed_block)
            with pd.option_context('display.max_rows', 50, 'display.max_columns', None,):
                print(alltx)

    def process_block_transactions(block):
        timemined = time.time()
        block_df = pd.DataFrame()
        block_obj = web3.eth.getBlock(block, True)
        miner = block_obj.miner 
        for transaction in block_obj.transactions:
            clean_tx = CleanTx(transaction, None, None, miner)
            block_df = block_df.append(clean_tx.to_dataframe(), ignore_index = False)
        block_df['time_mined'] = timemined
        return(block_df, block_obj)
    
    def process_block_data(block_df, block_obj):
        if len(block_obj.transactions)>0:
            block_df['weighted_fee'] = block_df['round_gp_10gwei']* block_df['gas_offered']
            block_mingasprice = block_df['round_gp_10gwei'].min()
            block_weightedfee = block_df['weighted_fee'].sum() / block_df['gas_offered'].sum()
        block_numtx = len(block_obj.transactions)
        clean_block = CleanBlock(block_obj, 1, 0, timemined, block_mingasprice, block_numtx, block_weightedfee)
        return(clean_block.to_dataframe())
       

    def get_txpool(block):
        """gets list of all txhash in txpool at block and stores in dataframe"""
        nonlocal txpool
        hashlist = []
        txpoolcontent = web3.txpool.content
        txpoolpending = txpoolcontent['pending']
        for tx_sequence in txpoolpending.values():
            for tx_obj in tx_sequence.values():
                hashlist.append(tx_obj['hash'])
        txpool_temp = pd.DataFrame(index = hashlist)
        txpool_temp['block'] = block
        txpool = txpool.append(txpool_temp, ignore_index = False)
        txpool = txpool.loc[txpool['block']>(block-5)] #keep from getting too big
        

    def analyze_txpool(block):
        nonlocal alltx
        nonlocal blockdata
        nonlocal txpool

        def get_hpa(gasprice):
            """gets the hash power accpeting the gas price over last 200 blocks"""
            hpa = hashpower.loc[gasprice >= hashpower.index, 'hashp_pct']
            if gasprice > hashpower.index.max():
                hpa = 100
            elif gasprice < hashpower.index.min():
                hpa = 0
            else:
                hpa = hpa.max()
            return int(hpa)

        def txAtAbove(gasprice):
            """gets the number of transactions in the txpool at or above the given gasprice"""
            txAtAb = txpool_by_gp.loc[txpool_by_gp.index >= gasprice, 'gas_price']
            if gasprice > txpool_by_gp.index.max():
                txAtAb = 0
            else:
                txAtAb = txAtAb.sum()
            return txAtAb

        def predict(row):
            intercept = 2.6802
            hpa_coef = -0.0235
            txatabove_coef= 0.0004
            sum1 = (intercept + (row['hashpower_accepting']*hpa_coef) + (row['tx_atabove']*txatabove_coef))
            return np.exp(sum1) 

        #get last 200 blocks mingasprice
        recent_blocks = blockdata.loc[blockdata['block_number'] > (block-200), ['mingasprice', 'block_number', 'gaslimit', 'time_mined']]

        #get avg blockinterval time
        blockinterval = recent_blocks.sort_values('block_number').diff()
        blockinterval.loc[blockinterval['block_number'] > 1, 'time_mined'] = np.nan
        blockinterval.loc[blockinterval['time_mined']< 0, 'time_mined'] = np.nan
        avg_timemined = blockinterval['time_mined'].mean()
        if avg_timemined is None:
            avg_timemined = 30
        
        print ('avg_timemined ' +str(avg_timemined))

        #create hashpower table
        hashpower = recent_blocks.groupby('mingasprice').count()
        hashpower = hashpower.rename(columns={'block_number': 'count'})
        hashpower['cum_blocks'] = hashpower['count'].cumsum()
        totalblocks = hashpower['count'].sum()
        hashpower['hashp_pct'] = hashpower['cum_blocks']/totalblocks*100

        #create txpool data
        if len(txpool) == 0:
            return
        txpool_block = txpool.loc[txpool['block']==block]
        alltx_block = alltx.loc[alltx['block_posted']==block, 'block_posted']
        txpool_block = pd.concat([txpool_block, alltx_block], axis=1, join='outer')
        txpool_block = txpool_block.drop(['block_posted', 'block'], axis=1)
        frames = [txpool_block, alltx]
        txpool_block = pd.concat(frames, axis=1, join='inner') #now with all tx data
        txpool_by_gp = txpool_block.groupby('round_gp_10gwei').count()
        

        n=100
        k=10
        predictTable = pd.DataFrame({'gasprice' :  range(10, 1010, 10)})
        ptable2 = pd.DataFrame({'gasprice' : range(0, 10, 1)})
        predictTable = predictTable.append(ptable2).reset_index(drop=True)
        predictTable = predictTable.sort_values('gasprice').reset_index(drop=True)
        predictTable['hashpower_accepting'] = predictTable['gasprice'].apply(get_hpa)
        predictTable['tx_atabove'] = predictTable['gasprice'].apply(txAtAbove)
        predictTable['expectedWait'] = predictTable.apply(predict, axis=1)
        predictTable['expectedWait'] = predictTable['expectedWait'].apply(lambda x: 2 if (x < 2) else x)
        predictTable['expectedWait'] = predictTable['expectedWait'].apply(lambda x: np.round(x, decimals=2))
        predictTable['expectedTime'] = predictTable['expectedWait'].apply(lambda x: np.round((x * avg_timemined / 60), decimals=2))
        
        gp_lookup = predictTable.set_index('gasprice')['hashpower_accepting'].to_dict()
        txatabove_lookup = predictTable.set_index('gasprice')['tx_atabove'].to_dict()

        txpool_block['wait_blocks'] = txpool_block['block_posted'].apply(lambda x: block - x)
        gaslimit = recent_blocks['gaslimit'].mean()
        txpool_block['pct_limit'] = txpool_block['gas_offered'].apply(lambda x: x / gaslimit)
        txpool_block['hashpower_accepting'] = txpool_block['round_gp_10gwei'].apply(lambda x: gp_lookup[x] if x in gp_lookup else 100)
        txpool_block['tx_atabove'] = txpool_block['round_gp_10gwei'].apply(lambda x: txatabove_lookup[x] if x in txatabove_lookup else 1)
        txpool_block['num_from'] = txpool_block.groupby('from_address')['block_posted'].transform('count')
        txpool_block['num_to'] = txpool_block.groupby('to_address')['block_posted'].transform('count')
        txpool_block['expectedWait'] = txpool_block.apply(predict, axis=1)
        txpool_block['expectedWait'] = txpool_block['expectedWait'].apply(lambda x: 2 if (x < 2) else x)
        txpool_block['expectedWait'] = txpool_block['expectedWait'].apply(lambda x: np.round(x, decimals=2))
        txpool_block['expectedTime'] = txpool_block['expectedWait'].apply(lambda x: np.round((x * avg_timemined / 60), decimals=2))
        return(txpool_block)



    def new_tx_callback(tx_hash):
        nonlocal alltx
        try:
            block = web3.eth.blockNumber
            tx_obj = web3.eth.getTransaction(tx_hash)
            timestamp = time.time()
            clean_tx = CleanTx(tx_obj, block, timestamp)
            alltx = alltx.append(clean_tx.to_dataframe(), ignore_index = False)
            manage_dataframes(block)
        except AttributeError as e:
            print(e)

    while True:
        tx_filter.watch(new_tx_callback)
        response = input("type q to quit \n")
        if response == 'q':
            break

filter_transactions()
