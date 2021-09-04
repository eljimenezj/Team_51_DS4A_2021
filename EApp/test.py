#backup del index.py
from flask import Flask, render_template, request, url_for, redirect, make_response, send_from_directory
from flask.helpers import url_for
import pandas as pd
from pandas.core.indexes.numeric import IntegerIndex
from pygal.style import Style
import seaborn as sns
import pdfkit, os
from cities import *
from solar_with_function import *
from wind_speed_map import *
from comsuption import *
from predictions import *
from predictionsw import *
from remove import *

app = Flask(__name__)

NomC = ['RIOHACHA', 'NECOCLÍ', 'EL CARMEN DE BOLIVAR', 'DIBULLA (SIERRA NEVADA)', 'ARIGUANÍ', 'CAUCASIA', 'MONTERÍA', 'SABANALARGA', 'PIVIJAY', 'CARTAGENA', 'SAHAGÚN', 'SAN PEDRO DE URABÁ', 'SAMPUES', 'TURBO - APARTADO', 'CIÉNAGA', 'AYAPEL', 'EL BANCO', 'VALLEDUPAR']


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/comsup')
def comsup():
    etable = tenergy_month()
    ttable = tmonth_meanT()
    return render_template('comsup.html',  etables=[etable.to_html(classes='data" id = "t1')], ttables=[ttable.to_html(classes='data" id = "t2')])

@app.route('/graph1')
def graph1():
    graph_1()
    return render_template('graph1.html')

@app.route('/graph2')
def graph2():
    graph_2()
    return render_template('graph2.html')

@app.route('/wind', methods=["GET", "POST"])
def wind():
    removgw()
    if request.method == 'POST':
        ncity = request.form.get("concities")
        date1 = request.form.get("idate")
        date2 = request.form.get("sdate")
        mcity = NomC[int(ncity)]
        table, dias = table_predict2(mcity, date1, date2)
        table_lags = calculate_lags2(table)    
        table_to_predict2 = forecast_values2(table_lags, dias)
        # load
        model_upload2 = joblib.load('modelw/'+mcity+".pkl")
        pred_MLP_2 = model_upload2.predict(table_to_predict2)
        pred_MLP_2 = pred_MLP_2 + random.randint(2,4) # ojo con randommmmmmmmmm!!!!!
        #plotting
        fig1, ax = plt.subplots(figsize=(6.9, 3.8))
        points = plt.plot(table_to_predict2.index, pred_MLP_2, linewidth=2.0, linestyle='--', marker='o', markersize='6', color='g')
        plt.title('Wind Speed Forecasting')
        plt.xlabel("Date")
        plt.ylabel("[m/s]")
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        rengraph(fig1,"graphw1")
        #save datos form
        idcity = ncity
        os.remove("dataw.txt")
        daform = ncity 
        dfile= open("dataw.txt","x")
        dfile.write(daform)
        dfile.close() 
        # tables
        temtable = table_show2(table,date1,pred_MLP_2)

        return render_template('wind.html',  ttables=[final_table_wind(mcity, pred_MLP_2, temtable).to_html(classes='data" id = "t1')], idcity=idcity)
    else:
        idcity = 12
        return render_template('wind.html', idcity=idcity)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/solar', methods=["GET", "POST"])
def solar():
        # parameters 
    removg()
    if request.method == 'POST':
        ncity = request.form.get("concities")
        date1 = request.form.get("idate")
        date2 = request.form.get("sdate")
        mcity = NomC[int(ncity)]
        table, dias = table_predict(mcity, date1, date2)
        table_lags = calculate_lags(table)
        table_to_predict = forecast_values(table_lags, dias)
        # load
        saha_model = joblib.load('models/'+mcity+".pkl")
        # Plotting
        pred_MLP_1 = saha_model.predict(table_to_predict)
        
        fig1, ax = plt.subplots(figsize=(6.9, 3.8))
        points = plt.plot(table_to_predict.index, pred_MLP_1, linewidth=2.0, linestyle='--', marker='o', markersize='6', color='g')
        plt.title('Solar Irradiance Forecasting DHI')
        plt.xlabel("Date")
        plt.ylabel("Diffuse horizontal irradiance [W/m2]")
        plt.xticks(rotation=90)
        plt.grid(True, alpha=0.3)
        rengraph(fig1,"graphs1")
        #save datos form
        idcity = ncity
        os.remove("data.txt")
        daform = ncity 
        dfile= open("data.txt","x")
        dfile.write(daform)
        dfile.close() 
        # tables
        temtable = table_show(table,date1,pred_MLP_1)

        return render_template('solar.html',  ttables=[final_table_solar(mcity, pred_MLP_1, temtable).to_html(classes='data" id = "t1')], idcity=idcity)
    else:
        idcity = 12
        return render_template('solar.html', idcity=idcity)
    

@app.route('/shistdata', methods=["GET", "POST"])
def shistdata():
    return render_template('shistdata.html')

@app.route('/shistwind', methods=["GET", "POST"])
def shistwind():
    return render_template('shistwind.html')

@app.route("/pdf1", methods=["GET", "POST"])
def index():
    etable = tenergy_month()
    ttable = tmonth_meanT()
    template = render_template("comsup_pdf.html", etables=[etable.to_html(classes='data" id = "t1')], ttables=[ttable.to_html(classes='data" id = "t2')])
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    #config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    # para ubuntu elpath es /usr/bin/wkhtmltopdf'
    pdfkit.from_string(template, 'comsuption.pdf', configuration=config)
    return send_from_directory('', 'comsuption.pdf')


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0')

# correr app => source myprojectenv/bin/activate