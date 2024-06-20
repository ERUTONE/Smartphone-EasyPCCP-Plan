print("client importing...")
import os, json, regex as re
from flask import render_template, request
from app import app
import main.globals as g
import main.host.src.host as host

layout_name = ""
theme_name = ""
layout: dict
theme_path = ""
layout_widgets = []
widget_styles = []
widgets_html = ""

def load_usercfg():
    global layout_name, theme_name

    with open("config/usercfg.json", "r") as f:
        _usercfg = json.load(f)
        layout_name = _usercfg["layout"]
        theme_name = _usercfg["theme"]

def get_layout():
    global layout_name, layout
    
    _path = g.c_layout + layout_name + ".json"
    if(os.path.exists(_path)) :
        with open(_path, "r") as f:
            layout = json.load(f)
        return
    
    _path = g.layout + layout_name + ".json"
    if(not os.path.exists(_path)) : 
        print("[ERROR] layout not found: " + _path)
        _path = g.layout_default
    
    with open(_path, "r") as f:
        layout = json.load(f)

def get_theme():
    global theme_name, theme_path
    
    _path = g.c_theme + theme_name + ".css"
    if(os.path.exists(_path)) :
        theme_path = _path
        return
    
    _path = g.theme + theme_name + ".css"
    if(not os.path.exists(_path)) : 
        print("[ERROR] theme not found: " + _path)
        _path = g.theme_default
        
    theme_path = _path

from main.client.src.widget import widget as new_widget
def create_widgets():
    global layout, layout_widgets
    for i in range(len(layout["placement"]) ):
        jwidget = layout["placement"][i]
        widget_path = g.widget + jwidget["widget"] + ".json"
        if(os.path.exists(widget_path)):
            # load as a new instance
            print(f' - loading widget {jwidget["widget"]}...')
            _widget = new_widget(widget_path, i)
            layout_widgets.append( _widget.create_widget() )
            widget_styles.append( _widget.get_style() )
        else:
            print("[ERROR] widget not found: " + widget_path)
            layout_widgets.append(f"ERROR: widget {jwidget} not found")
            widget_styles.append("")

def create_gridcss():
    global layout
    with open(g.template+"grid.css", "w") as f:
        # .container
        grid_col = layout["grid"][0]
        grid_row = layout["grid"][1]
        f.write(".container{ "+
            f"grid-template-columns : repeat({grid_col}, 1fr); "+
            f"grid-template-rows : repeat({grid_row}, 1fr); "+
             "width: 90vw; "+
            f"height: {90*grid_row/grid_col}vw; "+
            f"max-width: {90*grid_col/grid_row}svh; "+
             "max-height: 90svh; "+
            "}\n")
        # .widget
        for i in range(len(layout["placement"])):
            jwidget = layout["placement"][i]
            _scale = [int(n) for n in re.findall(r"(\d+)", jwidget["widget"])[-2:]]
            f.write(f"\n.widget#w{i}{{ " +
                f"grid-column: {jwidget['position'][0]}/{jwidget['position'][0]+_scale[0]}; " +
                f"grid-row: {jwidget['position'][1]}/{jwidget['position'][1]+_scale[1]}; " +
                "}\n")
            f.write(f".widget_title#w{i}-title{{ " +
                f"grid-column: {jwidget['position'][0]}/{jwidget['position'][0]+_scale[0]}; " +
                f"grid-row: {jwidget['position'][1]}/{jwidget['position'][1]+_scale[1]}; " +
                "}\n")
        f.write("\n".join(widget_styles))
    
# -------------------------------- #

def init(get_args=False, regen=False) :

    load_usercfg()
    if get_args:
        if "layout" in request.args:
            global layout_name; layout_name=request.args.get("layout")
            regen = True
        if "theme" in request.args:
            global theme_name; theme_name=request.args.get("theme")
    get_layout()
    get_theme()
    
    if regen:
        global layout_widgets; layout_widgets= []
        global widget_styles;  widget_styles = []
        create_widgets()
        create_gridcss()
        global widgets_html; widgets_html = "\n".join(layout_widgets)

# regen when py (re)starts
init(regen=True)

@app.route("/")
def show_interface():
    init(get_args=True)
    
    print(f"got request with {len(request.args)} arguments")
    for key in request.args:
        if(key=="reload"): init(regen=True, get_args=True)
        host.execute(key)
    
    global widgets_html
    return render_template("base.html",theme=theme_path, content=widgets_html)