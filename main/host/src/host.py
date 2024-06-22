print("host importing...")

import os
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
onload_js_pathes = []

def add_onload_js_queue(path): # path to js
    if path.endswith(".js") and os.path.exists(path):
        onload_js_pathes.append(path)
    else:
        print(f"AddOnloadScriptQueue: invalid path: {path}")

def merge_onload_js():
    print("host: merging onload scripts...")
    with open(g.template+"script.js", "w") as f:
        for path in onload_js_pathes:
            with open(path, "r") as s:
                f.write(s.read())