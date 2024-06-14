from ctypes import windll

def runas():

    windll.shell32.ShellExecuteW(
        None,
        "runas",
        "pythonw", # コンソール出したくないならpythonw
        "Switched_Audio_Devices.py", # 実行したいスクリプト
        None,
        0
        )

if __name__ == "__main__":
    runas()
