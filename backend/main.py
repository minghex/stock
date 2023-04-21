#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import asyncio

import tornado.web
import akshare as ak
import pandas as pd
import xlsxwriter as xw
import matplotlib.pyplot as plt
import numpy as np
import option as op

STOCK_NUMBER = 0

def testHandler():
    # writer = pd.ExcelWriter('pmi.xlsx', engine = 'xlsxwriter')
    df1 = ak.macro_china_pmi_yearly()
    # df1.tail(10).to_excel(writer, sheet_name='Sheet1')
    df2 = ak.rate_interbank()
    # df2.tail(10).to_excel(writer, sheet_name='Sheet2')
    # writer.close()




class MainHandler(tornado.web.RequestHandler):
    def get(self):
        df1 = ak.macro_china_pmi_yearly()
        (max_row,) = df1.shape

        sheetname = 'Sheet1'
        writer = pd.ExcelWriter('pmi.xlsx', engine = 'xlsxwriter')
        df1.tail(max_row).to_excel(writer, sheet_name=sheetname)

        workbook = writer.book
        worksheet = writer.sheets[sheetname]
        chart = workbook.add_chart({'type': 'line'})
        chart.add_series({
            'categories': [sheetname, 1, 0, max_row, 0],
            'values': [sheetname, 1, 1, max_row, 1],
            'name': 'PMI_INDEX',
        })
        chart.set_title({'name': 'PMI'})
        worksheet.insert_chart(1, 10, chart)
        writer.close()

def SHIBOR_BOND_HANDLER():
    sheetname = 'Sheet2'
    df1 = ak.rate_interbank(indicator="1年")
    df1.columns = [
        "date",
        "ratio",
        "price",
    ]
    df1.set_index('date', inplace=True)
    df2 = ak.stock_a_pe_and_pb(symbol="000300.SH")
    df2.set_index('date', inplace=True)
    df3 = pd.merge(df1, df2, left_index=True, right_index=True, how='inner')

    writer = pd.ExcelWriter('sample.xlsx', engine = 'xlsxwriter')
    (max_row, max_col) = df3.shape
    df3.filter(items=['date', 'ratio', 'close']).tail(1000).to_excel(writer, sheet_name=sheetname)
    workbook = writer.book
    worksheet = writer.sheets[sheetname]
    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': [sheetname, 1, 0, max_row, 0],
        'values': [sheetname, 1, 1, max_row, 1],
        'name': ' 一年期同业拆借利率',
    })

    chart.add_series({
        'categories': [sheetname, 1, 0, max_row, 0],
        'values': [sheetname, 1, 2, max_row, 2],
        'name': '沪深300指数',
        'y2_axis': True,
    })
    worksheet.insert_chart(1, 10, chart)
    writer.close()

def PE_BOND_HANDLER():
    df1 = ak.stock_a_pe_and_pb(symbol="000300.SH")
    df1['dividend_rate'] = df1['addTtmPe'].apply(lambda x: (100/x))
    df1.set_index('date', inplace=True)
    df2 = ak.bond_zh_us_rate()
    df2.set_index('日期', inplace=True)
    df3 = pd.merge(df1, df2, left_index=True, right_index=True, how='inner')
    df3["pe_bond_ratio"] = (
        (df3["dividend_rate"] - df3["中国国债收益率10年"]) / 100
    )
    df3['20day_rolling_avg'] = df3['pe_bond_ratio'].rolling(360).mean()
    df3['20day_rolling_avg_std'] = df3['pe_bond_ratio'].rolling(360).std()
    df3['20day_rolling_avg_std_add_1'] =  df3['20day_rolling_avg'] + df3['20day_rolling_avg_std']
    df3['20day_rolling_avg_std_sub_1'] =  df3['20day_rolling_avg'] - df3['20day_rolling_avg_std']

    df4 = ak.stock_a_all_pb()
    df4.set_index('date', inplace=True)
    df4["sh_index_xmh"] =  df3["close"]
    df5 = pd.merge(df3, df4, left_index=True, right_index=True, how='inner')

    sheetname = 'Sheet1'
    writer = pd.ExcelWriter('sample.xlsx', engine = 'xlsxwriter')
    (max_row, max_col) = df5.shape
    df5.filter(items=['date' ,'pe_bond_ratio', 'sh_index_xmh']).tail(max_row).to_excel(writer, sheet_name=sheetname)
    workbook = writer.book
    worksheet = writer.sheets[sheetname]
    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': [sheetname, 1, 0, max_row, 0],
        'values': [sheetname, 1, 1, max_row, 1],
        'name': '股债利差',
    })
    chart.add_series({
        'categories': [sheetname, 1, 0, max_row, 0],
        'values': [sheetname, 1, 2, max_row, 2],
        'name': '沪深300指数',
        'y2_axis': True,
    })
    chart.set_title({'name': 'PE_BOND_RATIO'})
    worksheet.insert_chart(1, 10, chart)
    writer.close()


