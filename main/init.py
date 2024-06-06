import os, json

def config():
    usercfg_path ="config/usercfg.json"
    if not os.path.isfile(usercfg_path):
        print("[INFO] Cannot find usercfg.json, creating default")
        # create usercfg.json
        with open("config/usercfg.json", "w") as f:
            json.dump({"layout":"default", "theme":"default"}, f, indent=4)
            f.close()
            
config()