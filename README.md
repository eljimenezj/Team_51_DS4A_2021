# DS4A 2021 Edition - Colombia

Repository of the Team-51 participating in the 5th cohort of Data Science for All.

## Project Overview
We were assigned to Dynamic Defense Solutions, a colombian company who wants to understand the potential of renewable energy generation (mainly solar and wind) in different areas of the country. In order to achieve this, we set 3 main objectives in this project:
- Identify regions with energy generation potential from descriptive analysis of irradiance and wind speed data.
- Efficiently calculate and visualize energy generation results and identify temporal patterns that affect it.
- Implement predictive models of consumption and generation to project state or private investment opportunities and economic benefits for the inhabitants of the study region in a window of time.

## Members 

- Laura Milena Manrique Garzón.
- Edgar Leandro Jimenez.
- Juan Manuel Muskus.
- Arturo Quevedo.
- William Prieto.
- Juan Felipe Múnera Vergara

![alt text](https://github.com/eljimenezj/Team_51_DS4A_2021/blob/main/Images/team51.PNG?raw=true)

##  Architecture 

Our solution is deployed on a virtual private server (VPS) with ubuntu 20.04 LTS operating system in digitalocean.com, we use flask as a development framework in python to connect HTML pages with CSS style sheets, The information presented comes basically from two sources: dataframe in cvs format and queries to our postgres server. 
For the geolocation we use the javascript library geojs that has a higher performance in rendering and layer insertion. The dataframe was manipulated with pandas and the graphics were created with the bokeh and mpld3 libraries. The predictive models we used the python libraries skforecast and sklearn, which are loaded with joblib for deployment.
Finally, for the VPS we installed gunicorn, nginx and postgres services as functional dependencies for the deployment of the eapp web application.
The architecture used for the development of the project was as follows:

![alt text](https://github.com/eljimenezj/Team_51_DS4A_2021/blob/main/Images/architecture.PNG?raw=true)

##  Video Presentation 

![alt text](https://github.com/eljimenezj/Team_51_DS4A_2021/blob/main/Images/video.PNG?raw=true)

[Video Team 51](https://www.youtube.com/watch?v=U3CBH6R0tgU)

## Dataset

We were provided with datas sets that contain weather information taken from meteorological stations associated to the company. The data sets contain meteorological records such as irradiance, wind speed, temperature, relative humidity, wind direction and pressure of every half hour since 1998. 







