import main.client.src.client as client_boss

def set_layout(arg = "default"):
    return client_boss.set_layout(arg)

def rotate_layout(arg = 1): # change
    return client_boss.rotate_layout(arg)

def set_theme(arg = "default"):
    return client_boss.set_theme(arg)

# ------------------ #

def load_usercfg():
    return client_boss.load_usercfg()

def generate_html():
    return client_boss.generate_html()