import tornado.web
import akshare as ak
import pandas as pd
import xlsxwriter as xw
import matplotlib.pyplot as plt
import numpy as np
import backend.option as op

def ret_sz50_option_df(
        data : pd.DataFrame,
        name : str,
) -> pd.DataFrame:
    #获取数据源
    df = pd.DataFrame()
    for v in data:
        daily = op.option_cffex_sz50_daily_sina(symbol=v)
        tmpDF = daily[['date','volume']].copy()
        tmpDF.rename(columns={'date': 'date', 'volume': name},inplace=True)
        df = pd.concat([df,tmpDF],axis=0)         
    #进行数据清洗
    df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')
    df = pd.pivot_table(data=df,index='date',values=name,aggfunc=np.sum ,fill_value=0)
    # print(df.info())
    df.sort_values(by='date',inplace=True)
    return df    

def OPTION_SZ50_LIST_HANDLER():
    # sz50指数期权列表
    df1 = op.option_cffex_sz50_list_sina()['上证50指数']
    # sz50主力期权
    df2 = op.option_cffex_sz50_spot_sina(symbol=df1[0])
    #call_option
    c_df = ret_sz50_option_df(df2['看涨合约-标识'],"c_volume")
    #pull_option
    p_df = ret_sz50_option_df(df2['看跌合约-标识'],'p_volume')
    #pcr_volume
    df = pd.merge(p_df,c_df,how='left',on='date')
    df['pcr'] = df['p_volume'] / df['c_volume']
    return df