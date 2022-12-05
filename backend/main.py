#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import asyncio

import tornado.web
import akshare as ak
import pandas as pd
import xlsxwriter as xw

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        df = ak.bond_zh_us_rate()
        writer = pd.ExcelWriter('sample.xlsx', engine = 'xlsxwriter')
        df.filter(items=['日期' , '中国国债收益率10年']).tail(200).to_excel(writer, sheet_name='Sheet1')
        # Get the xlsxwriter objects from the dataframe writer object.
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        # Create a chart object.
        chart = workbook.add_chart({'type': 'line'})
        # Get the dimensions of the dataframe.
        (max_row, max_col) = df.shape
        # Configure the series of the chart from the dataframe data.
        chart.add_series({
            #[sheetname, first_row, first_col, last_row, last_col]
            'categories': ['Sheet1', 1, 1, max_row, 1],
            'values': ['Sheet1', 1, 2, max_row, 2],
            'name': '=Sheet1!$C$1',
        })
        chart.set_y_axis({ 'name': '十年国债收益率'})


        rate_interbank_df = ak.rate_interbank(market="上海银行同业拆借市场", symbol="Shibor人民币", indicator="隔夜")
        rate_interbank_df.filter(items=['报告日' , '利率']).tail(200).to_excel(writer, sheet_name='Sheet1', startcol=4)
        chart2 = workbook.add_chart({'type': 'line'})
        (max_row, max_col) = rate_interbank_df.shape
        chart2.add_series({
            'categories': ['Sheet1', 1, 5, max_row, 5],
            'values': ['Sheet1', 1, 6, max_row, 6],
            'name': '同业拆借隔夜利率',
            'y2_axis': True,
        })
        chart2.set_y2_axis({ 'name': '隔夜利率'})
        chart.combine(chart2)
        worksheet.insert_chart(1, 7, chart)
        writer.close()

class InfHandler(tornado.web.RequestHandler):
    def get(self):
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


        # chart.add_series({
        #     'categories': [sheetname, 1, 0, max_row, 0],
        #     'values': [sheetname, 1, 2, max_row, 2],
        #     'name': 'ma20',
        # })

        # chart.add_series({
        #     'categories': [sheetname, 1, 0, max_row, 0],
        #     'values': [sheetname, 1, 4, max_row, 4],
        #     'name': 'std+1',
        # })

        # chart.add_series({
        #     'categories': [sheetname, 1, 0, max_row, 0],
        #     'values': [sheetname, 1, 5, max_row, 5],
        #     'name': 'std-1',
        # })
        worksheet.insert_chart(1, 10, chart)
        writer.close()



class PE_BOND_RATIO_Handler(tornado.web.RequestHandler):
    def get(self):
        wb = xw.Workbook()
        chart = wb.add_chart()

def testHandler():
        df4 = ak.stock_a_all_pb()
        print(df4)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/inf", InfHandler),
        (r"/1",PE_BOND_RATIO_Handler),
    ])

async def main():
    app = make_app()
    print("run main")
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())