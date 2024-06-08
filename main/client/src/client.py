print("client importing...")
import os, json, regex as re
from flask import render_template, request
from app import app
import main.globals as g

layout_name = ""
theme_name = ""
layout: dict
theme_path = ""
widgets = []

def load_usercfg():
    global layout_name, theme_name

    with open("config/usercfg.json", "r") as f:
        _usercfg = json.load(f)
        layout_name = _usercfg["layout"]
        theme_name = _usercfg["theme"]

def get_layout():
    global layout_name, layout
    
    _path = g.layout + layout_name + ".json"
    if(not os.path.exists(_path)) : 
        print("[ERROR] layout not found: " + _path)
        _path = g.layout_default
    
    with open(_path, "r") as f:
        layout = json.load(f)

def get_theme():
    global theme_name, theme_path
    _path = g.theme + theme_name + ".css"
    if(not os.path.exists(_path)) : 
        print("[ERROR] theme not found: " + _path)
        _path = g.theme_default
        
    theme_path = _path

from main.client.src.widget import create_widget
def create_widgets():
    global layout, widgets
    print(type(layout["placement"]))
    for i in range(len(layout["placement"]) ):
        jwidget = layout["placement"][i]
        widget_path = g.widget + jwidget["widget"] + ".json"
        if(os.path.exists(widget_path)):
            print(widget_path)
            widgets.append( create_widget(widget_path, i) )
        else:
            print("[ERROR] widget not found: " + widget_path)
            widget_path = g.widget_default

def create_grid():
    global layout
    grid_col = layout["grid"][0]
    grid_row = layout["grid"][1]
    # 
    with open(g.template+"grid.css", "w") as f:
        # TODO: .container
        f.write(f".container{{ \
            grid-template-columns : repeat({grid_col}, 1fr); \
            grid-template-rows : repeat({grid_row}, 1fr);\
            width: 90vw;\
            height: {90*grid_row/grid_col}vw;\
            max-width: {90*grid_col/grid_row}svh;\
            max-height: 90svh;\
            }}\n")
        # TODO: .widget
        for i in range(len(layout["placement"])):
            jwidget = layout["placement"][i]
            _scale = [int(n) for n in re.findall(r"(\d+)", jwidget["widget"])[-2:]]
            f.write(f".widget#w{i}{{ \
                grid-column: {jwidget['position'][0]}/{jwidget['position'][0]+_scale[0]}; \
                grid-row: {jwidget['position'][1]}/{jwidget['position'][1]+_scale[1]}; \
                }}\n")
    
# -------------------------------- #

def init() :

    load_usercfg()

    get_layout()
    get_theme()
    global widgets; widgets= []
    create_widgets()
    create_grid()

init()

@app.route("/")
def show_interface():
    if "reload" in request.args:
        init()
    return render_template("base.html",theme=theme_path, content="\n".join(widgets))