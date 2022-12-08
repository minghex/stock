#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import akshare as ak
import numpy as np
import pandas as pd
import backtrader as bd


HundredMillion = 100000000
WeightRatio = 0.35
EnhancedRatio = 0.8

def writer_to_excel():
    stock_list = ak.index_stock_cons_weight_csindex(symbol='000300')
    (max_row,max_col) = stock_list.shape
    writer = pd.ExcelWriter('stock.xlsx', engine = 'xlsxwriter')
    stock_list.tail(max_row).to_excel(writer, sheet_name='Sheet1')
    writer.close()

def enhanced_300_index_trade():
    stock_list = ak.index_stock_cons_weight_csindex(symbol='000300')
    stock_symbol = []
    stock_weight = []
    for _ , row in stock_list.iterrows():
        if row['权重'] > WeightRatio:
            stock_symbol.append(row['成分券代码'])
            stock_weight.append(row['权重'])

    df = pd.DataFrame([stock_symbol,stock_weight]).T
    df.columns = ['symbol', 'weight']
    df2 =  df.sort_values(by=['weight'], ascending=False)
    for _ , row in df2.iterrows():
        stock_hist_df = ak.stock_zh_a_hist(symbol=row['symbol'], period="daily", start_date="20221105", end_date='20221205', adjust="")
        if all(v > 0 for v in np.diff(stock_hist_df.tail(5)['收盘'])):
            # 连续上涨 强势
            buy_percent = row['weight'] * (EnhancedRatio + 0.2)
            print('强', row['symbol'], '以市价单调多仓至仓位:', buy_percent)
        else:
            buy_percent = row['weight'] * (EnhancedRatio - 0.2)
            print('弱', row['symbol'], '以市价单调多仓至仓位:', buy_percent)


def wind_a_total_value():
    #沪深两市总市值z
    stock_sse_summary_df = ak.stock_sse_summary()
    stock_szse_summary_df = ak.stock_szse_summary(date="20221205")
    return np.float64(stock_sse_summary_df['股票'].iloc[5]) + stock_szse_summary_df.iloc[0]['流通市值']/HundredMillion

def enhanced_windA_index_trade():
    market_value = wind_a_total_value()
    stock_list = ak.stock_zh_a_spot_em()

    stock_symbol = []
    stock_weight = []
    for _ , row in stock_list.iterrows():
        weight = row['流通市值'] / HundredMillion / market_value
        if weight > WeightRatio:
            stock_symbol.append(row['代码'])
            stock_weight.append(weight)

    df = pd.DataFrame([stock_symbol,stock_weight]).T
    df.columns = ['symbol', 'weight']
    df2 =  df.sort_values(by=['weight'], ascending=False)
    for _ , row in df2.iterrows():
        stock_hist_df = ak.stock_zh_a_hist(symbol=row['symbol'], period="daily", start_date="20221105", end_date='20221205', adjust="")
        if all(v > 0 for v in np.diff(stock_hist_df.tail(5)['收盘'])):
            # 连续上涨 强势
            buy_percent = row['weight'] * (EnhancedRatio + 0.2)
            print('强', row['symbol'], '以市价单调多仓至仓位:', buy_percent)
        else:
            buy_percent = row['weight'] * (EnhancedRatio - 0.2)
            print('弱', row['symbol'], '以市价单调多仓至仓位:', buy_percent)


enhanced_300_index_trade()
# writer_to_excel()

#create a Cerebro Engine
cerebro = bd.Cerebro()
#inject the Strategy
cerebro.addstrategy()
#load and inject a Data Feed
cerebro.adddata()
#execute
cerebro.run()
#visual feedback use
cerebro.plot()