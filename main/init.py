import os, json, logging, gc

def config():
    usercfg_path ="config/usercfg.json"
    if not os.path.isfile(usercfg_path):
        print("[INFO] Cannot find usercfg.json, creating default")
        # create usercfg.json
        with open("config/usercfg.json", "w") as f:
            json.dump({"layout":"default", "theme":"default"}, f, indent=4)
            
config()

# Werkzeugのロガーを無効化
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# ガベージコレクションのデバッグ情報
gc.set_debug(gc.DEBUG_STATS)