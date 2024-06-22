#!/usr/bin/env python3
print("starting app..")
import json
from flask import Flask
import main.globals as g


app = Flask(__name__,
    static_folder=g.home, # if not g.home.endswith("/") else g.home+"/",
    template_folder=g.template)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def load_cores():
    import main.host.src.host
    import main.client.src.client


with open(g.usercfg) as f:
    config = json.load(f)

    if "host" in config:
        host_ip = config["host"]
    else:
        host_ip = "0.0.0.0"
load_cores()

app.run(host=host_ip, port=5000, debug=True)

