print("client importing...")
import os, json
from flask import render_template
from app import app
import main.globals as g

layout_name = ""
theme_name = ""
layout: dict
theme_path = ""

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

def create_grid():
    global layout
    grid_col = layout["grid"][0]
    grid_row = layout["grid"][1]
    with open(g.template+"grid.css", "w") as f:
        # TODO: .container
        f.write(f".container{{ \
            grid-template-columns : repeat({grid_col}, 1fr); \
            grid-template-rows : repeat({grid_row}, 1fr);\
            }}")
            # TODO: size
        # TODO: .widget
        ...
    
# -------------------------------- #

load_usercfg()

get_layout()
get_theme()
create_grid()

@app.route("/")
def show_interface():
    return render_template("base.html",theme=theme_path)