print("host importing...")

import os, importlib, ast
import regex as re
import main.globals as g

modules = {}

def import_modules_from_directory(directory):
    print(f"host: importing all modules from {directory}...")
    modules = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = importlib.import_module(module_name)
            functions = {name: item for name, item in module.__dict__.items() if callable(item) and not name.startswith('__')}
            modules[module_name] = functions
            print(f"> {module_name} : {[f'{k}, ' for k in functions.keys()[:5]]} {'\b\b...' if len(functions) > 5 else ''}")
    return modules

def import_all_modules():
    global modules
    if len(modules)>0 : return
    else: modules = import_modules_from_directory(g.functions)
import main.client.src.client as client

def execute_module_function(call_string):
    match = re.match(r'(\w+)\.(\w+)\((.*)\)', call_string)
    if not match:
        raise ValueError("Invalid call string format")
    
    module_name, function_name, args_string = match.groups()
    
    global modules
    if module_name in modules and function_name in modules[module_name]:
        func = modules[module_name][function_name]
        
        # ast.literal_eval to safely evaluate the arguments string
        args = ast.literal_eval(f"({args_string},)")
        
        return func(*args)
    else:
        raise ValueError("Module or function not found")


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
            return execute_module_function(action)
        except Exception as e:
            print(f"  > execution failed: ",e)
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
    try:
        return execute_module_function(function)
    except Exception as e:
        print(f"  > execution failed: ",e)
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

