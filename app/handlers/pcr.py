import json
import akshare as ak
import pandas as pd
from .base import BaseHandler

class PCRHandler(BaseHandler):
    def get(self):
        df = ak.macro_china_shrzgm()
        df = df[['月份','社会融资规模增量']].copy()
        df.rename(columns={'月份':'date', '社会融资规模增量':'volume'},inplace=True)
        df_json = df.to_json()

        print(df_json)
        

        my_data = {'code': 0, 'data':df_json}
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(my_data))