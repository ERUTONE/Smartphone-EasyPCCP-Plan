print("host importing...")

import os
import importlib.util
import main.globals as g

actions = {}
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
            print(module_name, end=", ")
    print()


def import_all_modules():
    global modules_imported
    if modules_imported : return
    else: modules_imported = True

    import_all_modules_from_dir(g.functions)
    
# ------------------ #

def add_action(name, action): 
    global actions
    actions[name] = action # module.function(args)

def execute_function(function):
    import_all_modules()
    namespace = {}
    try:
        print(f" - executing {function} ...")
        exec(function)
    except Exception as e:
        print(f"  > execution failed")
        print(e)
    if "result" in namespace:
        return namespace["result"]
    else:
        return None

def execute_action(name):
    import_all_modules()
    if name in actions:
        print(f" - executing {name} : {actions[name]} ...")
        try:
            exec(actions[name])
        except Exception as e:
            print("   > execution failed")
            print(e)
    else:
        print(f"action '{name}' not found")