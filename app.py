#!/usr/bin/env python3
print("starting app..")

from flask import Flask,request,render_template
from jinja2 import FileSystemLoader
import os, datetime
import importlib.util
from json import loads,dumps,load


app = Flask(__name__, static_folder='/', template_folder='main/client/src/template/')
app.config['TEMPLATES_AUTO_RELOAD'] = True

def import_all_modules_from_dir(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            file_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            globals()[module_name] = module

def load_cores():
    import main.client.src.client
    import main.host.src.host
    
load_cores()
app.run(host='0.0.0.0', port=5000, debug=True)