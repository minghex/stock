#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import akshare as ak
import pandas as pd
from controller.handler import * 

class stock_pe_bond_Handler(BaseHandler):
    async def get(self):
        key = "stock_bond"
        doc = await self.get_data_from_database(key)
        if not doc:
            doc = self.gen_stock_pe_data()
            await self.save_data_to_db(key,doc)
        
        self.write_success_response(doc)


    # 构建数据(逻辑上每日只调用一次)
    def gen_stock_pe_data(self) -> str:
        df1 = ak.stock_index_pe_lg()
        df1['dividend_rate'] = df1['滚动市盈率'].apply(lambda x: (100/x))
        df1.set_index('日期', inplace=True)
        df2 = ak.bond_zh_us_rate()
        df2.set_index('日期', inplace=True)
        df3 = pd.merge(df1, df2, left_index=True, right_index=True, how='inner')
        df3["pe_bond_ratio"] = (
            (df3["dividend_rate"] - df3["中国国债收益率10年"]) / 100
        )
        df4 = ak.stock_a_all_pb()
        df4.set_index('date', inplace=True)
        df4["sh_index_xmh"] =  df3["指数"]
        res = pd.merge(df3, df4, left_index=True, right_index=True, how='inner')
        return res.to_json()
