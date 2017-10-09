import pandas as pd
import numpy as np
import json
import urllib
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Mined_Sql(Base):
    __tablename__ = 'minedtx2'
    id = Column(Integer, primary_key = True)
    index = Column(String(75))
    block_mined = Column(Integer)
    block_posted = Column(Integer)
    expectedTime = Column(DECIMAL(5,2))
    expectedWait = Column(DECIMAL(5,2))
    mined_probability = Column(DECIMAL(5,3))
    highgas2 = Column(Integer)
    from_address = Column(String(60))
    gas_offered = Column(Integer)
    gas_price = Column(BigInteger)
    hashpower_accepting = Column(Integer)
    miner = Column(String(60))
    num_from = Column(Integer)
    num_to = Column(Integer)
    ico = Column(Integer)
    dump = Column(Integer)
    high_gas_offered =  Column(Integer)
    pct_limit = Column(DECIMAL(5,4))
    removed_block = Column(Integer)
    round_gp_10gwei = Column(Integer)
    time_posted = Column(Integer)
    time_mined = Column(Integer)
    to_address = Column(String(60))
    tx_atabove = Column(Integer)
    wait_blocks = Column(Integer)
    chained = Column(Integer)
    nonce = Column(Integer)

class Tx_Sql(Base):
    __tablename__ = 'postedtx2'
    id = Column(Integer, primary_key = True)
    index = Column(String(75))
    block_mined = Column(Integer)
    block_posted = Column(Integer)
    expectedTime = Column(DECIMAL(5,2))
    expectedWait = Column(DECIMAL(5,2))
    mined_probability = Column(DECIMAL(5,3))
    from_address = Column(String(60))
    gas_offered = Column(Integer)
    gas_price = Column(BigInteger)
    highgas2 = Column(Integer)
    hashpower_accepting = Column(Integer)
    miner = Column(String(60))
    num_from = Column(Integer)
    num_to = Column(Integer)
    ico = Column(Integer)
    dump = Column(Integer)
    high_gas_offered =  Column(Integer)
    pct_limit = Column(DECIMAL(5,4))
    removed_block = Column(Integer)
    round_gp_10gwei = Column(Integer)
    time_posted = Column(Integer)
    time_mined = Column(Integer)
    to_address = Column(String(60))
    tx_atabove = Column(Integer)
    wait_blocks = Column(Integer)
    nonce = Column(Integer)
    chained = Column(Integer)

class Block_Data(Base):
    __tablename__= 'blockdata2'
    id = Column(Integer, primary_key = True)
    blockhash = Column(String(75))
    includedblock = Column(Integer)
    mingasprice = Column(Integer)
    blockfee = Column(DECIMAL(5,5))
    gaslimit = Column(Integer)
    gasused = Column(Integer)
    time_mined = Column(Integer)
    uncsreported = Column(Integer)
    speed = Column(DECIMAL(3,3))
    miner = Column(String(60))
    numtx = Column(Integer)
    uncle = Column(Integer)
    main = Column(Integer)
    block_number = Column(Integer)

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

    def check_reportblock(self, block):
        if (block - (self.start_block-1))%100 == 0:
            print (str(block) + ' ' + str(self.start_block))
            return True
        return False

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
        self.nonce = tx_obj['nonce']

    def to_dataframe(self):
        data = {self.hash: {'block_posted':self.block_posted, 'block_mined':self.block_mined, 'to_address':self.to_address, 'from_address':self.from_address, 'nonce':self.nonce, 'time_posted':self.time_posted, 'time_mined': None, 'gas_price':self.gas_price, 'miner':self.miner, 'gas_offered':self.gas_offered, 'round_gp_10gwei':self.gp_10gwei}}
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
        self.speed = self.gasused / self.gaslimit
    
    def to_dataframe(self):
        data = {0:{'block_number':self.block_number, 'gasused':self.gasused, 'miner':self.miner, 'gaslimit':self.gaslimit, 'numtx':self.numtx, 'blockhash':self.blockhash, 'time_mined':self.time_mined, 'mingasprice':self.mingasprice, 'uncsreported':self.uncsreported, 'blockfee':self.blockfee, 'main':self.main, 'uncle':self.uncle, 'speed':self.speed, 'includedblock':self.includedblock}}
        return pd.DataFrame.from_dict(data, orient = 'index')

