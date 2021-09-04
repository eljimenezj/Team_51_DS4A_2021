import pandas as pd
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
from modelos import * 

def periodo(inicio, fin):
    d0 = date(*(int(s) for s in inicio.split('-')))
    d1 = date(*(int(s) for s in fin.split('-')))
    delta = d1 - d0
    
    if delta.days < 0:
        return print("Fecha inicio mayor que fecha fin")
        neg = delta.days
    else:
        c = delta.days
    return c

def table_predict(city, finicio, ffin):
    '''
    fecha : YYYY-MM-DD
    '''

    df2 = pd.read_csv('data/'+str(city)+'.csv')
    df2['Date'] =  pd.to_datetime(df2['Date'],errors='coerce')
    df2 = df2[['Date', 'y']]
    df2.columns = ['ds', 'y']
    df2 = df2[(df2['ds'].dt.hour>=6) & (df2['ds'].dt.hour<=18)]
    
    # create datetime index passing the datetime series
    datetime_index = pd.DatetimeIndex(df2.ds.values)
    df2=df2.set_index(datetime_index)
    df2.drop('ds',axis=1,inplace=True)
    
    # Create future empty values
    c = periodo(finicio, ffin)
    idx = pd.date_range(df2.index[-1] + pd.Timedelta(hours=7), periods=24*c, freq='h')[1:]
    
    table = df2.append(pd.DataFrame(pd.Series(np.repeat(0, len(idx)), index=idx), columns= ['y']))
    table = table[(table.index.hour>=6) & (table.index.hour<=18)]
    
    return table, c
	

def calculate_lags(df2):
    # Lag for the time: day, week, month, quarter, semester, annual
    serie2 =pd.concat([df2,df2.y.shift(91),df2.y.shift(104),df2.y.shift(117),df2.y.shift(130),df2.y.shift(143)
                      ,df2.y.shift(156),df2.y.shift(169),df2.y.shift(182),df2.y.shift(390)
                      ,df2.y.shift(403),df2.y.shift(1170), df2.y.shift(1183),df2.y.shift(1196)
                      ,df2.y.shift(1209),df2.y.shift(2340), df2.y.shift(2353), df2.y.shift(2366)
                      ,df2.y.shift(2379),df2.y.shift(3900),df2.y.shift(4745)],
              axis=1)

    # Columns 
    columns_name2 = ['y','t_7','t_8','t_9','t_10','t_11','t_12','t_13','t_14',
                    't_30','t_31','t_90','t_91','t_92','t_93','t_180',
                    't_181','t_182','t_183','t_300','t_365']
    
    serie2.columns = columns_name2
    
    serie2 = serie2.dropna()

    return serie2
	
	
def forecast_values(serie, days):
    c = days * 13
    serie = serie[-c:]
    X_pred = serie.drop(['y'], axis=1)
    
    return X_pred

def table_show(table, inicio, forecast):
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
    name2 = ['DHI_Forecast']
    salida.columns = name2
    return salida

#source
ciudad_temp = pd.read_csv('cities_prom.csv')

def consumo_solar(city, irrad):
    if irrad <= 0:
        irrad = irrad + 0.1
        
    temp = ciudad_temp[ciudad_temp['name']==city]['temperature']
    pot_sol= potencia_solar(temp, irrad,36)
    if pot_sol < 0:
        pot_sol = 0
    return pot_sol

def final_table_solar(city, pred_MLP_1, p_tabla):
    column_generation = pd.DataFrame([consumo_solar(city,x) for x in pred_MLP_1])
    name_temp = ['G2']
    column_generation.columns = name_temp
    
    p_tabla['G'] = 0
    final_table = p_tabla.assign(G=column_generation['G2'].values)
    name_cg = ['DHI_Forecast','Generated Power (W)']
    final_table.columns = name_cg
    return final_table