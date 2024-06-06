print("client importing...")
from app import app
import main.globals as g
import os, json

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
        f.close()

def get_layout():
    global layout_name, layout
    
    _path = g.layout + layout_name + ".json"
    if(not os.path.exists(_path)) : 
        print("[ERROR] layout not found: " + _path)
        _path = g.layout_default
    
    with open(_path, "r") as f:
        layout = json.load(f)
        f.close()

def get_theme():
    global theme_name, theme_path
    _path = g.theme + theme_name + ".css"
    if(not os.path.exists(_path)) : 
        print("[ERROR] theme not found: " + _path)
        _path = g.theme_default
        
    theme_path = _path

# -------------------------------- #

load_usercfg()

get_layout()
get_theme()