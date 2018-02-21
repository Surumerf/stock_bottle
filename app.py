#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# pylint: skip-file

import os
import datetime as dt
from bottle import Bottle, template, request, static_file
from pandas import DataFrame
# import pandas_datareader.data as web
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

    cdf.to_csv('stock.txt')

    return

@app.route('/')
def index():
    return template('index')

@app.post('/code/')
def do_index():
    code = request.forms.get('code')
    jstock(code)
    return static_file('stock.txt', root='.')

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
