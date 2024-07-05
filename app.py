#!/usr/bin/env python3
print("starting app..")
import json
from flask import Flask
from flask import render_template, request, jsonify

import main.globals as g
import main.init


app = Flask(__name__,
    static_folder=g.home, # if not g.home.endswith("/") else g.home+"/",
    template_folder=g.template)
app.config['TEMPLATES_AUTO_RELOAD'] = True

with open(g.usercfg) as f:
    config = json.load(f)

    if "host" in config:
        host_ip = config["host"]
    else:
        host_ip = "0.0.0.0"


from main.client.src.client import generate_html
@app.route("/")
def show_interface():
    generate_html()
    from main.client.src.client import theme_path, layout_name
    
    return render_template("base.html",theme=theme_path, layout=layout_name)


from main.host.src.host import execute_action
from main.client.src.client import set_layout
@app.route("/action", methods=["POST"])
def action():
    params = request.get_json()
    if "layout" in params:
        regen = set_layout(params["layout"])
        del params["layout"]
        if regen: generate_html()
    
    returns = {}
    for key, value in params.items():
        returns[key] = execute_action(key, value) 

    return jsonify(returns)


app.run(host=host_ip, port=5000, debug=False)

