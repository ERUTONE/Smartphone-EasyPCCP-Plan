print("host importing...")

actions = {}

def add_action(name, action): 
    global actions
    actions[name] = action # module.function(args)
    
def load_actions():
    global actions
    print("loading actions...")