from matplotlib import pylab
import numpy as np
import pandas as pd
import DataAPI
import seaborn as sns
sns.set_style('white')

def getHistDayOptions(var, date):
    # 使用DataAPI.OptGet，拿到已退市和上市的所有期权的基本信息；
    # 同时使用DataAPI.MktOptdGet，拿到历史上某一天的期权成交信息；
    # 返回历史上指定日期交易的所有期权信息，包括：
    # optID  varSecID  contractType  strikePrice  expDate  tradeDate  closePrice turnoverValue
    # 以optID为index。
    dateStr = date.toISO().replace('-', '')
    optionsMkt = DataAPI.MktOptdGet(tradeDate = dateStr, field = [u"optID", "tradeDate", "closePrice", "turnoverValue"], pandas = "1")
    optionsMkt = optionsMkt.set_index(u"optID")
    optionsMkt.closePrice.name = u"price"

    optionsID = map(str, optionsMkt.index.values.tolist())
    fieldNeeded = ["optID", u"varSecID", u'contractType', u'strikePrice', u'expDate']
    optionsInfo = DataAPI.OptGet(optID=optionsID, contractStatus = [u"DE", u"L"], field=fieldNeeded, pandas="1")
    optionsInfo = optionsInfo.set_index(u"optID")
    options = concat([optionsInfo, optionsMkt], axis=1, join='inner').sort_index()
    return options[options.varSecID==var]

def calDayTurnoverValuePCR(optionVarSecID, date):
    # 计算历史每日的看跌看涨期权交易额的比值
    # PCR: put call ratio
    options = getHistDayOptions(optionVarSecID, date)
    call = options[options.contractType==u"CO"]
    put  = options[options.contractType==u"PO"]
    callTurnoverValue = call.turnoverValue.sum()
    putTurnoverValue = put.turnoverValue.sum()
    return 1.0 * putTurnoverValue / callTurnoverValue

def getHistPCR(beginDate, endDate):
    # 计算历史一段时间内的PCR指数并返回
    optionVarSecID = u"510050.XSHG"
    cal = Calendar('China.SSE')
    dates = cal.bizDatesList(beginDate, endDate)
    dates = map(Date.toDateTime, dates)
    histPCR = pd.DataFrame(0.0, index=dates, columns=['PCR'])
    histPCR.index.name = 'date'
    for date in histPCR.index:
        histPCR['PCR'][date] =  calDayTurnoverValuePCR(optionVarSecID, Date.fromDateTime(date))
    return histPCR

def getDayPCR(date):
    # 计算历史一段时间内的PCR指数并返回
    optionVarSecID = u"510050.XSHG"
    return calDayTurnoverValuePCR(optionVarSecID, date)

secID = '510050.XSHG'
begin = Date(2021, 2, 9)
end = Date(2021, 7, 30)

getHistPCR(begin, end).tail()