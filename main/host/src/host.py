print("host importing...")

import os, regex as re
from flask import render_template, request, jsonify, Blueprint
import importlib.util
import main.globals as g

modules_imported = False

def import_all_modules_from_dir(directory):
    print(f"host: importing all modules from {directory}...")
    print("> loaded: ",end="")
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            file_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            globals()[module_name] = module
            print(module_name, end=" ")
    print()

def import_all_modules():
    global modules_imported
    if modules_imported : return
    else: modules_imported = True
    
    import_all_modules_from_dir(g.functions)
import main.client.src.client as client

    
# ------------------ #
actions = {}

def add_action(name, action): # param : module.function(args)
    global actions
    actions[name] = action

def clear_actions():
    global actions
    actions.clear()

def execute_action(name, arg=None): # param
    import_all_modules()
    if name in actions:
        namespace = {}
        action = actions[name]
        
        # arg
        if arg != None and arg != "":
            arg = convert_string(arg)
            namespace["arg"] = arg
            if type(arg) == str:
                action = action.replace("$", f'"{arg}"')
            else:
                action = action.replace("$", f"{arg}")
            
        
        # execute
        try:
            print(f" - executing {name} : {action} ...")
            exec(f"result = {action}", globals(), namespace)
        except Exception as e:
            print("   > execution failed: ",e)
        
        if "result" in namespace:
            return namespace["result"]
        else:
            return None
    else:
        print(f"action '{name}' not found")
        return None

# for private
def convert_string(s):
    try:
        # まず浮動小数点数に変換を試みる
        if '.' in s:
            return float(s)
        # 浮動小数点数が含まれていない場合、整数に変換を試みる
        return int(s)
    except ValueError:
        # 数値に変換できない場合は文字列のまま返す
        return s

def execute_function(function): # module.function(args)
    import_all_modules()
    namespace = {}
    try:
        print(f" - executing {function} ...")
        exec(f"result = {function}", globals(), namespace)
    except Exception as e:
        print(f"  > execution failed: ",e)
    
    if "result" in namespace:
        return namespace["result"]
    else:
        return None

# ------------------ #
onload_js = []

def is_valid_path(path):
    # パスの妥当性をチェックする正規表現
    pattern = r'^[a-zA-Z0-9_\-\/\.]+$'
    return bool(re.match(pattern, path))

def add_onload_js_queue(arg, type=None, static=False): # path to js / js code
    global onload_js
    if type == None:
        if is_valid_path(arg):
            type = "path"
        else:
            type = "code"
    
    if type == "path":
        if arg.endswith(".js") and os.path.exists(arg):
            onload_js.append({"type":"path", "path":arg , "static":static})
        else:
            print(f"AddOnloadScriptQueue: invalid path: {arg}")
    elif type == "code":
        onload_js.append({"type":"code", "code":arg, "static":static})
    else:
        print(f"AddOnloadScriptQueue: invalid type: {type}")

def clear_onload_js():
    global onload_js
    # delete only "non-static" scripts
    onload_js = [script for script in onload_js if script["static"]]

def merge_onload_js():
    global onload_js
    print("host: merging onload scripts...")
    # reset
    with open(g.template+"script.js", "w", encoding='utf-8') as f:
        f.write("//auto-generated\n\n")
    with open(g.template+"script.js", "a", encoding='utf-8') as f:
        for script in onload_js:
            if script["type"] == "path":
                print(f" - ({script['type']}) {script['path']}")
                with open(script["path"], "r", encoding='utf-8') as js:
                    f.write(js.read())
            elif script["type"] == "code":
                print(f" - ({script['type']}) {script['code']}")
                f.write(script["code"])
            f.write("\n")
    clear_onload_js()


# ------------------ #

request_module = Blueprint("host", __name__, url_prefix="/")

@request_module.route("/")
def show_interface():
    client.generate_html()
    
    from main.client.src.client import theme_path
    return render_template("base.html",theme=theme_path)

@request_module.route("/action", methods=["POST"])
def action():
    
    print(f" ! got POST with arg {request.get_json()}")
    returns = {}
    for key, value in request.get_json().items():
        returns[key] = execute_action(key, value) 

    return jsonify(returns)