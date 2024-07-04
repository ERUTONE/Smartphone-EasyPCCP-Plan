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


@app.route("/")
def show_interface():
    from main.client.src.client import generate_html, theme_path
    generate_html()
    return render_template("base.html",theme=theme_path)

@app.route("/action", methods=["POST"])
def action():
    
    print(f" ! got POST with arg {request.get_json()}")
    returns = {}
    from main.host.src.host import execute_action
    for key, value in request.get_json().items():
        returns[key] = execute_action(key, value) 

    return jsonify(returns)

app.run(host=host_ip, port=5000, debug=True)

