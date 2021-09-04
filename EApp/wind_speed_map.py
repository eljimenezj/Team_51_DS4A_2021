import numpy as np
import pandas as pd
import folium
import datetime

def get_wind_speed_map(year,geojson,departmentName):
    avg_ws=pd.read_csv('hist_wind_speed.csv', delimiter=',')

    #Agregar Columnas de Departamentos    
    conditions=[(avg_ws['name']=='SABANALARGA'), #Atlantico
                (avg_ws['name']=='EL CARMEN DE BOLIVAR'), (avg_ws['name']=='CARTAGENA'), #Bolivar
                (avg_ws['name']=='DIBULLA (SIERRA NEVADA)'),(avg_ws['name']=='RIOHACHA'), #La guajira
                (avg_ws['name']=='PIVIJAY') , (avg_ws['name']=='CIÉNAGA') , (avg_ws['name']=='EL BANCO') , (avg_ws['name']=='ARIGUANÍ'), # Magdalena
                (avg_ws['name']=='MONTERÍA'),(avg_ws['name']=='SAHAGÚN'),(avg_ws['name']=='AYAPEL'), #Cordoba
                (avg_ws['name']=='SAMPUES'),#Sucre
                (avg_ws['name']=='NECOCLÍ'),(avg_ws['name']=='SAN PEDRO DE URABÁ'),(avg_ws['name']=='CAUCASIA'), #Antioquia
                (avg_ws['name']=='VALLEDUPAR'), #Cesar
               ]

    values=['ATLANTICO',
            'BOLIVAR','BOLIVAR',
            'LA GUAJIRA','LA GUAJIRA',
            'MAGDALENA','MAGDALENA','MAGDALENA','MAGDALENA',
            'CORDOBA','CORDOBA','CORDOBA',
            'SUCRE',
            'ANTIOQUIA','ANTIOQUIA','ANTIOQUIA',
            'CESAR']

    avg_ws['Departamento']=np.select(conditions,values)

    #Get lat & lon
    coordinates= pd.read_csv('cities.csv', delimiter=',')
    latitudes=pd.Series(coordinates['lat'].values,index=coordinates['name']).to_dict()
    longitudes=pd.Series(coordinates['lon'].values,index=coordinates['name']).to_dict()

    #Agregar columna de lat & lon
    avg_ws['lat']=avg_ws['name']
    avg_ws['lat'].replace(latitudes,inplace=True)
    avg_ws['lon']=avg_ws['name']
    avg_ws['lon'].replace(longitudes,inplace=True)

    #Filter by year & dept name 
    avg_ws=avg_ws[avg_ws['year']==year]
    if not (departmentName=='all'):
        avg_ws=avg_ws[avg_ws['Departamento']==departmentName]

    #Agrupar por depto    
    groupedByDept=avg_ws[['Departamento','avg']].groupby(['Departamento'])['avg'].mean().to_frame()
    groupedByDept.reset_index(inplace=True)

    #Mapa
    m = folium.Map(location =[8.9338129,-75.4641746], zoom_start=6)
    folium.Choropleth(
        geo_data=geojson,
        name="Wind layout",
        data=groupedByDept,
        columns=["Departamento", "avg"],
        key_on="feature.properties.DPTO_CNMBR",
        fill_color="GnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Wind speed ",
    ).add_to(m)

    folium.LayerControl().add_to(m)

    #Marcadores
    avg_ws.apply(lambda row: folium.Marker(location=[row['lat'], row['lon']],
                                       icon=folium.Icon(color="red", icon="info-sign"),
                                       popup="<b>"+row['name']+"</b>"+"<br>"+"Avg wind speed: "+str(f"{round(row['avg'],2)}")).add_to(m), axis=1)

    m.save("templates/wind_map.html")
    return m

#get_wind_speed_map(1999,'DpartamentosColombia.geojson','all')