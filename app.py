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
    plt.title(code)
    plt.savefig('image/{}.png'.format(code))

    return

@app.route('/')
def index():
    return template('index')

@app.post('/code/')
def do_index():
    code = request.forms.get('code')
    jstock(code)
    imagepath = 'image/{}.png'.format(code)
    txtpath = 'data/{}.txt'.format(code)
    return template('result', imagepath=imagepath, txtpath=txtpath)

@app.get('/code/image/<image>')
def returnImage(image):
    return static_file(image, root='./image/')

@app.get('/code/data/<txt>')
def returnText(txt):
    return static_file(txt, root='./data/')

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
