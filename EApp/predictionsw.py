import pandas as pd
import random
import seaborn as sns
import numpy as np
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.ForecasterAutoregCustom import ForecasterAutoregCustom
from skforecast.ForecasterAutoregMultiOutput import ForecasterAutoregMultiOutput
from skforecast.model_selection import grid_search_forecaster
from skforecast.model_selection import time_series_spliter
from skforecast.model_selection import cv_forecaster
from skforecast.model_selection import backtesting_forecaster
from skforecast.model_selection import backtesting_forecaster_intervals
from sklearn.experimental import enable_hist_gradient_boosting  # noqa
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import datetime
from datetime import date
import joblib
import matplotlib.pyplot as plt
import modelos
from modelos import densidad_aire, potencia_viento, potencia_viento_modificada, potencia_solar


def periodo2(inicio, fin):
    d0 = date(*(int(s) for s in inicio.split('-')))
    d1 = date(*(int(s) for s in fin.split('-')))
    delta = d1 - d0
    
    if delta.days < 0:
        return print("Fecha inicio mayor que fecha fin")
        neg = delta.days
    else:
        c = delta.days
    return c

#from datetime import datetime
def table_predict2(city, inicio, fin):
    '''
    fecha : YYYY-MM-DD
    '''

    df2 = pd.read_csv('dataw/'+str(city)+'.csv')
    df2['Date'] =  pd.to_datetime(df2['Date'],errors='coerce')
    df2 = df2[['Date', 'y']]
    df2.columns = ['ds', 'y']

    
    # create datetime index passing the datetime series
    datetime_index = pd.DatetimeIndex(df2.ds.values)
    df2=df2.set_index(datetime_index)
    df2.drop('ds',axis=1,inplace=True)
    
    # Create future empty values
    c = periodo2(inicio,fin)
    idx = pd.date_range(df2.index[-1] + pd.Timedelta(hours=1), periods=24*c, freq='h')[0:]
    table = df2.append(pd.DataFrame(pd.Series(np.repeat(0, len(idx)), index=idx), columns= ['y']))
    
    return table, c

## lags
def calculate_lags2(df2):
    # Lag for the time: day, week, month, quarter, semester, annual
    serie2 =pd.concat([df2,df2.y.shift(168),df2.y.shift(192),df2.y.shift(216),df2.y.shift(240),df2.y.shift(264)
                      ,df2.y.shift(288),df2.y.shift(312),df2.y.shift(336),df2.y.shift(720)
                      ,df2.y.shift(744),df2.y.shift(1440),df2.y.shift(1464)
                      ,df2.y.shift(2160), df2.y.shift(2184),df2.y.shift(2208)
                      ,df2.y.shift(2232)
                      ,df2.y.shift(4320), df2.y.shift(4344), df2.y.shift(4368)
                      ,df2.y.shift(4392),df2.y.shift(7200),df2.y.shift(8760)],
              axis=1)

    # Columns 
    columns_name2 = ['y','t_7',
                    't_8','t_9','t_10','t_11','t_12','t_13','t_14',
                    't_30','t_31','t_60','t_61','t_90','t_91','t_92','t_93'
                    ,'t_180'
                    ,'t_181','t_182','t_183','t_300','t_365']
    
    serie2.columns = columns_name2
    
    serie2 = serie2.dropna()

    return serie2
	
def forecast_values2(serie, days):
    c = days * 24
    serie = serie[-c:]
    X_pred = serie.drop(['y'], axis=1)
    
    return X_pred
	
import random
def table_show2(table, inicio, forecast):
    
    inicio = date(*(int(s) for s in inicio.split('-')))
    inicio += datetime.timedelta(days=1)
    inicio = inicio.strftime('%Y/%m/%d')

    salida = table[table.index > inicio]
    salida['y'] = 0
    
    temp = pd.DataFrame(forecast)
    temp = round(temp,1)
    name = ['y']
    temp.columns= name
    
    salida = salida.assign(y=temp['y'].values)
    name2 = ['Wind Speed_Forecast']
    salida.columns = name2
    
    return salida
	

ciudad_temp = pd.read_csv('cities_prom.csv')

def consumo_viento(city, vel):
    
    if vel <= 0:
        vel = vel + 0.1
        
    temp = ciudad_temp[ciudad_temp['name']==city]['temperature']
    temp = temp.values[0]
    
    hr = ciudad_temp[ciudad_temp['name']==city]['relative_humidity']
    hr = hr.values[0] 
    
    pot_win= potencia_viento_modificada(vel, temp, 90)
    
    if pot_win < 0:
        pot_win = 0
    return pot_win
	
	
def final_table_wind(city,pred_MLP_2,p_tabla2):
    column_generation = pd.DataFrame([consumo_viento(city,x) for x in pred_MLP_2])

    name_temp = ['G2']
    column_generation.columns = name_temp
    
    p_tabla2['G'] = 0
    final_table = p_tabla2.assign(G=column_generation['G2'].values)
    name_cg = ['Wind Speed_Forecast','Generated Power (W)']
    final_table.columns = name_cg
    return final_table