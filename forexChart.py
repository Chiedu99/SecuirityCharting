import fxcmpy
import socketio
import pandas as pd
import plotly.graph_objects as go
import datetime as dt
import dateutil.relativedelta
import math

# 239f5b3cd1685b1ba0dbd66ddf9c1764b6ae40bd



class BackTest:
    """ access_token: string (default: ''),
        an access token for your FXCM account. To create an access token
        visit https://tradingstation.fxcm.com/
    config_file: string (default: ''),
        path of an optional configuration file, fxcm tries to read all
        other parameter which are not given from that file. The file must
        be readable by configparser.
    log_file: string (default: None),
        path of an optional log file. If not given (and not found in the
        optional configuration file), log messages are printed to stdout.
    log_level: string (default: 'warn'),
        the log level. Must be one of 'error', 'warn', 'info' or 'debug'.
        If not given (and not found in the optional configuration file),
        'warn' is used.
    server: one of 'demo' or 'real' (default: 'demo'),
        wheter to use the fxcm demo or real trading server.
    proxy_url, string (default: None):
        if given (or found in the optional configuration file), the url is
        used for pproxy.
    proxy_port, integer (default: None):
        if proxy_url is given (or found in the optional configuration file),
        this is the port of the proxy server.
    proxy_type, one of 'http', 'socks4', 'socks5' or None (default: 'http'),
        if proxy_url is given (or found in the optional configuration file),
        this is the type of the proxy server.  """

    def __init__(self, access_token='', config_file='', log_file=None, log_level='', server='demo',proxy_url=None, proxy_port=None, proxy_type=None):
        self.server = fxcmpy.fxcmpy(access_token=access_token, config_file=config_file,
                 log_file=log_file, log_level=log_level, server=server,
                 proxy_url=proxy_url, proxy_port=proxy_port, proxy_type=proxy_type)





    # minutes: m1, m5, m15 and m30,hours: H1, H2, H3, H4, H6 and H8,one day: D1,one week: W1,one month: M1.
    #start = dt.datetime(2017, 7, 15)
    def collectDataPeriod(self, pair, period=None, start=None, end=None, columns = None):
        if start is None:
            data = self.server.get_candles(instrument=pair, period=period)
        if columns is None:
            data = self.server.get_candles(instrument=pair, period=period, start=start, stop=end)
        else:

            data = self.server.get_candles(instrument = pair,period=period, start = start, stop = end, columns = columns )
        return data

    #Helper function for collect data to get earliest start date
    @staticmethod
    def findEarliestStartDate(indicators):
        date = 0
        for item in indicators:
            if item[0] == 'SMA':
                if date < item[1]:
                    date = item[1]

        return date
    @staticmethod
    def SMA():
        pass

    @staticmethod
    def plot(data,pair,period):
        temp2 = data['askopen']
        temp3 = data['askclose']
        temp4 = data['tickqty']
        temp5 = data['asklow']
        temp6 = data['askhigh']
        temp8 = data['tickqty']
        temp7 = {**temp2, **temp3, **temp4, **temp5, **temp6, **temp8}
        for key, value in temp4.items():
            if key in temp2 and key in temp3:
                temp7[key] = [temp2[key], temp3[key], temp4[key], temp5[key], temp6[key], temp8[key]]
        dates = []
        for key in temp7.keys():
            dates.append(key)
        for i, item in enumerate([*dates]):
            dates[i] = item.strftime("%Y-%m-%d-%X")

        fulllist = temp7.values()
        print(fulllist)
        open = []
        close = []
        high = []
        low = []
        volume = []
        for arr in fulllist:
            open.append(arr[0])
            close.append(arr[1])
            high.append(arr[4])
            low.append(arr[3])
            volume.append(arr[5])
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

        fig = go.Figure(data=[trace1], layout=layout)
        fig.update_layout(
            title={
        'text': pair + ' '+ period,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
            )
        return fig.show()
    @staticmethod
    def graph(data,rawData, traceDate, indicators,offset):
        # listOfRequiredData will be a list with two elements, index 0 will be the data points that will be graphed,
        # index 1 will be a list of a dictionaries(layout)
        smadatapoints = []
        for item in indicators:
            if item[0]== "SMA":
                offsetval = offset-item[1]
                datacalc = rawData.iloc[offsetval:]
                datacalc.set_option("display.max_rows", None, "display.max_columns", None)
                print(datacalc)
                temp = datacalc['askclose']
                datapoints = {**temp}.values()
                datapoints2 = []
                counter = 0
                x = 0
                y = 1
                for value in datapoints:
                    datapoints2.append(value)
                print(len(datapoints2))
                for value in datapoints2:
                    x += value
                    appendval = x / y
                    smadatapoints.append(appendval)
                    y += 1
                smadatapoints = smadatapoints[item[1]:]



        listOfRequiredData = []
        print(len(smadatapoints))
        temp2 = data['askopen']
        temp3 = data['askclose']
        temp4 = data['tickqty']
        temp5 = data['asklow']
        temp6 = data['askhigh']
        temp8 = data['tickqty']
        temp7 = {**temp2, **temp3, **temp4, **temp5, **temp6, **temp8}
        for key, value in temp4.items():
            if key in temp2 and key in temp3:
                temp7[key] = [temp2[key], temp3[key], temp4[key], temp5[key], temp6[key], temp8[key]]
        dates = []
        for key in temp7.keys():
            dates.append(key)
        for i, item in enumerate([*dates]):
            dates[i] = item.strftime("%Y-%m-%d-%X")

        fulllist = temp7.values()

        open = []
        close = []
        high = []
        low = []
        volume = []
        for arr in fulllist:
            open.append(arr[0])
            close.append(arr[1])
            high.append(arr[4])
            low.append(arr[3])
            volume.append(arr[5])


        trace1 = {"name": 'candle', "type": "candlestick", "x": dates, "low": low, "high": high, "open": open,
                  'close': close, "yaxis": "y2"}
        trace2 = {"line": {"width": 1}, "mode": "lines", "name": "Moving Averges", "type": "scatter", "x": dates,
                  "y": smadatapoints, "marker": {"color": "#E377C2"}}
        layout = {"yaxis": {
            "type": "linear",
            "domain": [0.2, 0.9],
            "autorange": True
        }, "yaxis2": {
            "type": "linear",

            "domain": [0,0.2]
        }}



        fig = go.Figure(data= [trace2, go.Candlestick(x=dates, open=open, high=high, low=low, close=close)], layout=layout)
        #fig.show()



    def collectData(self, pair, period=None, start=None, end=None, columns = None, number = None,plot = None ,indicators = None):
        traceDate = start
        if start is None:
            rawData = self.server.get_candles(instrument=pair, period=period, number = number)
        if indicators is not None:

            offset = self.findEarliestStartDate(indicators)
            print(math.ceil((offset//5)*2))
            start = start - dateutil.relativedelta.relativedelta(days = math.ceil((offset//5)*2)+offset)

            rawData = self.server.get_candles(instrument=pair, period=period, start=start, stop=end)

        else:
            rawData = self.server.get_candles(instrument=pair, period=period, start=start, stop=end)

        data = rawData.loc[traceDate:]

        if plot is True:
            if indicators is None:
                self.plot(data,pair,period)
            else:
                self.graph(data,rawData, traceDate,indicators,offset)

        return 'done'















backTest = BackTest(access_token='239f5b3cd1685b1ba0dbd66ddf9c1764b6ae40bd', log_level="error")

print(backTest.collectData('EUR/USD','m1',dt.datetime(2020,4,11),dt.datetime(2020,4,23), plot = True))



