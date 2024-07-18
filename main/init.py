import os, json, logging, gc

def config():
    usercfg_path ="config/usercfg.json"
    if not os.path.isfile(usercfg_path):
        print("[INFO] Cannot find usercfg.json, creating default")
        # create usercfg.json
        with open(usercfg_path, "w") as f:
            json.dump({"layout":"default", "theme":"default"}, f, indent=4)
            
config()

# log
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# logging.basicConfig(level=logging.DEBUG)
# gc.set_debug(gc.DEBUG_STATS)
