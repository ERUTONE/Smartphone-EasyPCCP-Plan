print("host importing...")

import os
import importlib.util
import main.globals as g

actions = {}

def import_all_modules_from_dir(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            file_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            globals()[module_name] = module

import_all_modules_from_dir(g.functions)

def add_action(name, action): 
    global actions
    actions[name] = action # module.function(args)

def load_actions():
    print("loading actions...")
    global actions
    
    for name, action in actions.items():
        print(f" - loading action {name}() : {action}")
        exec(f"def {name}(): {action}", globals())

