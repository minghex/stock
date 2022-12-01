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
        # Insert the chart into the worksheet.
        # worksheet.insert_chart(1, 4, chart)

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

#todo 平均曲线 +1/-1标准差曲线
class InfHandler(tornado.web.RequestHandler):
    def get(self):
        df1 = ak.stock_a_pe_and_pb(symbol="000300.SH")
        df1['dividend_rate'] = df1['addTtmPe'].apply(lambda x: (100/x))
        df1.set_index('date', inplace=True)
        df2 = ak.bond_zh_us_rate()
        df2.set_index('日期', inplace=True)
        df3 = pd.merge(df1, df2, left_index=True, right_index=True, how='inner')
        df3["pe_bond_ratio"] = (
            df3["dividend_rate"] - df3["中国国债收益率10年"]
        )

        sheetname = 'Sheet1'
        writer = pd.ExcelWriter('board.xlsx', engine = 'xlsxwriter')
        (max_row, max_col) = df3.shape
        df3.filter(items=['date' ,'dividend_rate', '中国国债收益率10年', 'pe_bond_ratio']).tail(max_row).to_excel(writer, sheet_name=sheetname)
        workbook = writer.book
        worksheet = writer.sheets[sheetname]
        chart = workbook.add_chart({'type': 'line'})
        chart.add_series({
            'categories': [sheetname, 1, 0, max_row, 0],
            'values': [sheetname, 1, 3, max_row, 3],
            'name': '股债利差',
        })
        worksheet.insert_chart(1, 5, chart)
        writer.close()



class PE_BOND_RATIO_Handler(tornado.web.RequestHandler):
    def get(self):
        sheetname = 'PE_BOND_RATIO'
        writer = pd.ExcelWriter('sample.xlsx', engine = 'xlsxwriter')
        #PE
        pe_df = ak.stock_a_pe_and_pb(symbol="000300.SH")
        pe_df['dividend_rate'] = pe_df['addTtmPe'].apply(lambda x: (1/x)*100)
        (max_row, max_col) = pe_df.shape
        pe_df.filter(items=['date' , 'dividend_rate']).tail(max_row).to_excel(writer, sheet_name=sheetname)
        workbook  = writer.book
        worksheet = writer.sheets[sheetname]
        chart = workbook.add_chart({'type': 'line'})
        chart.add_series({
            'categories': [sheetname, 1, 1, max_row, 1],
            'values': [sheetname, 1, 2, max_row, 2],
            'name': '沪深300股息率',
        })
        chart.set_y_axis({ 'name': '沪深300股息率'})

        #bond
        startCol = 4
        df = ak.bond_zh_us_rate()
        # df['bond_ten'] = df['中国国债收益率10年'].apply(lambda x: x if x > 0 else 0)
        df.filter(items=['日期' , '中国国债收益率10年']).tail(max_row).to_excel(writer, sheet_name=sheetname, startcol=startCol)
        chart2 = workbook.add_chart({'type': 'line'})
        chart2.add_series({
            'categories': [sheetname, 1, startCol+1, max_row, startCol+1],
            'values': [sheetname, 1, startCol+2, max_row, startCol+2],
            'name': [sheetname, 0, startCol+2],
            'y2_axis': True,
        })
        chart2.set_y2_axis({ 'name': '十年国债收益率'})
        chart.combine(chart2)
        worksheet.insert_chart(1, startCol+3, chart)
        

        # for row in range (1, max_row-1):
        #     row_dict = worksheet.table.get(row, None)
        #     col_entry1 = row_dict.get(2, None)
        #     col_entry2 = row_dict.get(6, None)
        #     val = col_entry1.number-col_entry2.number
        #     worksheet.write(row, 3, val)

        # chart3 = workbook.add_chart({'type': 'line'})
        # chart3.add_series({
        #     'categories': [sheetname, 1, 1, max_row, 1],
        #     'values': [sheetname, 1, 3, max_row, 3],
        #     'name': '股债利差',
        # })
        # worksheet.insert_chart(20, startCol+3, chart3)

        writer.close()   

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