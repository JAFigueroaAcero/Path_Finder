# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 15:02:35 2021

@author: Juan Antonio
"""

from bokeh.plotting import figure
from tornado.ioloop import IOLoop

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.server.server import Server
from bokeh.models import ColumnDataSource, Row
from bokeh.events import DoubleTap
from bokeh.models import Dropdown
from bokeh.models.widgets import Button
import main as m
import sys
coordList = []
coordListc = []

lined = []

lines = []

linesc = []
pos = []

posc = []
joining = 0

def md(doc):
    global ds
    global ds2
    global source
    global source2
    TOOLS = "tap"
    bound = 10
    
    p = figure(title='Path Finder',
               tools=TOOLS,width=700,height=700,
               x_range=(-bound, bound), y_range=(-bound, bound))
    
    source = ColumnDataSource(data=dict(x=[], y=[]))   
    p.circle(source=source,x='x',y='y',size=10) 
    
    r = p.multi_line(xs = [], ys = [], line_color = 'blue')
    
    source2 = ColumnDataSource(data=dict(x=[], y=[]))   
    p.circle(source=source2,x='x',y='y',color = 'red') 
    ds = r.data_source
    
    r2 = p.multi_line(xs = [], ys = [], line_color = 'red')
    ds2 = r2.data_source
    button = Button(label="Stop", button_type="success")
    button.on_click(button_callback)

    p.on_event(DoubleTap, callback)


    d = Dropdown(label='menu', menu=['dot', 'connector','erase','path', 'new_path'])
    
    d.on_click(handler)
    layout = Row(p,d,button)

    doc.add_root(layout)

#add a dot where the click happened
def callback(event):
    global joining
    global lined
    global lines
    global pos
    global linesc
    global posc
    global coordList
    global coordListc
    Coords=(event.x,event.y)
    if joining == 0:
        coordList.append(Coords) 
        source.data = dict(x=[i[0] for i in coordList], y=[i[1] for i in coordList])
    elif joining == 1:
        if len(coordList) >= 2:
            if len(lined) <= 1:
                lined.append(Coords)
            if len(lined) == 2:
                ldf = []
                for l in lined:
                    ldf.append(coordList[sdis(l)])
                if ldf not in lines and ldf[0] != ldf[1]:
                    lines.append([ldf[0],ldf[1]])
                    lined = []
                    xl = []
                    yl = []
                    for l in lines:
                        xloc = [i[0]for i in l]
                        yloc = [i[1] for i in l]
                        xl.append(xloc)
                        yl.append(yloc)
                    ds.data = dict(xs=xl, ys=yl)
                else:
                    lined = []
    elif joining == 2:
        x = sdis(Coords)
        e = coordList.pop(x)
        lc = lines.copy()
        for l in lines:
            if e in l:
                lc.pop(lc.index(l))
        lines = lc
        xl = []
        yl = []
        for l in lines:
            xloc = [i[0] for i in l]
            yloc = [i[1] for i in l]
            xl.append(xloc)
            yl.append(yloc)
        ds.data = dict(xs=xl, ys=yl)
        source.data = dict(x=[i[0] for i in coordList], y=[i[1] for i in coordList])
        
    elif joining == 3:
        if len(pos) <= 1:
            pos.append(coordList[sdis(Coords)])
            source2.data = dict(x=[i[0] for i in pos], y=[i[1] for i in pos])
        else:
            pos = []
            source2.data = dict(x=[i[0] for i in pos], y=[i[1] for i in pos])
            ds2.data = dict(xs = [], ys = [])
        if len(lines) >= 1 and len(pos) == 2:
            final_l = [[c,[]] for c in coordList]
            for n,l in enumerate(lines):
                for o,val in enumerate(l):
                    final_l[coordList.index(val)][1].append(l[o-1])
          #  print (dict(final_l))
            ps = m.main(dict(final_l),pos[0],pos[1])
            xss = []
            yss = []
            for el in ps:
                xloc = []
                yloc = []
                for e in el:
                    xloc.append(e[0])
                    yloc.append(e[1])
                xss.append(xloc)
                yss.append(yloc)
            ds2.data = dict(xs=xss, ys=yss)
    elif joining == 4:
        if len(posc) <= 1:
            distances = []
            mps = []
            if coordListc == []:
                linesc = lines.copy()
            for l in linesc:
                if l[1][0] - l[0][0] != 0:
                    mp = (l[1][1] - l[0][1])/(l[1][0] - l[0][0])
                    mps.append(mp)
                    distances.append(abs((Coords[0] * mp - Coords[1] + (l[0][1] - l[0][0] * mp))/((mp**2 + 1)**0.5)))
                else:
                    mps.append(None)
                    distances.append(abs(l[1][1] - Coords[1]))
                    
            dindex = distances.index(min(distances))
            
            
            # Agregar comprobación si el punto se sale de los límites del mínimo y máximo
            # En caso de salir del limite omitir todo el proceso
            # Quizá un posterior ir a la siguiente distancia
    #        print(dindex)
            ldata = linesc[dindex]
            mp = mps[dindex]
            mag = m.magnitud(ldata[0], ldata[1])
            if  mag > m.magnitud(ldata[0], Coords) and mag > m.magnitud(ldata[1], Coords):
                if mp != None:
                    b = Coords[1] - Coords[0]/mp
                    c = ldata[0][1] - mp * ldata[0][0]
                    x = (mp * (b - c))/(mp**2 - 1)
                    y = x/mp + b
                else:
                    x = Coords[0]
                    y = ldata[1][1]
                
                if coordListc == []:
                    coordListc = coordList.copy() + [(x,y)]
                else:
                    coordListc += [(x,y)]
                for p in ldata:
                    loc = [p,(x,y)]
                    linesc.append(loc)
                  #  print(loc)
                    
                linesc.pop(linesc.index(ldata))
           #     print(linesc)
                
                xl = []
                yl = []
                
                for l in linesc:
                    xloc = [i[0] for i in l]
                    yloc = [i[1] for i in l]
                    xl.append(xloc)
                    yl.append(yloc)
                posc.append((x,y))
                ds.data = dict(xs=xl, ys=yl)
                source.data = dict(x=[i[0] for i in coordListc], y=[i[1] for i in coordListc])
                source2.data = dict(x=[i[0] for i in posc], y=[i[1] for i in posc])
        else:
            posc = []
            coordListc = []
            source2.data = dict(x=[i[0] for i in posc], y=[i[1] for i in posc])
            source.data = dict(x=[i[0] for i in coordList], y=[i[1] for i in coordList])
            ds2.data = dict(xs = [], ys = [])
            xl = []
            yl = []
            
            for l in lines:
                xloc = [i[0] for i in l]
                yloc = [i[1] for i in l]
                xl.append(xloc)
                yl.append(yloc)
            ds.data = dict(xs=xl, ys=yl)
        if len(linesc) >= 1 and len(posc) == 2:
            final_l = [[c,[]] for c in coordListc]
            for n,l in enumerate(linesc):
                for o,val in enumerate(l):
                    final_l[coordListc.index(val)][1].append(l[o-1])
     #       print(dict(final_l))
     #       print(posc[0])
     #       print(posc[1])
            
            ps = m.main(dict(final_l),posc[0],posc[1])
            xss = []
            yss = []
            for el in ps:
                xloc = []
                yloc = []
                for e in el:
                    xloc.append(e[0])
                    yloc.append(e[1])
                xss.append(xloc)
                yss.append(yloc)
            ds2.data = dict(xs=xss, ys=yss)
            

def handler(event):
    global joining
    if event.item == 'dot':
        joining = 0
    elif event.item == 'connector':
        joining = 1
    elif event.item == 'erase':
        joining = 2
    elif event.item == 'path':
        joining = 3
    else:
        joining = 4
    print(joining)
def button_callback():
    sys.exit()

def sdis(loc):
    global coordList
    distances = []
    for c in coordList:
        distances.append(m.magnitud(loc, c))
    return distances.index(min(distances))
    
        
def main():
    """Launch the server and connect to it.
    """
    
    print("Preparing a bokeh application.")
    io_loop = IOLoop.current()
    bokeh_app = Application(FunctionHandler(md))

    server = Server({"/": bokeh_app}, io_loop=io_loop)
    server.start()
    print("Opening Bokeh application on http://localhost:5006/")

    io_loop.add_callback(server.show, "/")
    io_loop.start()

if __name__ == "__main__":
    main()