import pandas as pd
import folium
import requests, json

pdcities = pd.read_csv('cities.csv')
listc = pdcities[["id","name","dpto","lat","lon","population"]]

#clima
api_key = "20da860edb90c7fc86537181df2428de"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def assignc(name):
    for ind in listc.index:
        if name == str(listc['id'][ind]):
            complete_url = base_url + "appid=" + api_key + "&q=" + str(listc['name'][ind]) 
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                # Ubica la ciudad
            return y["temp"]-273.15;
#location=[9.2922333,-75.412339],zoom_start=7, #tiles='Stamen Terrain'