class SummaryReport():
    def __init__(self, tx_df, block_df, end_block):
        self.end_block = end_block
        self.tx_df = tx_df
        self.block_df = block_df
        self.post = {}

        self.tx_df['minedGasPrice'] = self.tx_df['round_gp_10gwei'].apply(lambda x: x/10)
        self.tx_df['gasCat1'] = (self.tx_df['minedGasPrice'] <= 1)
        self.tx_df['gasCat2'] = (self.tx_df['minedGasPrice']>1) & (self.tx_df['minedGasPrice']<= 4)
        self.tx_df['gasCat3'] = (self.tx_df['minedGasPrice']>4) & (self.tx_df['minedGasPrice']<= 20)
        self.tx_df['gasCat4'] = (self.tx_df['minedGasPrice']>20) & (self.tx_df['minedGasPrice']<= 50)
        self.tx_df['gasCat5'] = (self.tx_df['minedGasPrice']>50) 
        self.block_df['emptyBlocks'] = (self.block_df['numtx']==0).astype(int)
        self.tx_df['mined'] = self.tx_df['block_mined'].notnull()
        self.tx_df['delay'] = self.tx_df['block_mined'] - self.tx_df['block_posted']
        self.tx_df['delay2'] = self.tx_df['time_mined'] - self.tx_df['time_posted']
        self.tx_df.loc[self.tx_df['delay'] <= 0, 'delay'] = np.nan
        self.tx_df.loc[self.tx_df['delay2'] <= 0, 'delay2'] = np.nan

        total_tx = len(self.tx_df)
        self.post['latestblockNum'] = self.end_block
        self.post['totalTx'] = total_tx
        self.post['totalCatTx1'] = self.tx_df['gasCat1'].sum()
        self.post['totalCatTx2'] = self.tx_df['gasCat2'].sum()
        self.post['totalCatTx3'] = self.tx_df['gasCat3'].sum()
        self.post['totalCatTx4'] = self.tx_df['gasCat4'].sum()
        self.post['totalCatTx5'] = self.tx_df['gasCat5'].sum()
        self.post['totalTransfers'] = len(self.tx_df[self.tx_df['gas_offered']==21000])
        self.post['totalConCalls'] = len(self.tx_df[self.tx_df['gas_offered']!=21000])
        self.post['maxMinedGasPrice'] = self.tx_df['minedGasPrice'].max()
        self.post['minMinedGasPrice'] = self.tx_df['minedGasPrice'].min()
        self.post['medianGasPrice']= int(self.tx_df['minedGasPrice'].quantile(.5))
        self.post['cheapestTx'] = self.tx_df.loc[self.tx_df['gas_offered']==21000, 'minedGasPrice'].min()
        self.post['cheapestTxID'] = self.tx_df.loc[(self.tx_df['minedGasPrice']==self.post['cheapestTx']) & (self.tx_df['gas_offered'] == 21000)].index[0]
        self.post['dearestTx'] = self.tx_df.loc[self.tx_df['gas_offered']==21000, 'minedGasPrice'].max()
        self.post['dearestTxID'] = self.tx_df.loc[(self.tx_df['minedGasPrice']==self.post['dearestTx']) & (self.tx_df['gas_offered'] == 21000)].index[0]
        self.post['emptyBlocks'] =  len(self.block_df[self.block_df['speed']==0])
        self.post['fullBlocks'] = len(self.block_df[self.block_df['speed']>=.95])
        self.post['totalBlocks'] = len(self.block_df)
        self.post['medianDelay'] = self.tx_df['delay'].quantile(.5)
        self.post['medianDelayTime'] = self.tx_df['delay2'].quantile(.5)
        
        url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR,GBP,CNY"
        with urllib.request.urlopen(url) as response:
            pricesRaw = json.loads(response.read().decode())
        ethPricesTable = pd.DataFrame.from_dict(pricesRaw, orient='index')
        self.post['ETHpriceUSD'] = int(ethPricesTable.loc['USD', 0])
        self.post['ETHpriceEUR'] = int(ethPricesTable.loc['EUR', 0])
        self.post['ETHpriceCNY'] = int(ethPricesTable.loc['CNY', 0])
        self.post['ETHpriceGBP'] = int(ethPricesTable.loc['GBP', 0])
    
        """find minimum gas price with at least 50 transactions mined"""
        tx_grouped_price = self.tx_df[['block_posted', 'minedGasPrice']].groupby('minedGasPrice').count()
        tx_grouped_price.rename(columns = {'block_posted': 'count'}, inplace = True)
        tx_grouped_price['sum'] = tx_grouped_price['count'].cumsum()
        minlow_series = tx_grouped_price[tx_grouped_price['sum']>50].index
        self.post['minLow'] = minlow_series.min()
    
        """generate table with key miner stats"""
        miner_txdata = self.tx_df[['block_posted', 'miner']].groupby('miner').count()
        miner_txdata.rename(columns={'block_posted':'count'}, inplace = True)
        # Next Find Each Miners Mininum Price of All Mined Transactions
        minprice_df = self.tx_df[['miner', 'minedGasPrice']].groupby('miner').min()
        minprice_df = minprice_df.rename(columns={"minedGasPrice": 'minGasPrice'})
        avgprice_df = self.tx_df[['miner', 'minedGasPrice']].groupby('miner').mean()
        avgprice_df = avgprice_df.rename(columns={"minedGasPrice": 'avgGasPrice'})
        miner_txdata = pd.concat([miner_txdata, minprice_df], axis = 1)
        miner_txdata = pd.concat([miner_txdata, avgprice_df], axis = 1)
        # Calculate Each Miners % Empty and Total Blocks
        miner_blocks = block_df[['miner','emptyBlocks','block_number']].groupby('miner').agg({'emptyBlocks':'sum', 'block_number':'count'})
        miner_txdata = pd.concat([miner_txdata, miner_blocks], axis = 1)
        miner_txdata.reset_index(inplace=True)
        miner_txdata = miner_txdata.rename(columns={'index':'miner', 'block_number':'totBlocks'})
        #Convert to percentages
        total_blocks = miner_txdata['totBlocks'].sum()
        miner_txdata['pctTot'] = miner_txdata['totBlocks']/total_blocks*100
        miner_txdata['pctEmp'] = miner_txdata['emptyBlocks']/miner_txdata['totBlocks']*100
        miner_txdata['txBlocks'] = miner_txdata['totBlocks'] - miner_txdata['emptyBlocks']
        tot_txblocks = miner_txdata['txBlocks'].sum()
        miner_txdata['pctTxBlocks'] = miner_txdata['txBlocks']/tot_txblocks*100
        pct_txblocks = tot_txblocks/total_blocks
        miner_txdata  = miner_txdata.sort_values(['minGasPrice','totBlocks'], ascending = [True, False])
        #Make Table with top10 Miner Stats
        top_miners = miner_txdata.sort_values('totBlocks', ascending=False)
        top_miners = top_miners.loc[:,['miner','minGasPrice','avgGasPrice', 'pctTot']].head(10)
        top_miners = top_miners.sort_values(['minGasPrice','avgGasPrice'], ascending = [True, True]).reset_index(drop=True)
        #Table with hashpower by gasprice
        price_table = miner_txdata[['pctTxBlocks', 'minGasPrice']].groupby('minGasPrice').sum().reset_index()
        price_table['pctTotBlocks'] = price_table['pctTxBlocks'] * pct_txblocks
        price_table['cumPctTxBlocks'] = price_table['pctTxBlocks'].cumsum()
        price_table['cumPctTotBlocks'] = price_table['pctTotBlocks'].cumsum()
        #store dataframes for json
        self.miner_txdata = miner_txdata
        self.top_miners = top_miners
        self.price_table = price_table

        '''gas guzzler table'''
        gg = {
            '0x6090a6e47849629b7245dfa1ca21d94cd15878ef': 'ENS registrar',
            '0xcd111aa492a9c77a367c36e6d6af8e6f212e0c8e': 'Acronis',
            '0x209c4784ab1e8183cf58ca33cb740efbf3fc18ef': 'Poloniex',
            '0xece701c76bd00d1c3f96410a0c69ea8dfcf5f34e': 'Etheroll',
            '0xa74476443119a942de498590fe1f2454d7d4ac0d': 'Golem',
            '0xedce883162179d4ed5eb9bb2e7dccf494d75b3a0': 'Bittrex',
            '0x70faa28a6b8d6829a4b1e649d26ec9a2a39ba413': 'Shapeshift',
            '0xff1f9c77a0f1fd8f48cfeee58b714ca03420ddac': 'e4row',
            '0x8d12a197cb00d4747a1fe03395095ce2a5cc6819': 'Etherdelta',
            '0xe94b04a0fed112f3664e45adb2b8915693dd5ff3': 'Bittrex Safe Split',
            '0xace62f87abe9f4ee9fd6e115d91548df24ca0943': 'Monaco',
            '0xb9e7f8568e08d5659f5d29c4997173d84cdf2607': 'Swarm City'
        }
        gasguzz = self.tx_df.groupby('to_address').count()
        gasguzz = gasguzz.sort_values('block_posted', ascending = False)
        tottx = len(self.tx_df)
        gasguzz['pcttot'] = gasguzz['block_posted']/tottx*100
        gasguzz = gasguzz.head(n=10)
        for index, row in gasguzz.iterrows():
            if index in gg.keys():
                gasguzz.loc[index, 'ID'] = gg[index]
            else:
                gasguzz.loc[index, 'ID'] = ''
        gasguzz = gasguzz.reset_index()
        self.gasguzz = gasguzz

        '''low gas price tx watch list'''
        recent = self.end_block - 250
        lowprice = self.tx_df.loc[(self.tx_df['minedGasPrice'] < 1000) & (self.tx_df['block_posted'] < recent), ['minedGasPrice', 'block_posted', 'mined', 'block_mined']]
        lowprice = lowprice.sort_values(['minedGasPrice'], ascending = True).reset_index()
        self.lowprice = lowprice
    
        '''average block time'''
        blockinterval = self.block_df[['block_number', 'time_mined']].diff()
        blockinterval.loc[blockinterval['block_number'] > 1, 'time_mined'] = np.nan
        blockinterval.loc[blockinterval['time_mined']< 0, 'time_mined'] = np.nan
        self.avg_timemined = blockinterval['time_mined'].mean()
    
        '''median wait time by gas price for bar graph'''
        price_wait = self.tx_df.loc[:, ['minedGasPrice', 'delay']]
        price_wait.loc[price_wait['minedGasPrice']>=40, 'minedGasPrice'] = 40
        price_wait = price_wait.loc[(price_wait['minedGasPrice']<=10) | (price_wait['minedGasPrice']==20) | (price_wait['minedGasPrice'] == 40), ['minedGasPrice', 'delay']]
        price_wait.loc[price_wait['minedGasPrice']<1, 'minedGasPrice'] = 0
        price_wait = price_wait.groupby('minedGasPrice').median()
        price_wait.reset_index(inplace=True)
        price_wait['delay'] = price_wait['delay']*self.avg_timemined/float(60)
        self.price_wait = price_wait