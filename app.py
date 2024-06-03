#!/usr/bin/env python3


from flask import Flask,request,render_template
from json import loads,dumps,load
import datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def hello():
    if 'use_template' in request.args:
        dt_now = datetime.datetime.now()
        
        return render_template('index.html', clockString=dt_now.strftime('%Y-%m-%d %H:%M:%S'), div=render_template('testdiv.html'))
    else:
        my_dict = {
            "name": "user",
            "age": 25,
            "gender": "male",
            "hobbies": [
                "reading",
                "cooking",
                "sleeping"
            ]
        }
        return render_template('layout_prototype.html', my_dict=my_dict)