def create_xlsx_dataframe(
        dataframe: pd.DataFrame,
        chartname: str = 'hello',
        sheetname: str = 'sheet1',
        indexSymbol: str = 'sh',
        indexName: str = '上证指数',
        outfile: str = 'sample.xlsx',
        **kwargs,
    ):
    '''
        create xlsx with dataframe
    '''

    itemList = []
    for key in kwargs:
        itemList.append(key)

    #添加指数
    index_df = ak.stock_a_pe_and_pb(symbol=indexSymbol)
    index_df = index_df[['date','close']].copy()
    index_df.set_index('date', inplace=True)
    merge_df = pd.merge(dataframe, index_df, left_index=True, right_index=True, how='inner')
    itemList.append('close')

    writer = pd.ExcelWriter(outfile, engine = 'xlsxwriter')
    (max_row, max_col) = merge_df.shape
    merge_df.filter(items=itemList).tail(max_row).to_excel(writer, sheet_name=sheetname, index=True)
   
    workbook = writer.book
    worksheet = writer.sheets[sheetname]
    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': [sheetname, 1, 0, max_row, 0],
        'values': [sheetname, 1, 1, max_row, 1],
        'name': chartname,
    })

    chart.add_series({
        'categories': [sheetname, 1, 0, max_row, 0],
        'values': [sheetname, 1, max_col, max_row, max_col],
        'name': indexName,
        'y2_axis': True,
    })
    worksheet.insert_chart(1, max_col+1, chart)
    writer.close()

def Macro_China_Shrzgm_Handler():
    df = ak.macro_china_shrzgm()
    df = df[['月份','社会融资规模增量']].copy()
    df.rename(columns={'月份':'date', '社会融资规模增量':'volume'},inplace=True)
    print(df.info())
    print(df.head())
    df['date'] = pd.to_datetime(df['date'],format='%Y%m')
    # # print(df.info())
    # # print(df.head())
    # create_xlsx_dataframe(df,chartname='社会融资规模增量',outfile='macro.xlsx',**{'月份': '日期', '社会融资规模增量': '人民币贷款'})


def todo1Handler():
    # 社会零售 储蓄率 
    macro_china_consumer_goods_retail_df = ak.macro_china_consumer_goods_retail()
    print(macro_china_consumer_goods_retail_df)

def STOCK_RANk_HANDLER():
    df_60 = ak.stock_rank_xstp_ths(symbol="60日均线")
    print("60MA: %.2f" % (len(df_60) / STOCK_NUMBER))
    df_20 = ak.stock_rank_xstp_ths(symbol="20日均线")
    print("20MA: %.2f" % (len(df_20) / STOCK_NUMBER))

def MARKET_BASE_INFO_HANDLER() -> int:
    df1 = ak.stock_sse_summary()
    df2 = ak.stock_szse_summary(date="20221220")
    return int(df1.iat[4, 1]) + int(df2.iat[0, 1])


def OPTION_HS300_LIST_HANDLER():
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
    create_xlsx_dataframe(df,'沪深300指数期权持仓量PCR',outfile='hs300.xlsx',**{'date': 'date', 'pcr': 'pcr', 'p_volume':'p_volume', 'c_volume':'c_volume'})
    return

def BOND_HANDLER():
    bond_zh_us_rate_df = ak.bond_zh_us_rate()
    bond_ten_y = bond_zh_us_rate_df[['日期','中国国债收益率2年']].copy()
    bond_ten_y.rename(columns={'日期': 'date'},inplace=True)
    bond_ten_y['date'] = pd.to_datetime(bond_ten_y['date'],format='%Y-%m-%d')
    bond_ten_y.set_index('date',inplace=True)

    pmi_df = ak.macro_china_pmi_yearly()

    merge_df = pd.merge(pmi_df,bond_ten_y,how='inner',left_index=True, right_index=True)
    outfile='bond.xlsx'
    sheetname='bond'
    writer = pd.ExcelWriter(outfile, engine = 'xlsxwriter')
    (max_row, max_col) = merge_df.shape
    merge_df.tail(max_row).to_excel(writer, sheet_name=sheetname, index=True)
   
    workbook = writer.book
    worksheet = writer.sheets[sheetname]
    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': [sheetname, 1, 0, max_row, 0],
        'values': [sheetname, 1, 1, max_row, 1],
        'name': 'PMI',
    })

    chart.add_series({
        'categories': [sheetname, 1, 0, max_row, 0],
        'values': [sheetname, 1, max_col, max_row, max_col],
        'name': '2年期国债收益率',
        'y2_axis': True,
    })
    worksheet.insert_chart(1, max_col+1, chart)
    writer.close()

def OPTION_TEST():
    OPTION_ZZ1000_LIST_HANDLER()
    OPTION_HS300_LIST_HANDLER()
    OPTION_SZ50_LIST_HANDLER()

class Handler(tornado.web.RequestHandler):
    def get(self):
        self.write('sss')

async def main():
    application = tornado.web.Application({
        (r"/", TestHandler)
    })
    application.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())