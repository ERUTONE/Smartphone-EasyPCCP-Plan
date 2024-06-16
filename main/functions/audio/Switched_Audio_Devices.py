import subprocess, json

def set_audio_device(arg, by = "uuid"): # by = "uuid" or "name"
    # PowerShell 実行ファイルのパス
    powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    script_path = r"backend\Switched_Audio_Devices.ps1"
    
    # スクリプトに渡す引数
    if by == "uuid":
        script_arg = arg
        print(f"* Switch to audio device uuid {arg}")
    elif by == "name":
        with open("config/usercfg.json", "r") as f:
            _usercfg = json.load(f)
            _audio_devices = _usercfg["audio_devices"] if "audio_devices" in _usercfg else {}
            if arg in _audio_devices:
                if "uuid" in _audio_devices[arg]:
                    script_arg = _audio_devices[arg]["uuid"]
                    print(f"* Switch to audio device name '{arg}' - {script_arg}")
                else:
                    raise ValueError(f"Audio device name '{arg}' has no 'uuid' in usercfg.json")
            else:
                raise ValueError(f"Audio device name '{arg}' not found in usercfg.json")
    else:
        raise ValueError("by-arg must be 'uuid' or 'name'")

    # コマンドを構成・実行
    command = [powershell_path, '-File', script_path, script_arg]
    
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    # 呼び出し方例
    # by="uuid" あるいはby指定なしの場合は、uuidを直接指定する
    # by="name"での指定では、usercfg.jsonのaudio_devicesに登録されているデバイス名を指定する
    print(set_audio_device("koral_speaker", by="name"))

# ! Notification

# pyを実行する前に、実行権限を与える必要がある
# Windows Powershellを管理者権限で開き、以下のコマンドを実行する。
# Set-ExecutionPolicy RemoteSigned
# メッセージが表示され入力を促されたら、「Y」で続行する。
# これで準備は完了