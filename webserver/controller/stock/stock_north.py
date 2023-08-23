import akshare as ak
import pandas as pd
from controller.handler import * 

def gen_stock_net_flow() -> str:
    return ak.stock_hsgt_north_net_flow_in_em(symbol='北上').to_json()

def gen_stock_sz_index() -> str:
    return ak.stock_zh_index_daily(symbol="sh000001").to_json()

class stock_north_net_flow(BaseHandler):
    async def get(self):
        doc_net_flow = await self.get_data('stock_north_netflow', gen_stock_net_flow)
        df_net_flow = pd.DataFrame(json.loads(doc_net_flow))
        
        doc_sz_index = await self.get_data('stock_sz000001_index', gen_stock_sz_index)
        df_sz_index = pd.DataFrame(json.loads(doc_sz_index))
        df_sz_index['date'] = pd.to_datetime(df_sz_index['date'], unit='ms').dt.strftime('%Y-%m-%d')
        
        merged_df = pd.merge(df_net_flow, df_sz_index, on='date')
        select_columns = ['date', 'value', 'close']
        self.write_success_response(merged_df[select_columns].to_json())
