#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import akshare as ak
import pandas as pd
from controller.handler import * 

#(指数级别)收盘价高于5/20/60均线的股票的数量占比（0%~100%）
#持续缩量且向下突破20日均线的股票
class stock_csxl_xxtp_handler(BaseHandler):
    async def get(self):
        # 持续缩量
        stock_rank_cxsl_ths_df = await self.get_stock_cxsl_data()
        # 向下突破
        stock_rank_xxtp_ths_df = await self.get_stock_xxtp_data()
        # 满足持续缩量 向下突破
        merge_df = pd.merge(stock_rank_cxsl_ths_df, stock_rank_xxtp_ths_df, on=['股票代码','股票简称','最新价'])
        print(len(merge_df))
        print(merge_df)
        select_columns = ['股票代码', '股票简称', '最新价', '换手率', '缩量天数', '所属行业']
        self.write_success_response(merge_df[select_columns].to_json())
    
    async def get_stock_cxsl_data(self) -> pd.DataFrame:
        key = "stock_cxsl"
        doc = await self.get_data_from_database(key)
        if not doc:
            doc = self.gen_stock_cxsl_data()
            await self.save_data_to_db(key,doc)

        json_data = json.loads(doc) 
        return pd.DataFrame(json_data)
    
    def gen_stock_cxsl_data(self) -> str:
        return ak.stock_rank_cxsl_ths().to_json() 


    async def get_stock_xxtp_data(self) -> pd.DataFrame:
        key = "stock_xxtp"
        doc = await self.get_data_from_database(key)
        if not doc:
            doc = self.gen_stock_xxtp_data()
            await self.save_data_to_db(key,doc)

        json_data = json.loads(doc) 
        return pd.DataFrame(json_data)
    
    def gen_stock_xxtp_data(self) -> str:
        return ak.stock_rank_xxtp_ths(symbol="20日均线").to_json() 
