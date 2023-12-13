import akshare as ak
import pandas as pd
from controller.handler import * 
from controller.stock.stock_define import *
from datetime import datetime

def gen_stock_sz_index() -> str:
    return ak.stock_zh_index_daily(symbol="sh000001").to_json()

#北上净流入
def gen_stock_net_flow() -> str:
    return ak.stock_hsgt_north_net_flow_in_em(symbol='北上').to_json()

class stock_north_net_flow(BaseHandler):
    async def get(self):
        doc_net_flow = await self.get_data(stock_north_netflow, gen_stock_net_flow)
        df_net_flow = pd.DataFrame(json.loads(doc_net_flow))
        
        doc_sz_index = await self.get_data(stock_sz_index, gen_stock_sz_index)
        df_sz_index = pd.DataFrame(json.loads(doc_sz_index))
        df_sz_index['date'] = pd.to_datetime(df_sz_index['date'], unit='ms').dt.strftime('%Y-%m-%d')
        
        merged_df = pd.merge(df_net_flow, df_sz_index, on='date')
        select_columns = ['date', 'value', 'close']
        res = merged_df.tail(300).reset_index(drop=True)
        self.write_success_response(res[select_columns].to_json())

#股指期货结构 
def gen_stock_index_futures() -> str:
    # 格式化日期
    end_date = datetime.now().strftime("%Y%m%d")
    df = ak.futures_main_sina(symbol="IF0", end_date=end_date)
    return df.to_json() 

class stock_futures_index(BaseHandler):
    async def get(self):
        doc = await self.get_data(stock_index_futures, gen_stock_index_futures)
        df = pd.DataFrame(json.loads(doc))
        select_columns = ['日期', '收盘价']
        self.write_success_response(df[select_columns].to_json())
        #期货曲线定价都来到了contango结构（升水）远期价格高于现货价格,深度contango不做空，深度back不追多
        #右轴-期货收盘价(连续)
        #左轴-期货结算价(连一) - 期货结算价(连三)
