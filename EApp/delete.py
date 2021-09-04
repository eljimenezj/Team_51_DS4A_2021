
from pathlib import Path
import os

my_file = Path("/opt/eapp/file.text")
if my_file.is_file():
   print('existe')
   os.remove("/opt/eapp/file.text")
else:
   print('Nada')

def removg():
    my_file = Path("/opt/eapp/static/graphs/graphs1.html")
    ban = True
    while ban:
        if my_file.is_file():
            os.remove("/opt/eapp/static/graphs/graphs1.html")
            break
    plt_html = "<html><body></body></html>"
    Html_file = open("/opt/eapp/static/graphs/graphs1.html","x")
    Html_file.write(plt_html)
    Html_file.close()

def removgw():
    my_file = Path("/opt/eapp/static/graphs/graphw1.html")
    ban = True
    while ban:
        if my_file.is_file():
            os.remove("/opt/eapp/static/graphs/graphw1.html")
            break
    plt_html = "<html><body></body></html>"
    Html_file = open("/opt/eapp/static/graphs/graphw1.html","x")
    Html_file.write(plt_html)
    Html_file.close()

def rengraph(fig1,nom):
    plt_html = mpld3.fig_to_html(fig1, figid = 'fig1', no_extras= True, template_type='simple', use_http=False)
    Html_file= open("/opt/eapp/templates/"+nom+".html","w")
    Html_file.write(plt_html)
    Html_file.close()
    return Html_file;