print("client importing...")
import os, json, regex as re
from flask import render_template, request, jsonify
from app import app
import main.globals as g
import main.host.src.host as host

layout_name = ""
theme_name = ""
theme_path = ""
layout_widgets = []
widget_styles = []
widgets_html = ""

def load_usercfg():
    global layout_name, theme_name

    with open(g.usercfg, "r", encoding='utf-8') as f:
        _usercfg = json.load(f)
        layout_name = _usercfg["layout"]
        theme_name = _usercfg["theme"]

def set_layout(arg = "default"):
    global layout_name
    if type(arg) == str: layout_name = arg
    elif type(arg) == int:
        with open(g.usercfg, "r", encoding='utf-8') as f:
            _usercfg = json.load(f)
            _group = _usercfg["layout_group"]
            if arg < len(_group) and arg >= 0:
                layout_name = _group[arg]
    return "reload"

layout_group_count = 0
def rotate_layout(arg = 1): # change
    global layout_name, layout_group_count
    with open(g.usercfg, "r", encoding='utf-8') as f:
        _usercfg = json.load(f)
        _group = _usercfg["layout_group"]
        _len = len(_group)
    # get current layout
    if layout_name in _group:
        layout_group_count = _group.index(layout_name)
    layout_group_count = (layout_group_count + arg) % _len
    layout_name = _group[layout_group_count]
    return "reload"

def get_layout():
    global layout_name, layout
    
    _path = g.c_layout + layout_name + ".json"
    if(os.path.exists(_path)) :
        with open(_path, "r", encoding='utf-8') as f:
            return json.load(f)
        
    
    _path = g.layout + layout_name + ".json"
    if(not os.path.exists(_path)) : 
        print("[ERROR] layout not found: " + _path)
        _path = g.layout_default + ".json"
    
    with open(_path, "r", encoding='utf-8') as f:
        return json.load(f)

def set_theme(arg = "default"):
    global theme_name
    theme_name = arg
    return "reload"

def get_theme():
    global theme_name, theme_path
    
    _path = g.c_theme + theme_name + ".css"
    if(os.path.exists(_path)) :
        theme_path = _path
        return
    
    _path = g.theme + theme_name + ".css"
    if(not os.path.exists(_path)) : 
        print("[ERROR] theme not found: " + _path)
        _path = g.theme_default + ".css"
        
    theme_path = _path

from main.client.src.widget import widget as new_widget
def create_widgets():
    global layout_name
    layout = get_layout()
    with open(g.template+"grid.html", "w", encoding='utf-8') as f:
        f.write('<!-- Auto generated html -->\n')
        for i in range(len(layout["placement"]) ):
            jwidget = layout["placement"][i]
            widget_path = g.widget + jwidget["widget"] + ".json"
            if(os.path.exists(widget_path)):
                # load as a new instance
                print(f' - loading widget {jwidget["widget"]}...')
                _widget = new_widget(widget_path, i)
                f.write( _widget.create_widget() )
                widget_styles.append( _widget.get_style() )
            else:
                print("[ERROR] widget not found: " + widget_path)
                f.write(f"<div>ERROR: widget {jwidget} not found</div>")
                widget_styles.append("")

def create_gridcss():
    layout = get_layout()
    with open(g.template+"grid.css", "w", encoding='utf-8') as f:
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

def init():

    # get_layout()
    get_theme()
    
    host.clear_actions()
    global layout_widgets; layout_widgets= []
    global widget_styles;  widget_styles = []
    create_widgets()
    create_gridcss()
    global widgets_html; widgets_html = "\n".join(layout_widgets)
    host.merge_onload_js()

# regen when py (re)starts
load_usercfg()
init()

@app.route("/")
def show_interface():
    init()
    
    global widgets_html, theme_path
    return render_template("base.html",theme=theme_path)

@app.route("/action", methods=["POST"])
def action():
    
    print(f" ! got POST with arg {request.get_json()}")
    returns = {}
    for key, value in request.get_json().items():
        returns[key] = host.execute_action(key, value) 

    return jsonify(returns)