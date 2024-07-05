print("host importing...")

import os, importlib.util, ast, inspect
import regex as re
import main.globals as g

modules = {}

def import_modules_from_directory(directory):
    print(f"host: importing all modules from {directory}...")
    modules = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            file_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            functions = {name: item for name, item in module.__dict__.items() if inspect.isfunction(item) and not name.startswith('__')}
            modules[module_name] = functions
            print(f'  > {"{:<15}".format(module_name)} : {len(functions)} functions')
    return modules

def import_all_modules():
    global modules
    if len(modules)>0 : return
    else: modules = import_modules_from_directory(g.functions)

def execute_module_function(call_string):
    match = re.match(r'(\w+)\.(\w+)\((.*)\)', call_string)
    if not match:
        raise ValueError(f" !> {call_string}: Invalid call string format")
    
    module_name, function_name, args_str = match.groups()
    del match
    
    global modules
    if module_name in modules and function_name in modules[module_name]:
        func = modules[module_name][function_name]
        
        args = parse_arguments(args_str)
        try:
            return func(*args)
        except Exception as e:
            raise ValueError(f" !> Function call failed: {module_name}.{function_name}({args_str})") from e
    else:
        raise ValueError(f"Module or function not found: {module_name}.{function_name}")

def parse_arguments(args_str):
    if not args_str.strip():
        return []
    
    try:
        args = ast.literal_eval(f'[{args_str}]')
    except (ValueError, SyntaxError) as e:
        raise ValueError(f" !> Failed to parse arguments {args_str}: {e}")
    
    return args

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
        return execute_module_function(action)
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
    return execute_module_function(function)
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

