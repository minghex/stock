#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd 

def combine_concat():
    df1 = pd.DataFrame({
        "date" : ["2023-02-25","2023-02-26","2023-02-24"],
        "volume":[100,50,100],
        "min":  [33,44,55]
    })
    df2 = pd.DataFrame({
        "date" : ["2023-02-25","2023-02-26","2023-02-24","2023-02-23"],
        "volume":[20,30,40,88],
        "max": [88,99,100,101],
    })
    df1['date'] = pd.to_datetime(df1["date"],format='%Y-%m-%d')
    df1.sort_values(by='date',inplace=True)
    df1.set_index('date',inplace=True)
    
    df2['date'] = pd.to_datetime(df2["date"],format='%Y-%m-%d')
    df2.sort_values(by='date',inplace=True)
    df2.set_index('date',inplace=True)
    #concat axis=0,按行追加;axis=1,按列追加.
    df3 = pd.concat([df1,df2],axis=0)
    print(df3)
    
    df4 = pd.concat([df1,df2],axis=1)
    print(df4)

# combine_concat()


def join_merge():
    df1 = pd.DataFrame({
        "date"  :   ["2023-02-25","2023-02-26","2023-02-24"],
        "max"   :   [100,50,100],
        "min"   :   [33,44,55]
    })
    df2 = pd.DataFrame({
        "date"  :   ["2023-02-25","2023-02-26","2023-02-24","2023-02-23"],
        "volume":   [20,30,40,88],
        "final":    [88,99,100,101],
    })
    #how-left交集数据;right并集数据
    #on-具有相同键名 对于两个表不同的键名链接使用left_one right_on
    df3 = pd.merge(df1,df2,how='right',on='date')
    print(df3)
    df4 = pd.merge(df1,df2,how='left',on='date')
    print(df4)

# join_merge()

def datetime():
    df = pd.DataFrame({
        "Date": [
            "2022-10-01",
            "2023-11-02",
        ],
    })
    print(df.describe())
    df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')
    print(df.describe())

# datetime()


def pivot():
    df = pd.DataFrame({
        "Attr1":["one","one","one","two","two","two"],
        "Attr2":['A','B','C','A','B','C'],
        "values":[1,2,3,4,5,6],
    })

    df2 = pd.pivot(df,index='Attr1', columns=['Attr2'], values='values')
    print(df2)

pivot()
# df = pd.DataFrame({
#     "Name": [
#         "A",
#         "B",
#         "C",
#     ],
#     "Age":[
#         10,
#         11,
#         12,
#     ],
# })

# # read_*    to_*
# sample = pd.read_excel("sample.xlsx")
# sample.to_excel("sample2.xlsx",sheet_name="pcr", index=False)

# method:
#    sample.info()  sample.head()   sample.tail()

# attr: 
#    sample.shape (return tuple (nrows,ncolumes))


# How do I select specific columns from a DataFrame
# sample[['colume1', 'colume2]]

# How do I filter specific rows from a DataFrame
# filter = sample[['colume1'] > 10]

#Plot
# df['colume'].plot()   
# plt.show()