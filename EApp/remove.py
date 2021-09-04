import os

def removg():
    ban = True
    while ban:
        if os.path.exists("static/graphs/graphs1.html"):
            os.remove("static/graphs/graphs1.html")
            ban = True
        else:
            ban = False

    plt_html = "<html><body></body></html>"
    Html_file= open("static/graphs/graphs1.html","x")
    Html_file.write(plt_html)
    Html_file.close()

def removgw():
    ban = True
    while ban:
        if os.path.exists("static/graphs/graphw1.html"):
            os.remove("static/graphs/graphw1.html")
            ban = True
        else:
            ban = False

    plt_html = "<html><body></body></html>"
    Html_file= open("static/graphs/graphw1.html","x")
    Html_file.write(plt_html)
    Html_file.close()