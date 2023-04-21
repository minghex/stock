import json
import akshare as ak
import pandas as pd
import numpy as np
from .base import BaseHandler
import handlers.option as op 

class PCRHandler(BaseHandler):
    def get(self):
        df = ak.macro_china_shrzgm()
        df = df[['月份','社会融资规模增量']].copy()
        df.rename(columns={'月份':'date', '社会融资规模增量':'volume'},inplace=True)
        df_json = df.to_json()

        print(df_json)
        

        my_data = {'code': 0, 'data':df_json}
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(my_data))


def ret_option_df(
        data : pd.DataFrame,
        name : str,
) -> pd.DataFrame:
    #获取数据源
    df = pd.DataFrame()
    for v in data:
        daily = ak.option_cffex_hs300_daily_sina(symbol=v)
        tmpDF = daily[['date','volume']].copy()
        tmpDF.rename(columns={'date': 'date', 'volume': name},inplace=True)
        df = pd.concat([df,tmpDF],axis=0)         
    #进行数据清洗
    df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')
    df = pd.pivot_table(data=df,index='date',values=name,aggfunc=np.sum ,fill_value=0)
    # print(df.info())
    df.sort_values(by='date',inplace=True)
    return df    

def OPTION_HS300_LIST_HANDLER() -> pd.DataFrame:
    # 沪深300指数期权列表
    df1 = op.option_cffex_hs300_list_sina()['沪深300指数']
    # 沪深300主力期权
    df2 = ak.option_cffex_hs300_spot_sina(symbol=df1[0])
    #call_option
    c_df = ret_option_df(df2['看涨合约-标识'],"c_volume")
    #pull_option
    p_df = ret_option_df(df2['看跌合约-标识'],'p_volume')
    #pcr_volume
    df = pd.merge(p_df,c_df,how='left',on='date')
    df['pcr'] = df['p_volume'] / df['c_volume']
    return df['pcr'].copy()

def ret_zz1000_option_df(
        data : pd.DataFrame,
        name : str,
) -> pd.DataFrame:
    #获取数据源
    df = pd.DataFrame()
    for v in data:
        daily = ak.option_cffex_zz1000_daily_sina(symbol=v)
        tmpDF = daily[['date','volume']].copy()
        tmpDF.rename(columns={'date': 'date', 'volume': name},inplace=True)
        df = pd.concat([df,tmpDF],axis=0)         
    #进行数据清洗
    df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')
    df = pd.pivot_table(data=df,index='date',values=name,aggfunc=np.sum ,fill_value=0)
    df.sort_values(by='date',inplace=True)
    return df    

def OPTION_ZZ1000_LIST_HANDLER() -> pd.DataFrame:
    # 中证1000指数期权列表
    df1 = op.option_cffex_zz1000_list_sina()['中证1000指数']
    # 沪深300主力期权
    df2 = ak.option_cffex_zz1000_spot_sina(symbol=df1[0])
    #call_option
    c_df = ret_zz1000_option_df(df2['看涨合约-标识'],"c_volume")
    #pull_option
    p_df = ret_zz1000_option_df(df2['看跌合约-标识'],'p_volume')
    #pcr_volume
    df = pd.merge(p_df,c_df,how='left',on='date')
    df['pcr'] = df['p_volume'] / df['c_volume']
    return df['pcr'].copy()
    
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
    df.sort_values(by='date',inplace=True)
    return df    

def OPTION_SZ50_LIST_HANDLER() -> pd.DataFrame:
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
    return df['pcr'].copy()

class OptionPCRHandler(BaseHandler):
    def get(self):
        df = OPTION_HS300_LIST_HANDLER()
        self.write_success_response(df.to_json())

    def post(self):
        # option_type = self.request_data.get('option_type',0)
        option_type = 0
        df = self.option_switch(option_type) 
        self.write_success_response(df.to_json())

    def option_switch(self, case, *args) -> pd.DataFrame:
        cases = {
            0: OPTION_SZ50_LIST_HANDLER,
            1: OPTION_HS300_LIST_HANDLER,
            2: OPTION_ZZ1000_LIST_HANDLER,
        }
        func = cases.get(case, OPTION_SZ50_LIST_HANDLER)
        return func(*args)

