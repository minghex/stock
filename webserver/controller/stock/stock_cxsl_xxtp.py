#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import akshare as ak
import pandas as pd
from controller.handler import * 


def gen_stock_xxtp_data() -> str:
    return ak.stock_rank_xxtp_ths(symbol="20日均线").to_json() 

def gen_stock_cxsl_data() -> str:
    return ak.stock_rank_cxsl_ths().to_json() 

#持续缩量且向下突破20日均线的股票
class stock_csxl_xxtp_handler(BaseHandler):
    async def get(self):
        # 持续缩量
        stock_rank_cxsl_ths_df = await self.get_stock_cxsl_data()
        # 向下突破
        stock_rank_xxtp_ths_df = await self.get_stock_xxtp_data()
        # 满足持续缩量 向下突破
        merge_df = pd.merge(stock_rank_cxsl_ths_df, stock_rank_xxtp_ths_df, on=['股票代码','股票简称','最新价'])
        
        select_columns = ['股票代码', '股票简称', '最新价', '换手率', '缩量天数', '所属行业']
        self.write_success_response(merge_df[select_columns].to_json())
    
    async def get_stock_cxsl_data(self) -> pd.DataFrame:
        doc = await self.get_data("stock_cxsl", gen_stock_cxsl_data)
        json_data = json.loads(doc) 
        return pd.DataFrame(json_data)
    

    async def get_stock_xxtp_data(self) -> pd.DataFrame:
        doc = await self.get_data("stock_xxtp", gen_stock_xxtp_data)
        json_data = json.loads(doc) 
        return pd.DataFrame(json_data)


class stock_xstp_handler(BaseHandler):
    def gen_stock_xstp_data(self) -> str:
        return ak.stock_rank_xstp_ths(symbol="60日均线")