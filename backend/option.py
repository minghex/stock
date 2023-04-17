#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import json
import datetime
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup
import pandas as pd

#沪深300主力期权
def option_cffex_hs300_list_sina() -> Dict[str, List[str]]:
    url = "https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    symbol = soup.find(attrs={"id": "option_symbol"}).find_all("li")[1].text
    temp_attr = soup.find(attrs={"id": "option_suffix"}).find_all("li")
    contract = [item.text for item in temp_attr]
    return {symbol: contract}


#中证1000主力期权
def option_cffex_zz1000_list_sina() -> Dict[str, List[str]]:
    url = "https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/mo/cffex"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    symbol = soup.find(attrs={"id": "option_symbol"}).find_all("li")[2].text
    temp_attr = soup.find(attrs={"id": "option_suffix"}).find_all("li")
    contract = [item.text for item in temp_attr]
    return {symbol: contract}


#上证50主力期权
def option_cffex_sz50_list_sina() -> Dict[str, List[str]]:
    url = "https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    symbol = soup.find(attrs={"id": "option_symbol"}).find_all("li")[0].text
    temp_attr = soup.find(attrs={"id": "option_suffix"}).find_all("li")
    contract = [item.text for item in temp_attr]
    return {symbol: contract}


def option_cffex_sz50_spot_sina(symbol: str = "mo2208") -> pd.DataFrame:
    url = "https://stock.finance.sina.com.cn/futures/api/openapi.php/OptionService.getOptionData"
    params = {
        "type": "futures",
        "product": "ho",
        "exchange": "cffex",
        "pinzhong": symbol,
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(
        data_text[data_text.find("{") : data_text.rfind("}") + 1]
    )
    option_call_df = pd.DataFrame(
        data_json["result"]["data"]["up"],
        columns=[
            "看涨合约-买量",
            "看涨合约-买价",
            "看涨合约-最新价",
            "看涨合约-卖价",
            "看涨合约-卖量",
            "看涨合约-持仓量",
            "看涨合约-涨跌",
            "行权价",
            "看涨合约-标识",
        ],
    )
    option_put_df = pd.DataFrame(
        data_json["result"]["data"]["down"],
        columns=[
            "看跌合约-买量",
            "看跌合约-买价",
            "看跌合约-最新价",
            "看跌合约-卖价",
            "看跌合约-卖量",
            "看跌合约-持仓量",
            "看跌合约-涨跌",
            "看跌合约-标识",
        ],
    )
    data_df = pd.concat([option_call_df, option_put_df], axis=1)
    data_df["看涨合约-买量"] = pd.to_numeric(data_df["看涨合约-买量"], errors="coerce")
    data_df["看涨合约-买价"] = pd.to_numeric(data_df["看涨合约-买价"], errors="coerce")
    data_df["看涨合约-最新价"] = pd.to_numeric(data_df["看涨合约-最新价"], errors="coerce")
    data_df["看涨合约-卖价"] = pd.to_numeric(data_df["看涨合约-卖价"], errors="coerce")
    data_df["看涨合约-卖量"] = pd.to_numeric(data_df["看涨合约-卖量"], errors="coerce")
    data_df["看涨合约-持仓量"] = pd.to_numeric(data_df["看涨合约-持仓量"], errors="coerce")
    data_df["看涨合约-涨跌"] = pd.to_numeric(data_df["看涨合约-涨跌"], errors="coerce")
    data_df["行权价"] = pd.to_numeric(data_df["行权价"], errors="coerce")
    data_df["看跌合约-买量"] = pd.to_numeric(data_df["看跌合约-买量"], errors="coerce")
    data_df["看跌合约-买价"] = pd.to_numeric(data_df["看跌合约-买价"], errors="coerce")
    data_df["看跌合约-最新价"] = pd.to_numeric(data_df["看跌合约-最新价"], errors="coerce")
    data_df["看跌合约-卖价"] = pd.to_numeric(data_df["看跌合约-卖价"], errors="coerce")
    data_df["看跌合约-卖量"] = pd.to_numeric(data_df["看跌合约-卖量"], errors="coerce")
    data_df["看跌合约-持仓量"] = pd.to_numeric(data_df["看跌合约-持仓量"], errors="coerce")
    data_df["看跌合约-涨跌"] = pd.to_numeric(data_df["看跌合约-涨跌"], errors="coerce")
    return data_df

def option_cffex_sz50_daily_sina(
    symbol: str = "mo2208P6200",
) -> pd.DataFrame:
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    url = f"https://stock.finance.sina.com.cn/futures/api/jsonp.php/var%20_{symbol}{year}_{month}_{day}=/FutureOptionAllService.getOptionDayline"
    params = {"symbol": symbol}
    r = requests.get(url, params=params)
    data_text = r.text
    data_df = pd.DataFrame(
        eval(data_text[data_text.find("[") : data_text.rfind("]") + 1])
    )
    data_df.columns = ["open", "high", "low", "close", "volume", "date"]
    data_df = data_df[
        [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
    ]
    data_df["date"] = pd.to_datetime(data_df["date"]).dt.date
    data_df["open"] = pd.to_numeric(data_df["open"])
    data_df["high"] = pd.to_numeric(data_df["high"])
    data_df["low"] = pd.to_numeric(data_df["low"])
    data_df["close"] = pd.to_numeric(data_df["close"])
    data_df["volume"] = pd.to_numeric(data_df["volume"])
    return data_df
