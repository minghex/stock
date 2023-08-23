import akshare as ak
import pandas as pd
import numpy as np
import controller.option.option_data as op 
from controller.handler import * 

# 数据缓存
option_pcr_cache_dict = {}

def ret_option_df(
        data : pd.DataFrame,
        name : str,
        debug = False,
) -> pd.DataFrame:
    #获取数据源
    df = pd.DataFrame()
    total_data = len(data)
    index = 0
    for v in data:
        index += 1
        if index == total_data:
            break
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
    p_df = ret_option_df(df2['看跌合约-标识'],'p_volume',True)
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

# 缓存失效时间戳
class option_pcr_handler(BaseHandler):
    async def get(self):
        doc = await self.get_option_pcr_data(0)
        self.write_success_response(doc)

    async def post(self):
        json_data = self.get_json_body()
        if not json_data:
            self.write_response(Response_ReqError_Code,"not found option type")
        else:
            option_type = json_data['option_type']
            doc =await self.get_option_pcr_data(option_type)
            self.write_success_response(doc)

    # 获取数据
    async def get_option_pcr_data(self, type) -> str:
        key = "option_pcr_" + str(type)
        doc = await self.get_data_from_database(key)
        if not doc:
            doc = self.gen_option_pcr_data(type).to_json()
            await self.save_data_to_db(key, doc)
        return doc

    # 构建数据(逻辑上每日只调用一次)
    def gen_option_pcr_data(self, case, *args) -> pd.DataFrame:
        cases = {
            0: OPTION_HS300_LIST_HANDLER,
            1: OPTION_ZZ1000_LIST_HANDLER,
            2: OPTION_SZ50_LIST_HANDLER,
        }
        func = cases.get(case, OPTION_HS300_LIST_HANDLER)
        return func(*args)
