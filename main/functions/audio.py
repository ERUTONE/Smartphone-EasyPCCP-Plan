import subprocess, json

def get_audio_devices():
    # PowerShell 実行ファイルのパス
    powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    script_path = r"backend\Get_Audio_Devices.ps1"
    # コマンドを構成・実行   
    command = [powershell_path, '-File', script_path]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def set_audio_device(arg, by = "uuid"): # by = "uuid" or "name"
    from main.functions._audio.Switched_Audio_Devices import set_audio_device as function
    return function(arg, by)    
        
def set_master_volume(value):
    from main.functions._audio.master_volume import set_master_volume as function
    function(value)

def add_master_volume(change):
    from main.functions._audio.master_volume import add_master_volume as function
    function(change)
    
def toggle_master_volume_mute():
    from main.functions._audio.master_volume import toggle_master_volume_mute as function
    function()

def set_application_volume(app, value):
    from main.functions._audio.application_volume import set_application_volume as function
    function(app, value)

def add_application_volume(app, change):
    from main.functions._audio.application_volume import add_application_volume as function
    function(app, change)

def toggle_application_volume(app):
    from main.functions._audio.application_volume import toggle_application_volume as function
    function(app)

def get_application_volume_mute(app):
    from main.functions._audio.application_volume import get_application_volume_mute as function
    return function(app)

