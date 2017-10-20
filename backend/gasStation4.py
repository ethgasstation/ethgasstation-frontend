import time
import logging
import sys
import json
import math
import traceback
import os
import pandas as pd
import threading
import numpy as np
from web3 import Web3, HTTPProvider
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, BigInteger, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from egs import *

web3 = Web3(HTTPProvider('http://localhost:8545'))
engine = create_engine(
    'mysql+mysqlconnector://ethgas:station@127.0.0.1:3306/tx', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def init_dfs():
    """load data from mysql"""
    blockdata = pd.read_sql('SELECT * from blockdata2 order by id desc limit 2000', con=engine)
    blockdata = blockdata.drop('id', axis=1)
    postedtx = pd.read_sql('SELECT * from postedtx2 order by id desc limit 100000', con=engine)
    minedtx = pd.read_sql('SELECT * from minedtx2 order by id desc limit 100000', con=engine)
    minedtx.set_index('index', drop=True, inplace=True)
    alltx = postedtx[['index', 'expectedTime', 'expectedWait', 'mined_probability', 'highgas2', 'from_address', 'gas_offered', 'gas_price', 'hashpower_accepting', 'num_from', 'num_to', 'ico', 'dump', 'high_gas_offered', 'pct_limit', 'round_gp_10gwei', 'time_posted', 'block_posted', 'to_address', 'tx_atabove', 'wait_blocks', 'chained', 'nonce']].join(minedtx[['block_mined', 'miner', 'time_mined', 'removed_block']], on='index', how='left')
    alltx.set_index('index', drop=True, inplace=True)
    return(blockdata, alltx)

def prune_data(blockdata, alltx, txpool, block):
    """keep dataframes and databases from getting too big"""
    stmt = text("DELETE FROM postedtx2 WHERE block_posted <= :block")
    stmt2 = text("DELETE FROM minedtx2 WHERE block_mined <= :block")
    deleteBlock = block-2000
    session.query(Tx_Sql).from_statement(stmt).params(block=deleteBlock)
    session.query(Mined_Sql).from_statement(stmt).params(block=deleteBlock)
    alltx = alltx.loc[alltx['block_posted'] > deleteBlock]
    blockdata = blockdata.loc[blockdata['block_number'] > deleteBlock]
    txpool = txpool.loc[txpool['block'] > (block-5)]
    return (blockdata, alltx, txpool)

def write_to_sql(alltx, analyzed_block, block_sumdf, mined_blockdf_seen, block):
    """write data to mysql for analysis"""
    post = alltx[alltx.index.isin(mined_blockdf_seen.index)]
    post.to_sql(con=engine, name='minedtx2', if_exists='append', index=True)
    print ('num mined = ' + str(len(post)))
    post2 = alltx.loc[alltx['block_posted'] == (block-1)]
    post2.to_sql(con=engine, name='postedtx2', if_exists='append', index=True)
    print ('num posted = ' + str(len(post2)))
    analyzed_block.reset_index(drop=False, inplace=True)
    analyzed_block.to_sql(con=engine, name='txpool_current', index=False, if_exists='replace')
    block_sumdf.to_sql(con=engine, name='blockdata2', if_exists='append', index=False)

def write_report(report, top_miners, price_wait, miner_txdata, gasguzz, lowprice):
    """write json data"""
    parentdir = os.path.dirname(os.getcwd())
    top_minersout = top_miners.to_json(orient='records')
    minerout = miner_txdata.to_json(orient='records')
    gasguzzout = gasguzz.to_json(orient='records')
    lowpriceout = lowprice.to_json(orient='records')
    price_waitout = price_wait.to_json(orient='records')
    filepath_report = parentdir + '/json/txDataLast10k.json'
    filepath_tminers = parentdir + '/json/topMiners.json'
    filepath_pwait = parentdir + '/json/priceWait.json'
    filepath_minerout = parentdir + '/json/miners.json'
    filepath_gasguzzout = parentdir + '/json/gasguzz.json'
    filepath_lowpriceout = parentdir + '/json/validated.json'

    try:
        with open(filepath_report, 'w') as outfile:
            json.dump(report, outfile, allow_nan=False)
        with open(filepath_tminers, 'w') as outfile:
            outfile.write(top_minersout)
        with open(filepath_pwait, 'w') as outfile:
            outfile.write(price_waitout)
        with open(filepath_minerout, 'w') as outfile:
            outfile.write(minerout)
        with open(filepath_gasguzzout, 'w') as outfile:
            outfile.write(gasguzzout)
        with open(filepath_lowpriceout, 'w') as outfile:
            outfile.write(lowpriceout)

    except Exception as e:
        print(e)

def write_to_json(gprecs, txpool_by_gp, prediction_table):
    """write json data"""
    try:
        txpool_by_gp = txpool_by_gp.rename(columns={'gas_price':'count'})
        txpool_by_gp['gasprice'] = txpool_by_gp['round_gp_10gwei']/10
        txpool_by_gp['gas_offered'] = txpool_by_gp['gas_offered']/1e6
        prediction_table['gasprice'] = prediction_table['gasprice']/10
        prediction_tableout = prediction_table.to_json(orient='records')
        txpool_by_gpout = txpool_by_gp.to_json(orient='records')
        parentdir = os.path.dirname(os.getcwd())
        filepath_gprecs = parentdir + '/json/ethgasAPI.json'
        filepath_txpool_gp = parentdir + '/json/memPool.json'
        filepath_prediction_table = parentdir + '/json/predictTable.json'
        with open(filepath_gprecs, 'w') as outfile:
            json.dump(gprecs, outfile)

        with open(filepath_prediction_table, 'w') as outfile:
            outfile.write(prediction_tableout)

        with open(filepath_txpool_gp, 'w') as outfile:
            outfile.write(txpool_by_gpout)
    
    except Exception as e:
        print(e)
    
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
    """get tx data from block"""
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
    """process block to dataframe"""
    if len(block_obj.transactions) > 0:
        block_df['weighted_fee'] = block_df['round_gp_10gwei']* block_df['gas_offered']
        block_mingasprice = block_df['round_gp_10gwei'].min()
        block_weightedfee = block_df['weighted_fee'].sum() / block_df['gas_offered'].sum()
    else:
        block_mingasprice = np.nan
        block_weightedfee = np.nan
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

def get_tx_atabove(gasprice, txpool_by_gp):
    """gets the number of transactions in the txpool at or above the given gasprice"""
    txAtAb = txpool_by_gp.loc[txpool_by_gp.index >= gasprice, 'gas_price']
    if gasprice > txpool_by_gp.index.max():
        txAtAb = 0
    else:
        txAtAb = txAtAb.sum()
    return txAtAb

def get_tx_unchained(gasprice, txpool_by_gp_unchained):
    """gets the number of nonce-filtered in the txpool at or above the given gasprice"""
    txAtAb = txpool_by_gp_unchained.loc[txpool_by_gp.index >= gasprice, 'gas_price']
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
    try:
        sum1 = (intercept + (row['hashpower_accepting']*hpa_coef) + (row['tx_atabove']*txatabove_coef) + (row['ico']*ico_coef) + (row['dump']*dump_coef) + (row['high_gas_offered']*high_gas_coef))
        return np.exp(sum1)
    except Exception:
        print(e)
        return np.nan

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
    #get txpool hashes at block
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
    txpool_by_gp = txpool_block[['gas_price', 'round_gp_10gwei']].groupby('round_gp_10gwei').agg({'gas_price':'count'})
    txpool_by_gp.reset_index(inplace=True, drop=False)
    txpool_block_unchained = txpool_block.loc[txpool_block['chained']==0]
    txpool_by_gp_unchained = txpool_block_unchained[['gas_price', 'round_gp_10gwei']].groupby('round_gp_10gwei').agg({'gas_price':'count'})
    return(txpool_block, txpool_by_gp, txpool_by_gp_unchained)

def make_predictiontable(hashpower, avg_timemined, txpool_by_gp, txpool_by_gp_unchained):
    predictTable = pd.DataFrame({'gasprice' :  range(10, 1010, 10)})
    ptable2 = pd.DataFrame({'gasprice' : range(0, 10, 1)})
    predictTable = predictTable.append(ptable2).reset_index(drop=True)
    predictTable = predictTable.sort_values('gasprice').reset_index(drop=True)
    predictTable['hashpower_accepting'] = predictTable['gasprice'].apply(get_hpa, args=(hashpower,))
    predictTable['tx_atabove'] = predictTable['gasprice'].apply(get_tx_atabove, args=(txpool_by_gp,))
    predictTable['tx_atabove_unchained'] = predictTable['gasprice'].apply(get_tx_unchained, args=(txpool_by_gp_unchained,))
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
    tx_unchained_lookup = predictTable.set_index('gasprice')['tx_atabove_unchained'].to_dict()
    return(gp_lookup, txatabove_lookup, tx_unchained_lookup, predictTable)

def get_adjusted_post(row, block):
    if row['chained'] == 1:
        return np.nan
    elif (row['chained']==0 and row['temp_chained']==1):
        return block
    elif (row['chained']==0 and row['temp_chained']==0):
        return row['block_posted']
    elif (row['chained']==0 and row['temp_chained']==np.nan):
        return row['block_posted']
    else:
        pass

def analyze_txpool(block, gp_lookup, txatabove_lookup, txpool_block, gaslimit, avg_timemined, txpool_by_gp, txpool_by_gp_unchained, tx_unchained_lookup):
    '''defines prediction parameters for all transactions in the txpool'''
    print('txpool block length ' + str(len(txpool_block)))
    txpool_block['pct_limit'] = txpool_block['gas_offered'].apply(lambda x: x / gaslimit)
    txpool_block['hashpower_accepting'] = txpool_block['round_gp_10gwei'].apply(lambda x: gp_lookup[x] if x in gp_lookup else 100)
    txpool_block['num_from'] = txpool_block.groupby('from_address')['block_posted'].transform('count')
    txpool_block_nonce = txpool_block[['from_address', 'nonce']].groupby('from_address').agg({'nonce':'min'})
    txpool_block['temp_chained'] = txpool_block['chained']
    txpool_block['chained'] = txpool_block.apply(check_nonce, args=(txpool_block_nonce,), axis=1)
    txpool_block['tx_atabove'] = txpool_block['round_gp_10gwei'].apply(lambda x: txatabove_lookup[x] if x in txatabove_lookup else 1)
    txpool_block['tx_unchained'] = txpool_block['round_gp_10gwei'].apply(lambda x: tx_unchained_lookup[x] if x in tx_unchained_lookup else 1)
    txpool_block['block_posted_adj'] = txpool_block.apply(get_adjusted_post, args = (block,), axis=1)
    txpool_block['num_to'] = txpool_block.groupby('to_address')['block_posted'].transform('count')
    txpool_block['ico'] = (txpool_block['num_to'] > 90).astype(int)
    txpool_block['dump'] = (txpool_block['num_from'] > 5).astype(int)
    txpool_block['high_gas_offered'] = (txpool_block['pct_limit']> .037).astype(int)
    txpool_block['highgas2'] = (txpool_block['pct_limit'] > .15).astype(int)
    txpool_block['expectedWait'] = txpool_block.apply(predict, axis=1)
    txpool_block['expectedWait'] = txpool_block['expectedWait'].apply(lambda x: 2 if (x < 2) else x)
    txpool_block['expectedWait'] = txpool_block['expectedWait'].apply(lambda x: np.round(x, decimals=2))
    txpool_block['expectedTime'] = txpool_block['expectedWait'].apply(lambda x: np.round((x * avg_timemined / 60), decimals=2))
    txpool_block['wait_blocks'] = txpool_block['block_posted_adj'].apply(lambda x: block-x)
    txpool_block['mined_probability'] = txpool_block.apply(predict_mined, axis=1)
    txpool_by_gp = txpool_block[['wait_blocks', 'gas_offered', 'gas_price', 'round_gp_10gwei']].groupby('round_gp_10gwei').agg({'wait_blocks':'median','gas_offered':'sum', 'gas_price':'count'})
    txpool_by_gp.reset_index(inplace=True, drop=False)
    txpool_block = txpool_block.drop(['block_posted_adj', 'temp_chained'], axis=1)
    return(txpool_block, txpool_by_gp)

def get_gasprice_recs(prediction_table, block_time, block, speed, minlow=-1):
    
    def get_safelow(minlow):
        series = prediction_table.loc[prediction_table['expectedTime'] <= 10, 'gasprice']
        safelow = series.min()
        print('safelow1 = ' + str(safelow))
        minhash_list = prediction_table.loc[prediction_table['hashpower_accepting']>=1.5, 'gasprice']
        if (safelow < minhash_list.min()):
            safelow = minhash_list.min()
        print('safelow2 = ' + str(safelow))
        if minlow >= 0:
            if safelow < minlow:
                safelow = minlow
        return float(safelow)

    def get_average():
        series = prediction_table.loc[prediction_table['expectedTime'] <= 4, 'gasprice']
        average = series.min()
        minhash_list = prediction_table.loc[prediction_table['hashpower_accepting']>35, 'gasprice']
        if average < minhash_list.min():
            average= minhash_list.min()
        return float(average)

    def get_fast():
        series = prediction_table.loc[prediction_table['expectedTime'] <= 1, 'gasprice']
        fastest = series.min()
        minhash_list = prediction_table.loc[prediction_table['hashpower_accepting']>90, 'gasprice']
        if fastest < minhash_list.min():
            fastest = minhash_list.min()
        if np.isnan(fastest):
            fastest = 100
        return float(fastest)

    def get_fastest():
        fastest = prediction_table['expectedTime'].min()
        series = prediction_table.loc[prediction_table['expectedTime'] == fastest, 'gasprice']
        fastest = series.min()
        minhash_list = prediction_table.loc[prediction_table['hashpower_accepting']>95, 'gasprice']
        if fastest < minhash_list.min():
            fastest = minhash_list.min()
        return float(fastest) 

    def get_wait(gasprice):
        try:
            wait =  prediction_table.loc[prediction_table['gasprice']==gasprice, 'expectedTime'].values[0]
        except:
            wait = 0
        wait = round(wait, 1)
        return float(wait)
    
    print ('minlow = ' + str(minlow))
    gprecs = {}
    gprecs['safeLow'] = get_safelow(minlow)
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

def get_recent_txtime():
    global alltx
    last_time = alltx['time_posted'].max()
    return last_time

def check_filter(start_time, current_time, recent_txtime):
    if (start_time > recent_txtime):
        print('starting up')
        last_tx = start_time - recent_txtime
        print('last tx was ' +str(last_tx)+ ' seconds ago')
        return 0
    if (current_time - recent_txtime) > 60:
        print ('filter lost')
        return 1
    return 0


def master_control():
    start_time = time.time()
    tx_filter = web3.eth.filter('pending')
    def new_tx_callback(tx_hash):
        try:
            block = web3.eth.blockNumber
            tx_obj = web3.eth.getTransaction(tx_hash)
            timestamp = time.time()
            clean_tx = CleanTx(tx_obj, block, timestamp)
            append_new_tx(clean_tx, block)
        except AttributeError as e:
            print(e)
    try:
        while True:
            current_time = time.time()
        
            #check for new tx from filter
            recent_txtime = get_recent_txtime()
            print('time since last tx ' + str(current_time - recent_txtime))
        
            #determine if filter is lost
            lost_filter = check_filter(start_time, current_time, recent_txtime)
            if lost_filter:
                print('lost filter')
                tx_filter.stop_watching()
                tx_filter = web3.eth.filter('pending')
            else:
                print ('filter ok')

            #check if filter is running. if not, start
            if not tx_filter.running:
                print('starting up filter')
                tx_filter.watch(new_tx_callback)
            print('threadlist:')
            print(threading.enumerate())
            time.sleep(15)
    
    except KeyboardInterrupt:
        print('ending')
        

def append_new_tx(clean_tx, block):
    global alltx
    global timer
    if not clean_tx.hash in alltx.index:
        alltx = alltx.append(clean_tx.to_dataframe(), ignore_index = False)
    if timer.check_newblock(block):
        print (block)
        if block > timer.start_block+1:
            update_dataframes(block)
    

def update_dataframes(block):
    global alltx
    global txpool
    global blockdata
        
    print('updating dataframes at block '+ str(block))
    try:
        #get minedtransactions and blockdata from previous block
        mined_block_num = block-3
        (mined_blockdf, block_obj) = process_block_transactions(mined_block_num)
        #add mined data to tx dataframe - only unique hashes seen by node
        mined_blockdf_seen = mined_blockdf[mined_blockdf.index.isin(alltx.index)]
        print('num mined in ' + str(mined_block_num)+ ' = ' + str(len(mined_blockdf)))
        print('num seen in ' + str(mined_block_num)+ ' = ' + str(len(mined_blockdf_seen)))
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
        #make txpool block data
        (txpool_block, txpool_by_gp, txpool_by_gp_unchained) = merge_txpool_alltx(txpool, alltx, block-1)
        #make prediction table
        (gp_lookup, txatabove_lookup, tx_unchained_lookup, predictiondf) = make_predictiontable(hashpower, block_time, txpool_by_gp, txpool_by_gp_unchained)
        #get gpRecs
        gprecs = get_gasprice_recs (predictiondf, block_time, block, speed, timer.minlow)
        #analyze block transactions within txpool
        (analyzed_block, txpool_by_gp) = analyze_txpool(block-1, gp_lookup, txatabove_lookup, txpool_block, gaslimit, block_time, txpool_by_gp, txpool_by_gp_unchained, tx_unchained_lookup)
        assert analyzed_block.index.duplicated().sum()==0
        #with pd.option_context('display.max_columns', None,):
            #print(analyzed_block)
        # update tx dataframe with txpool variables and time preidctions
        alltx = alltx.combine_first(analyzed_block)
        #with pd.option_context('display.max_columns', None,):
            #print(alltx)
        if timer.check_reportblock(block):
            last1500t = alltx[alltx['block_posted'] > (block-1500)].copy()
            print('txs '+ str(len(last1500t)))
            last1500b = blockdata[blockdata['block_number'] > (block-1500)].copy()
            print('blocks ' +  str(len(last1500b)))
            report = SummaryReport(last1500t, last1500b, block)
            write_report(report.post, report.top_miners, report.price_wait, report.miner_txdata, report.gasguzz, report.lowprice)
            timer.minlow = report.minlow
        write_to_json(gprecs, txpool_by_gp, predictiondf)
        write_to_sql(alltx, analyzed_block, block_sumdf, mined_blockdf_seen, block)
        (blockdata, alltx, txpool) = prune_data(blockdata, alltx, txpool, block)
    except: 
        print(traceback.format_exc())   
    
(blockdata, alltx) = init_dfs()
txpool = pd.DataFrame()
print ('blocks '+ str(len(blockdata)))
print ('txcount '+ str(len(alltx)))
timer = Timers(web3.eth.blockNumber)  
master_control()
