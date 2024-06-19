#!/usr/bin/env python3
print("starting app..")

from flask import Flask


app = Flask(__name__,
    static_folder='/',
    template_folder='main/client/src/template/')
app.config['TEMPLATES_AUTO_RELOAD'] = True

def load_cores():
    import main.client.src.client
    import main.host.src.host
    
load_cores()
app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
