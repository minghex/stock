#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import asyncio

import tornado.web
import akshare as ak
import pandas as pd
import xlsxwriter as xw

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print('')


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
    writer = pd.ExcelWriter('board.xlsx', engine = 'xlsxwriter')
    (max_row, max_col) = df5.shape
    df5.filter(items=['date' ,'pe_bond_ratio', 'sh_index_xmh']).tail(max_row).to_excel(writer, sheet_name=sheetname)
    workbook = writer.book
    worksheet = writer.sheets[sheetname]
    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': [sheetname, 1, 0, max_row, 0],
        'values': [sheetname, 1, 1, max_row, 1],
        'name': 'PE_BOND_RATIO',
    })
    chart.add_series({
        'categories': [sheetname, 1, 0, max_row, 0],
        'values': [sheetname, 1, 2, max_row, 2],
        'name': 'SH_INDEX',
        'y2_axis': True,
    })
    chart.set_title({'name': 'PE_BOND_RATIO'})
    worksheet.insert_chart(1, 10, chart)
    writer.close()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(8888)
    print("service ready")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())