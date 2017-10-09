import time
import sys
import json
import math
import traceback
import pandas as pd
import numpy as np
from web3 import Web3, HTTPProvider
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, BigInteger, text
from sqlalchemy.ext.declarative import declarative_base
from egs import *

web3 = Web3(HTTPProvider('http://localhost:8545'))
engine = create_engine(
    'mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)
Base.metadata.create_all(engine)


def init_dfs():
   blockdata = pd.read_sql('SELECT * from blockdata2 order by id desc limit 1000', con=engine)
   blockdata = blockdata.drop('id', axis=1)
   alltx = pd.read_sql('SELECT * from minedtx2 order by id desc limit 10000', con=engine)
   alltx = alltx.drop('id', axis=1)
   alltx.set_index('index', drop=True, inplace=True)
   return(blockdata, alltx)


def get_txhases_from_txpool(block):
        """gets list of all txhash in txpool at block and returns dataframe"""
        hashlist = []
        txpoolcontent = web3.txpool.content
        txpoolpending = txpoolcontent['pending']
        for tx_sequence in txpoolpending.values():
            for tx_obj in tx_sequence.values():
                hashlist.append(tx_obj['hash'])
        txpool_current = pd.DataFrame(index = hashlist)
        txpool_current['block'] = block
        return txpool_current

def get_diff(current, prior, block):
    """gets txhashes removed from txpool at current block and returns df"""
    removed = np.setdiff1d(prior, current, assume_unique=True)
    removed_df = pd.DataFrame(index=removed)
    removed_df['removed_block'] = block
    print('Number of tx removed :' + str(len(removed_df)))
    return removed_df


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
        timemined = block_df['time_mined'].min()
        clean_block = CleanBlock(block_obj, 1, 0, timemined, block_mingasprice, block_numtx, block_weightedfee)
        return(clean_block.to_dataframe())

def get_hpa(gasprice, hashpower):
    """gets the hash power accpeting the gas price over last 200 blocks"""
    hpa = hashpower.loc[gasprice >= hashpower.index, 'hashp_pct']
    if gasprice > hashpower.index.max():
        hpa = 100
    elif gasprice < hashpower.index.min():
        hpa = 0
    else:
        hpa = hpa.max()
    return int(hpa)

def txAtAbove(gasprice, txpool_by_gp):
    """gets the number of transactions in the txpool at or above the given gasprice"""
    txAtAb = txpool_by_gp.loc[txpool_by_gp.index >= gasprice, 'gas_price']
    if gasprice > txpool_by_gp.index.max():
        txAtAb = 0
    else:
        txAtAb = txAtAb.sum()
    return txAtAb

def predict(row):
    if row['chained'] == 1:
        return np.nan
    intercept = 2.6697
    hpa_coef = -0.0233
    txatabove_coef= 0.0003
    ico_coef = 1.3629
    dump_coef = 1.1738
    high_gas_coef = .5317
    sum1 = (intercept + (row['hashpower_accepting']*hpa_coef) + (row['tx_atabove']*txatabove_coef) + (row['ico']*ico_coef) + (row['dump']*dump_coef) + (row['high_gas_offered']*high_gas_coef))
    return np.exp(sum1)

def predict_mined(row):
    if row['chained']==1:
        return np.nan
    intercept = -.1104
    hpa = .0364
    hgo = -1.8213
    wb = -0.0006
    sum1 = intercept + (row['hashpower_accepting']*hpa) + (row['highgas2']*hgo) + (row['wait_blocks']*wb)
    factor = np.exp(-1*sum1)
    prob = 1 / (1+factor)
    return prob 

def check_nonce(row, txpool_block_nonce):
    if row['num_from']>1:
        if row['nonce'] > txpool_block_nonce.loc[row['from_address'],'nonce']:
            return 1
        if row['nonce'] == txpool_block_nonce.loc[row['from_address'], 'nonce']:
            return 0
    else:
        return 0

def analyze_last200blocks(block, blockdata):
    recent_blocks = blockdata.loc[blockdata['block_number'] > (block-200), ['mingasprice', 'block_number', 'gaslimit', 'time_mined', 'speed']]
    gaslimit = recent_blocks['gaslimit'].mean()
    last10 = recent_blocks.sort_values('block_number', ascending=False).head(n=10)
    speed = last10['speed'].mean()
    #create hashpower accepting dataframe based on mingasprice accepted in block
    hashpower = recent_blocks.groupby('mingasprice').count()
    hashpower = hashpower.rename(columns={'block_number': 'count'})
    hashpower['cum_blocks'] = hashpower['count'].cumsum()
    totalblocks = hashpower['count'].sum()
    hashpower['hashp_pct'] = hashpower['cum_blocks']/totalblocks*100
    #get avg blockinterval time
    blockinterval = recent_blocks.sort_values('block_number').diff()
    blockinterval.loc[blockinterval['block_number'] > 1, 'time_mined'] = np.nan
    blockinterval.loc[blockinterval['time_mined']< 0, 'time_mined'] = np.nan
    avg_timemined = blockinterval['time_mined'].mean()
    if np.isnan(avg_timemined):
        avg_timemined = 30
    return(hashpower, avg_timemined, gaslimit, speed)

def merge_txpool_alltx(txpool, alltx, block):
    #get txpool data at block
    txpool_block = txpool.loc[txpool['block']==block]
    #add transactions submitted at block
    alltx_block = alltx.loc[alltx['block_posted']==block, 'block_posted']
    alltx_block = alltx_block[~alltx_block.index.isin(txpool_block.index)]
    print ('len txpool_block ' + str(len(txpool_block)))
    txpool_block = txpool_block.join(alltx_block, how='outer')
    print ('len txpool_block ' + str(len(txpool_block)))
    txpool_block = txpool_block.drop(['block_posted', 'block'], axis=1)
    #merge transaction data for txpool transactions
    #txpool_block only has transactions received by filter
    txpool_block = txpool_block.join(alltx, how='inner')
    #group by gasprice
    txpool_block = txpool_block[~txpool_block.index.duplicated(keep = 'first')]
    assert txpool_block.index.duplicated().sum()==0
    txpool_by_gp = txpool_block.groupby('round_gp_10gwei').count()
    return(txpool_block, txpool_by_gp)

def make_predictiontable(hashpower, avg_timemined, txpool_by_gp):
    predictTable = pd.DataFrame({'gasprice' :  range(10, 1010, 10)})
    ptable2 = pd.DataFrame({'gasprice' : range(0, 10, 1)})
    predictTable = predictTable.append(ptable2).reset_index(drop=True)
    predictTable = predictTable.sort_values('gasprice').reset_index(drop=True)
    predictTable['hashpower_accepting'] = predictTable['gasprice'].apply(get_hpa, args=(hashpower,))
    predictTable['tx_atabove'] = predictTable['gasprice'].apply(txAtAbove, args=(txpool_by_gp,))
    predictTable['ico'] = 0
    predictTable['dump'] = 0
    predictTable['high_gas_offered'] = 0
    predictTable['wait_blocks'] = 0
    predictTable['highgas2'] = 0
    predictTable['chained'] = 0
    predictTable['expectedWait'] = predictTable.apply(predict, axis=1)
    predictTable['expectedWait'] = predictTable['expectedWait'].apply(lambda x: 2 if (x < 2) else x)
    predictTable['expectedWait'] = predictTable['expectedWait'].apply(lambda x: np.round(x, decimals=2))
    predictTable['expectedTime'] = predictTable['expectedWait'].apply(lambda x: np.round((x * avg_timemined / 60), decimals=2))  
    gp_lookup = predictTable.set_index('gasprice')['hashpower_accepting'].to_dict()
    txatabove_lookup = predictTable.set_index('gasprice')['tx_atabove'].to_dict()
    return(gp_lookup, txatabove_lookup, predictTable)

def analyze_txpool(block, gp_lookup, txatabove_lookup, txpool_block, gaslimit, avg_timemined):
    '''defines prediction parameters for all transactions in the txpool'''
    txpool_block['wait_blocks'] = txpool_block['block_posted'].apply(lambda x: block - x)
    txpool_block['pct_limit'] = txpool_block['gas_offered'].apply(lambda x: x / gaslimit)
    txpool_block['hashpower_accepting'] = txpool_block['round_gp_10gwei'].apply(lambda x: gp_lookup[x] if x in gp_lookup else 100)
    txpool_block['tx_atabove'] = txpool_block['round_gp_10gwei'].apply(lambda x: txatabove_lookup[x] if x in txatabove_lookup else 1)
    txpool_block['num_from'] = txpool_block.groupby('from_address')['block_posted'].transform('count')
    txpool_block_nonce = txpool_block[['from_address', 'nonce']].groupby('from_address').agg({'nonce':'min'})
    txpool_block['chained'] = txpool_block.apply(check_nonce, args=(txpool_block_nonce,), axis=1)
    txpool_block['num_to'] = txpool_block.groupby('to_address')['block_posted'].transform('count')
    txpool_block['ico'] = (txpool_block['num_to'] > 90).astype(int)
    txpool_block['dump'] = (txpool_block['num_from'] > 5).astype(int)
    txpool_block['high_gas_offered'] = (txpool_block['pct_limit']> .037).astype(int)
    txpool_block['highgas2'] = (txpool_block['pct_limit'] > .15).astype(int)
    txpool_block['expectedWait'] = txpool_block.apply(predict, axis=1)
    txpool_block['mined_probability'] = txpool_block.apply(predict_mined, axis=1)
    txpool_block['expectedWait'] = txpool_block['expectedWait'].apply(lambda x: 2 if (x < 2) else x)
    txpool_block['expectedWait'] = txpool_block['expectedWait'].apply(lambda x: np.round(x, decimals=2))
    txpool_block['expectedTime'] = txpool_block['expectedWait'].apply(lambda x: np.round((x * avg_timemined / 60), decimals=2))
    return(txpool_block)

def get_gasprice_recs(prediction_table, block_time, block, speed, minlow=-1):
    def get_safelow():
        series = prediction_table.loc[prediction_table['expectedTime'] <= 20, 'gasprice']
        safelow = series.min()
        minhash_list = prediction_table.loc[prediction_table['hashpower_accepting']>=1.5, 'gasprice']
        if (safelow < minhash_list.min()):
            safelow = minhash_list.min()
        if minlow >= 0:
            if safelow < minlow:
                safelow = minlow
        return (safelow)

    def get_average():
        series = prediction_table.loc[prediction_table['expectedTime'] <= 5, 'gasprice']
        average = series.min()
        minhash_list = prediction_table.loc[prediction_table['hashpower_accepting']>35, 'gasprice']
        if average < minhash_list.min():
            average= minhash_list.min()
        return (average)

    def get_fast():
        series = prediction_table.loc[prediction_table['expectedTime'] <= 2, 'gasprice']
        fastest = series.min()
        minhash_list = prediction_table.loc[prediction_table['hashpower_accepting']>90, 'gasprice']
        if fastest < minhash_list.min():
            fastest = minhash_list.min()
        if np.isnan(fastest):
            fastest = 100
        return (fastest)

    def get_fastest():
        fastest = prediction_table['expectedTime'].min()
        series = prediction_table.loc[prediction_table['expectedTime'] == fastest, 'gasprice']
        fastest = series.min()
        minhash_list = prediction_table.loc[prediction_table['hashpower_accepting']>95, 'gasprice']
        if fastest < minhash_list.min():
            fastest = minhash_list.min()
        return (fastest) 

    def get_wait(gasprice):
        wait =  prediction_table.loc[prediction_table['gasprice']==gasprice, 'expectedWait'].values[0]
        wait = round(wait, 1)
        return wait
    
    gprecs = {}
    gprecs['safeLow'] = get_safelow()
    gprecs['safeLowWait'] = get_wait(gprecs['safeLow'])
    gprecs['average'] = get_average()
    gprecs['avgWait'] = get_wait(gprecs['average'])
    gprecs['fast'] = get_fast()
    gprecs['fastWait'] = get_wait(gprecs['fast'])
    gprecs['fastest'] = get_fastest()
    gprecs['fastestWait'] = get_wait(gprecs['fastest'])
    gprecs['block_time'] = block_time
    gprecs['blockNum'] = block
    gprecs['speed'] = speed
    return(gprecs)

def filter_transactions():
    """filter and add to dataframe"""
    (blockdata, alltx) = init_dfs()
    txpool = pd.DataFrame()
    print ('blocks '+ str(len(blockdata)))
    print ('txcount '+ str(len(alltx)))
    print(blockdata)
    print(alltx)
    timer = Timers(web3.eth.blockNumber)
    tx_filter = web3.eth.filter('pending')

    def manage_dataframes(clean_tx, block):
        nonlocal alltx
        nonlocal txpool
        nonlocal blockdata
        if not clean_tx.hash in alltx.index:
            alltx = alltx.append(clean_tx.to_dataframe(), ignore_index = False)
        if timer.check_newblock(block):
            print (block)
            if block <= timer.start_block+1:
                return
            try:
                #get minedtransactions and blockdata from previous block
                (mined_blockdf, block_obj) = process_block_transactions(block - 3)
                #add mined data to tx dataframe - only unique hashes seen by node
                mined_blockdf_seen = mined_blockdf[mined_blockdf.index.isin(alltx.index)]
                alltx = alltx.combine_first(mined_blockdf_seen)
                #process block data
                block_sumdf = process_block_data(mined_blockdf, block_obj)
                #add block data to block dataframe 
                blockdata = blockdata.append(block_sumdf, ignore_index = True)
                #get list of txhashes from txpool 
                current_txpool = get_txhases_from_txpool(block)
                #add txhashes to txpool dataframe
                txpool = txpool.append(current_txpool, ignore_index = False)
                #get txhashes removed in current blocks txpool add data to alltx
                prior_txpool = txpool[txpool['block']==(block-1)]
                removed_txhashes = get_diff(current_txpool.index.tolist(), prior_txpool.index.tolist(), block)
                removed_txhashes = removed_txhashes[removed_txhashes.index.isin(alltx.index)]
                print ('removed_txhashes ' + str(len(removed_txhashes)))
                alltx = alltx.combine_first(removed_txhashes)
                #get hashpower table, block interval time, gaslimit, speed from last 200 blocks
                (hashpower, block_time, gaslimit, speed) = analyze_last200blocks(block, blockdata)
                #keep txpool dataframe from getting too big
                txpool = txpool.loc[txpool['block']>(block-5)]
                #make txpool block data
                (txpool_block, txpool_by_gp) = merge_txpool_alltx(txpool, alltx, block-1)
                #make prediction table
                (gp_lookup, txatabove_lookup, predictiondf) = make_predictiontable(hashpower, block_time, txpool_by_gp)
                #get gpRecs
                gprecs = get_gasprice_recs (predictiondf, block_time, block, speed)
                print(gprecs)
                #analyze block transactions within txpool
                analyzed_block = analyze_txpool(block-1, gp_lookup, txatabove_lookup, txpool_block, gaslimit, block_time)
                assert analyzed_block.index.duplicated().sum()==0
                # update tx dataframe with txpool variables and time preidctions
                alltx = alltx.combine_first(analyzed_block)
                with pd.option_context('display.max_columns', None,):
                    print(alltx)
                if timer.check_reportblock(block):
                    last500t = alltx[alltx['block_posted'] > (block-500)].copy()
                    last500b = blockdata[blockdata['block_number'] > (block-500)].copy()
                    report = SummaryReport(last500t, last500b, block)
                    print (report.post)
                post = alltx[alltx.index.isin(mined_blockdf_seen.index)]
                post.to_sql(con=engine, name = 'minedtx2', if_exists='append', index=True)
                post2 = alltx.loc[alltx['block_posted']==(block-1)]
                post2.to_sql(con=engine, name = 'postedtx2', if_exists='append', index=True)
                analyzed_block.reset_index(drop=False, inplace=True)
                analyzed_block.to_sql(con=engine, name='txpool_current', index=False, if_exists='replace')
                block_sumdf.to_sql(con=engine, name='blockdata2', if_exists='append', index=False)
            except: 
                print(traceback.format_exc())
    

    def new_tx_callback(tx_hash):
        try:
            block = web3.eth.blockNumber
            tx_obj = web3.eth.getTransaction(tx_hash)
            timestamp = time.time()
            clean_tx = CleanTx(tx_obj, block, timestamp)
            manage_dataframes(clean_tx, block)
        except AttributeError as e:
            print(e)

    while True:
        tx_filter.watch(new_tx_callback)
        response = input("type q to quit \n")
        if response == 'q':
            break

filter_transactions()
