#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# pylint: skip-file

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import datetime as dt
from bottle import Bottle, template, request, static_file
from pandas import DataFrame
import jsm

app = Bottle()

def jstock(code):
    target = jsm.Quotes().get_historical_prices(code)
    
    date = [data.date for data in target]
    open = [data.open for data in target]
    high = [data.high for data in target]
    low = [data.low for data in target]
    close = [data.close for data in target]
    volume = [data.volume for data in target]
    adj_close = [data._adj_close for data in target]

    Date = date[::-1]
    Open = open[::-1]
    High = high[::-1]
    Low = low[::-1]
    Close = close[::-1]
    Adj = adj_close[::-1]
    Vol = volume[::-1]

    cdf = DataFrame(index=Date)
    cdf.index.name = "Date"
    cdf["Open"] = Open
    cdf["High"] = High
    cdf["Low"] = Low
    cdf["Close"] = Close
    cdf["Adj Close"] = Adj
    cdf["Volume"] = Vol

    cdf.to_csv('data/{}.txt'.format(code))

    df = DataFrame(index=Date)
    df['Adj Close'] = Adj

    plt.figure()
    df['Adj Close'].plot(color='black')
    plt.grid()
    plt.savefig('image/{}.png'.format(code))

    return

@app.route('/')
def index():
    return template('index')

@app.post('/code/')
def do_index():
    code = request.forms.get('code')
    jstock(code)
    search = jsm.Quotes().search(code)
    Name = search[0].name
    financialData = jsm.Quotes().get_finance(code)
    finance = [
        financialData.market_cap,
        financialData.shares_issued,
        financialData.dividend_yield,
        financialData.dividend_one,
        financialData.per,
        financialData.pbr,
        financialData.price_min,
        financialData.round_lot
    ]
    imagepath = 'image/{}.png'.format(code)
    txtpath = 'data/{}.txt'.format(code)
    return template('result', imagepath=imagepath, txtpath=txtpath, code=code, Name=Name, finance=finance)

@app.get('/list/<list>')
def returnList(list):
    industries = {
        '0050': "農林・水産業",
        '1050': "鉱業",
        '2050': "建設業",
        '3050': "食料品",
        '3100': "繊維製品",
        '3150': "パルプ・紙",
        '3200': "化学",
        '3250': "医薬品",
        '3300': "石油・石炭製品",
        '3350': "ゴム製品",
        '3400': "ガラス・土石製品",
        '3450': "鉄鋼",
        '3500': "非鉄金属",
        '3550': "金属製品",
        '3600': "機械",
        '3650': "電気機器",
        '3700': "輸送機器",
        '3750': "精密機器",
        '3800': "その他製品",
        '4050': "電気・ガス業",
        '5050': "陸運業",
        '5100': "海運業",
        '5150': "空運業",
        '5200': "倉庫・運輸関連業",
        '5250': "情報・通信",
        '6050': "卸売業",
        '6100': "小売業",
        '7050': "銀行業",
        '7100': "証券業",
        '7150': "保険業",
        '7200': "その他金融業",
        '8050': "不動産業",
        '9050': "サービス業"
    }
    ind = industries[str(list)]
    rowdata = jsm.Quotes().get_brand(str(list))
    return template('list', list=list, ind=ind, rowdata=rowdata)

@app.get('/industry')
def returnIndustry():
    return template('industry')

@app.get('/image/<image>')
def returnImage(image):
    return static_file(image, root='./image/')

@app.get('/data/<txt>')
def returnText(txt):
    return static_file(txt, root='./data/')

@app.get('/css/<css>')
def returnCss(css):
    return static_file(css, root='./css/')

@app.get('/js/<js>')
def returnJs(js):
    return static_file(js, root='./js/')

@app.get('/logo.svg')
def returnSvg():
    return static_file('logo.svg', root='.')

@app.get('/logo2.svg')
def returnSvg():
    return static_file('logo2.svg', root='.')

@app.get('/apple-touch-icon.png')
def returnIcon():
    return static_file('apple-touch-icon.png', root='.')

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
