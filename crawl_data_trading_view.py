import requests
import json
import pandas as pd
import os
import datetime


def data_from_tradingview(symbol):
    trading_view_data_url = 'https://iboard.ssi.com.vn/dchart/api/history'
    data_json = {
        'date': [],
        'open': [],
        'high': [],
        'low': [],
        'close': [],
        'volume': [],
    }
    now = datetime.datetime.now()
    current_year = now.year
    for year in range(2000, current_year):

        begin_date = int(datetime.datetime(year, 1, 1).timestamp())
        end_date = int(datetime.datetime(year, 12, 31).timestamp())

        response = requests.get(
            f'{trading_view_data_url}?symbol={symbol}&resolution=D&from={begin_date}&to={end_date}')
        response_data = json.loads(response.text)
        data_json['date'].extend(response_data['t'])
        data_json['open'].extend(response_data['o'])
        data_json['high'].extend(response_data['h'])
        data_json['low'].extend(response_data['l'])
        data_json['close'].extend(response_data['c'])
        data_json['volume'].extend(response_data['v'])

       
    
    df_file = pd.DataFrame(data_json)
    df_file['date'] = pd.to_datetime(df_file['date'], unit='s')
    return df_file.set_index('date')




def getAllStocks():
    response = requests.get('https://iboard.ssi.com.vn/dchart/api/1.1/defaultAllStocks')
    response_data = json.loads(response.text)
    array_data = response_data['data']
   
    data_frame = pd.DataFrame(array_data)[['clientName','code','type','exchange']].sort_values(by=['code'],ignore_index=True)
    return data_frame
