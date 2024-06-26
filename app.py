#!/usr/bin/env python3
print("starting app..")
import json, logging
from flask import Flask
import main.globals as g

import main.init

app = None

if (__name__ == "__main__"):
    
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
    
    # Werkzeugのロガーを無効化
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    from main.host.src.host import request_module
    app.register_blueprint(request_module)

    app.run(host=host_ip, port=5000, debug=True)

