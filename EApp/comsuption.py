import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mpld3
from mpld3 import plugins

df_cons = pd.read_csv('consumption.csv', delimiter=',')

def line_prepender(filename, line):
    with open(filename, 'a') as f:
        f.write("\n")
        f.write(line)
       

def tenergy_month():
    year_month_total = df_cons.groupby(["year_month"])["total"].mean()
    energy_month = pd.DataFrame(year_month_total).reset_index()
    energy_month.rename({"total": "Energy consumption [kWhs]", "year_month": "Year/Month"}, axis='columns', inplace=True)
    return energy_month

def graph_1():
    year_month_total = df_cons.groupby(["year_month"])["total"].mean()
    energy_month = pd.DataFrame(year_month_total).rename(columns={'total':'Energy Consumption [kWhs]'})
    em = energy_month.reset_index().rename(columns={'year_month':'Date'})
    em.Date.astype('str')
    fig1, ax = plt.subplots(figsize=(6.9, 3.8))
    points = plt.plot(em['Date'], em['Energy Consumption [kWhs]'], linewidth=2.0, linestyle='--', marker='o', markersize='7', color='b')
    plt.title('Total Consumption Over Time')
    plt.xlabel("Date")
    plt.ylabel("Energy Consumption [kWhs]")
    plt.grid(True, alpha=0.3)

    labels = []
    for i in range(len(em.Date)):
        label = em.Date[[i]].T
        label.columns = ['Row {0}'.format(i)]
        labels.append(str(label))
    
    plt.savefig('static/img/g1.png')
    plt_html = mpld3.fig_to_html(fig1, figid = 'fig1', no_extras= True, template_type='simple')
    
    Html_file= open("templates/graph1.html","w")
    Html_file.write(plt_html)
    Html_file.close()
    return Html_file

def tmonth_meanT():
    dict_month = {1: 'Jan', 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Ago", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dic"}
    month_meanT = df_cons.groupby(["month"])["total"].mean()
    month_meanT.rename(index=dict_month, inplace=True)
    month_meanT=pd.DataFrame(month_meanT).reset_index()
    mm = month_meanT.copy().rename(columns={'total':'Energy Consumption [kWhs]', 'month':'Month'})
    return mm

def graph_2():
    mm = tmonth_meanT()
    fig2, ax1 = plt.subplots(figsize=(6.5, 3.7))
    gf = ax1.bar(x=mm['Month'], height=mm['Energy Consumption [kWhs]'], width=0.8)
    plt.title('Mean Consumption by Month')
    plt.xlabel("Month")
    plt.ylabel("Energy Consumption [kWhs]")
    ax1.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.75)

    def gradientbars(bars):
        grad = np.atleast_2d(np.linspace(0,1,256)).T
        ax = bars[0].axes
        lim = ax.get_xlim()+ax.get_ylim()
        for bar in bars:
            bar.set_zorder(1)
            bar.set_facecolor("none")
            x,y = bar.get_xy()
            w, h = bar.get_width(), bar.get_height()
            ax.imshow(grad, extent=[x,x+w,y,y+h], aspect="auto", zorder=0)
        ax.axis(lim)
    gradientbars(gf)
    
    plt.savefig('static/img/g2.png')
    plt_html = mpld3.fig_to_html(fig2, figid = 'fig2', no_extras= True, template_type='simple')
    Html_file= open("templates/graph2.html","w")
    Html_file.write(plt_html)
    Html_file.close()
    return Html_file