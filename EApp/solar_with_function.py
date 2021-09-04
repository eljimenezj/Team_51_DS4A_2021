import numpy as np
import pandas as pd
import folium
import datetime

#Función que crea el mapa, devuelve el mapa 'm', recibe:
#DHI_avgs: Dataframe del view "hist_dhi", que tiene los promedios de DHI por region y año
#year: año que se desea mostrar
#coordinates: Dataframe con el nombre de las ciudades, su latitud y longitud
#geojson: path del geojson
#Departamento a mostrar. 'All' los muestra todos

def getSolarMapByYearAndDept(year,geojson,departmentName):
    #Cargar view con los promedios de VHI por region y año
    DHI_avgs = pd.read_csv('hist_dhi.csv', delimiter=',')

    #Agregar Columnas de Departamentos    
    conditions=[(DHI_avgs['name']=='SABANALARGA'), #Atlantico
                (DHI_avgs['name']=='EL CARMEN DE BOLIVAR'), (DHI_avgs['name']=='CARTAGENA'), #Bolivar
                (DHI_avgs['name']=='DIBULLA (SIERRA NEVADA)'),(DHI_avgs['name']=='RIOHACHA'), #La guajira
                (DHI_avgs['name']=='PIVIJAY') , (DHI_avgs['name']=='CIÉNAGA') , (DHI_avgs['name']=='EL BANCO') , (DHI_avgs['name']=='ARIGUANÍ'), # Magdalena
                (DHI_avgs['name']=='MONTERÍA'),(DHI_avgs['name']=='SAHAGÚN'),(DHI_avgs['name']=='AYAPEL'), #Cordoba
                (DHI_avgs['name']=='SAMPUES'),#Sucre
                (DHI_avgs['name']=='NECOCLÍ'),(DHI_avgs['name']=='SAN PEDRO DE URABÁ'),(DHI_avgs['name']=='CAUCASIA'), #Antioquia
                (DHI_avgs['name']=='VALLEDUPAR'), #Cesar
               ]

    values=['ATLANTICO',
            'BOLIVAR','BOLIVAR',
            'LA GUAJIRA','LA GUAJIRA',
            'MAGDALENA','MAGDALENA','MAGDALENA','MAGDALENA',
            'CORDOBA','CORDOBA','CORDOBA',
            'SUCRE',
            'ANTIOQUIA','ANTIOQUIA','ANTIOQUIA',
            'CESAR']

    DHI_avgs['Departamento']=np.select(conditions,values)    
    
    #Get lat & lon
    coordinates= pd.read_csv('cities.csv', delimiter=',')
    latitudes=pd.Series(coordinates['lat'].values,index=coordinates['name']).to_dict()
    longitudes=pd.Series(coordinates['lon'].values,index=coordinates['name']).to_dict()
    
    #Agregar columna de lat & lon
    DHI_avgs['lat']=DHI_avgs['name']
    DHI_avgs['lat'].replace(latitudes,inplace=True)
    DHI_avgs['lon']=DHI_avgs['name']
    DHI_avgs['lon'].replace(longitudes,inplace=True)
    
    #Filter by year & dept name 
    DHI_avgs=DHI_avgs[DHI_avgs['year']==year]
    if not (departmentName=='all'):
        DHI_avgs=DHI_avgs[DHI_avgs['Departamento']==departmentName]
        
    #Agrupar por depto    
    groupedByDept=DHI_avgs[['Departamento','avg']].groupby(['Departamento'])['avg'].mean().to_frame()
    groupedByDept.reset_index(inplace=True)
        
    #Mapa
    m = folium.Map(location =[8.9338129,-75.4641746], zoom_start=6)
    folium.Choropleth(
        geo_data=geojson,
        name="Solar layout",
        data=groupedByDept,
        columns=["Departamento", "avg"],
        key_on="feature.properties.DPTO_CNMBR",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="DHI ",
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    
    #Marcadores
    DHI_avgs.apply(lambda row: folium.Marker(location=[row['lat'], row['lon']],
                                       icon=folium.Icon(color="green", icon="info-sign"),
                                       popup="<b>"+row['name']+"</b>"+"<br>"+"Avg DHI: "+str(f"{round(row['avg'],2)}")).add_to(m), axis=1)
    
    m.save('templates/solar_map.html')        
    return m
#Probar la función
#getSolarMapByYearAndDept(1999,'DpartamentosColombia.geojson','CESAR')
