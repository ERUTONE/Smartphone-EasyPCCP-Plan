print("host importing...")

import os, regex as re
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
    
# ------------------ #
actions = {}

def add_action(name, action): # param : module.function(args)
    global actions
    actions[name] = action

def execute_action(name): # param
    import_all_modules()
    if name in actions:
        print(f" - executing {name} : {actions[name]} ...")
        namespace = {}
        try:
            exec(f"result = {actions[name]}", globals(), namespace)
        except Exception as e:
            print("   > execution failed: ",e)
        
        if "result" in namespace:
            return namespace["result"]
        else:
            return None
    else:
        print(f"action '{name}' not found")
        return None

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

def add_onload_js_queue(arg, type=None): # path to js / js code
    global onload_js
    if type == None:
        if is_valid_path(arg):
            type = "path"
        else:
            type = "code"
    
    if type == "path":
        if arg.endswith(".js") and os.path.exists(arg):
            onload_js.append({"type":"path", "path":arg})
        else:
            print(f"AddOnloadScriptQueue: invalid path: {arg}")
    elif type == "code":
        onload_js.append({"type":"code", "code":arg})
    else:
        print(f"AddOnloadScriptQueue: invalid type: {type}")

def merge_onload_js():
    global onload_js
    print("host: merging onload scripts...")
    # reset
    with open(g.template+"script.js", "w") as f:
        f.write("//auto-generated\n\n")
    with open(g.template+"script.js", "a") as f:
        for script in onload_js:
            if script["type"] == "path":
                print(f" - ({script['type']}) {script['path']}")
                with open(script["path"], "r") as js:
                    f.write(js.read())
            elif script["type"] == "code":
                print(f" - ({script['type']}) {script['code']}")
                f.write(script["code"])
            f.write("\n")