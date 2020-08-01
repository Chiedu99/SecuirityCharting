import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
import shutil
import math

# yfinance documentation: https://github.com/ranaroussi/yfinance
# moving average: 6 months and 20 days behind




def changeDate(y):
    reformedstr = y.split('/')
    for i, char in enumerate(reformedstr):
        if len(char) == 1:
            char = '0' + char
            reformedstr[i] = char
    finalstr = [reformedstr[2], reformedstr[0], reformedstr[1]]
    returndate = '-'.join(finalstr)

    return returndate


def changestartDate(y):
    reformedstr = y.split('/')
    for i, char in enumerate(reformedstr):
        if len(char) == 1:
            char = '0' + char
            reformedstr[i] = char
    finalstr = [reformedstr[2], reformedstr[0], reformedstr[1]]
    if int(finalstr[1]) <= 6:
        finalstr[0] = str(int(finalstr[0]) - 1)
        finalremainder = 6 - int(finalstr[1])
        finalstr[1] = str(12 - finalremainder)
    else:
        finalstr[1] = str(int(finalstr[1]) - 6)

    returndate = '-'.join(finalstr)

    return returndate


def current_day(stock_name):
    return yf.Ticker(stock_name).info
    # This will return current data for a stock in a dictionary


class Stock:
    # This object will be used to retrieve data of a stock, current day and past

    def __init__(self, name):
        self.name = name
        self.ticker = yf.Ticker(name)

    @property
    def current_data(self):
        # This will retrieve current stock data, including volume and daily resistance/support
        return self.ticker.info

    @property
    def currentPrice(self):
        return self.ticker.info['ask']

    @property
    def currentVolume(self):
        return self.ticker.info['regularMarketVolume']

    @property
    def averageVolume(self):
        return self.ticker.info['averageVolume']

    @property
    def day_data(self):
        data = self.ticker.history(period='1d')
        temp2 = data['Open']
        temp3 = data['Close']
        temp4 = data['Volume']
        temp5 = data['Low']
        temp6 = data['High']
        temp7 = {**temp2, **temp3, **temp4, **temp5, **temp6}
        for k, v in temp7.items:
            for item in v:
                if item == 0:
                    del temp7[k]
        for key, value in temp4.items():
            if key in temp2 and key in temp3:
                temp7[key] = [temp2[key], temp3[key], temp4[key], temp5[key], temp6[key]]
        return temp7

    @property
    def week_data(self, start_date):
        data = self.ticker.history(period='5d')
        temp2 = data['Open']
        temp3 = data['Close']
        temp4 = data['Volume']
        temp5 = data['Low']
        temp6 = data['High']
        temp7 = {**temp2, **temp3, **temp4, **temp5, **temp6}
        for key, value in temp4.items():
            if key in temp2 and key in temp3:
                temp7[key] = [temp2[key], temp3[key], temp4[key], temp5[key], temp6[key]]
        return temp7

    @property
    def monthly_data(self, start_date=None):
        # This will return dictionary such as {Timestamp: [Open,Close,Volume,Low,High]}
        data = self.ticker.history(period='1mo')
        temp2 = data['Open']
        temp3 = data['Close']
        temp4 = data['Volume']
        temp5 = data['Low']
        temp6 = data['High']
        temp7 = {**temp2, **temp3, **temp4, **temp5, **temp6}
        for key, value in temp4.items():
            if key in temp2 and key in temp3:
                temp7[key] = [temp2[key], temp3[key], temp4[key], temp5[key], temp6[key]]
        return temp7

    @property
    def yearly_date(self):
        # This will return dictionary such as {Timestamp: [Open,Close,Volume,Low,High]}
        data = self.ticker.history(period='6mo')
        temp2 = data['Open']
        temp3 = data['Close']
        temp4 = data['Volume']
        temp5 = data['Low']
        temp6 = data['High']
        temp7 = {**temp2, **temp3, **temp4, **temp5, **temp6}
        for key, value in temp4.items():
            if key in temp2 and key in temp3:
                temp7[key] = [temp2[key], temp3[key], temp4[key], temp5[key], temp6[key]]

        dates = []
        for key in temp7.keys():
            dates.append(key)

        for i, item in enumerate([*dates]):
            dates[i] = item.strftime("%Y-%m-%d")

        fulllist = temp7.values()
        open = []
        close = []
        high = []
        low = []
        df = pd.DataFrame()
        for arr in fulllist:
            open.append(arr[0])
            close.append(arr[1])
            high.append(arr[4])
            low.append(arr[3])
        fig = go.Figure(data=[go.Candlestick(x=dates, open=open, high=high, low=low, close=close)])
        print('starting-1')
        fig.show()
        return temp7

    def exactInterval(self, interval, start, end):
        # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        data = yf.download(tickers=self.name, interval=interval, start=start, end=end)
        temp2 = data['Open']
        temp3 = data['Close']
        temp4 = data['Volume']
        temp5 = data['Low']
        temp6 = data['High']
        temp8 = data['Volume']
        temp7 = {**temp2, **temp3, **temp4, **temp5, **temp6, **temp8}
        for key, value in temp4.items():
            if key in temp2 and key in temp3:
                temp7[key] = [temp2[key], temp3[key], temp4[key], temp5[key], temp6[key], temp8[key]]

        dates = []
        for key in temp7.keys():
            dates.append(key)
        print(dates)

        for i, item in enumerate([*dates]):
            dates[i] = item.strftime("%Y-%m-%d-%X")

        fulllist = temp7.values()
        open = []
        close = []
        high = []
        low = []
        volume = []
        df = pd.DataFrame()
        for arr in fulllist:
            open.append(arr[0])
            close.append(arr[1])
            high.append(arr[4])
            low.append(arr[3])
            volume.append(arr[5])
        print(dates)
        print(open)
        volumeTrace = {"name": "Volume", "type": "bar", "x": dates, "y": volume, 'yaxis': "y"}
        trace1 = {"name": 'candle', "type": "candlestick", "x": dates, "low": low, "high": high, "open": open,
                  'close': close, "yaxis": "y2"}
        layout = {"yaxis": {
            "type": "linear",
            "domain": [0, 0.2],
            "autorange": True
        }, "yaxis2": {
            "type": "linear",

            "domain": [0.2, 0.9]
        }}

        fig = go.Figure(data=[volumeTrace, trace1], layout=layout)
        fig.update_layout(
            title={
                'text': self.name.upper(),
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        print(fig.show())

        return "Finished process"

    def custom_range(self, startDate, endDate):
        # [Open, Close, Volume, Low, High]}
        start = changeDate(startDate)
        startSMA = changestartDate(startDate)
        print(start)
        end = changeDate(endDate)
        data = self.ticker.history(start=start, end=end)
        dataSMA = self.ticker.history(start=startSMA, end=end)
        temp2 = data['Open']
        temp3 = data['Close']
        temp4 = data['Volume']
        temp5 = data['Low']
        temp6 = data['High']
        tempSMA = dataSMA['Close']
        datapoints = {**tempSMA}.values()
        smadatapoints = []
        for value in datapoints:
            smadatapoints.append(value)

        print(smadatapoints)
        temp7 = {**temp2, **temp3, **temp4, **temp5, **temp6}

        for key, value in temp4.items():
            if key in temp2 and key in temp3:
                temp7[key] = [temp2[key], temp3[key], temp4[key], temp5[key], temp6[key]]

        dates = []
        for key in temp7.keys():
            dates.append(key)

        for i, item in enumerate([*dates]):
            dates[i] = item.strftime("%Y-%m-%d")

        fulllist = temp7.values()
        open = []
        close = []
        high = []
        low = []
        df = pd.DataFrame()
        for arr in fulllist:
            open.append(arr[0])
            close.append(arr[1])
            high.append(arr[4])
            low.append(arr[3])

        fig = go.Figure(data=[go.Candlestick(x=dates, open=open, high=high, low=low, close=close)])
        print('starting-1')
        fig.show()
        print('starting')

        return temp7

    def movingAverage(self, start,end):
        # This will return dictionary such as {Timestamp: [Open,Close,Volume,Low,High]}
        data = self.ticker.history(start=start, end=end)
        temp2 = data['Open']
        temp3 = data['Close']
        temp4 = data['Volume']
        temp5 = data['Low']
        temp6 = data['High']
        temp7 = {**temp2, **temp3, **temp4, **temp5, **temp6}
        datapoints = {**temp3}.values()
        datapoints2 = []
        smadatapoints = []
        x = 0
        y = 1
        for value in datapoints:
            datapoints2.append(value)
        for value in datapoints2:
            x += value
            appendval = x / y
            smadatapoints.append(appendval)
            y += 1

        for key, value in temp4.items():
            if key in temp2 and key in temp3:
                temp7[key] = [temp2[key], temp3[key], temp4[key], temp5[key], temp6[key]]

        dates = []
        for key in temp7.keys():
            dates.append(key)

        for i, item in enumerate([*dates]):
            dates[i] = item.strftime("%Y-%m-%d")

        movingaverage = dict(zip(dates, smadatapoints))
        print(movingaverage)
        fulllist = temp7.values()
        open = []
        close = []
        high = []
        low = []
        df = pd.DataFrame()
        for arr in fulllist:
            open.append(arr[0])
            close.append(arr[1])
            high.append(arr[4])
            low.append(arr[3])

        trace1 = {"type": "candlestick", "x": dates, "low": low, "high": high, "open": open, "yaxis": "y2"}

        trace2 = {"line": {"width": 1}, "mode": "lines", "name": "Moving Averges", "type": "scatter", "x": dates,
                  "y": smadatapoints, "marker": {"color": "#E377C2"}}

        fig = go.Figure(data=[trace2, go.Candlestick(x=dates, open=open, high=high, low=low, close=close)])
        fig.show()

        return temp7

    def volumePeriod(self, start=None, end=None):
        data = yf.download(tickers=self.name, start=start, end=end)
        temp2 = data['Open']
        temp3 = data['Close']
        temp4 = data['Volume']
        temp5 = data['Low']
        temp6 = data['High']
        temp8 = data['Volume']
        temp7 = {**temp2, **temp3, **temp4, **temp5, **temp6, **temp8}
        for key, value in temp4.items():
            if key in temp2 and key in temp3:
                temp7[key] = [temp2[key], temp3[key], temp4[key], temp5[key], temp6[key], temp8[key]]

        dates = []
        for key in temp7.keys():
            dates.append(key)
        print(dates)

        for i, item in enumerate([*dates]):
            dates[i] = item.strftime("%Y-%m-%d-%X")

        fulllist = temp7.values()
        open = []
        close = []
        high = []
        low = []
        volume = []
        df = pd.DataFrame()
        for arr in fulllist:
            open.append(arr[0])
            close.append(arr[1])
            high.append(arr[4])
            low.append(arr[3])
            volume.append(arr[5])
        print(dates)
        print(open)
        volumeTrace = {"name": "Volume", "type": "bar", "x": dates, "y": volume, 'yaxis': "y"}
        trace1 = {"name": 'candle', "type": "candlestick", "x": dates, "low": low, "high": high, "open": open,
                  'close': close, "yaxis": "y2"}
        layout = {"yaxis": {
            "type": "linear",
            "domain": [0, 0.2],
            "autorange": True
        }, "yaxis2": {
            "type": "linear",

            "domain": [0.2, 0.9]
        }}

        fig = go.Figure(data=[volumeTrace, trace1], layout=layout)
        print(fig.show())

        return "Finished process"











stock = Stock('aapl')
stock.exactInterval('1d','2019-4-22','2020-4-23')
