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
    df['Adj Close'].plot()
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

@app.get('/code/image/<image>')
def returnImage(image):
    return static_file(image, root='./image/')

@app.get('/code/data/<txt>')
def returnText(txt):
    return static_file(txt, root='./data/')

@app.get('/css/<css>')
def returnCss(css):
    return static_file(css, root='./css/')

@app.get('/code/css/<css>')
def returnCss(css):
    return static_file(css, root='./css/')

@app.get('/code/js/<js>')
def returnJs(js):
    return static_file(js, root='./js/')

@app.get('/logo.svg')
def returnSvg():
    return static_file('logo.svg', root='.')

@app.get('/code/logo2.svg')
def returnSvg():
    return static_file('logo2.svg', root='.')

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
