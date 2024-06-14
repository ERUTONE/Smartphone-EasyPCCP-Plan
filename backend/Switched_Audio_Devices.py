import subprocess

# PowerShell 実行ファイルのパス
powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"

# 実行する PowerShell スクリプトのパス
script_path = r"C:\Users\n1230084.STCN2\Documents\githubクローン用ファイル\Smartphone-EasyPCCP-Plan\backend\Switched_Audio_Devices.ps1"

# スクリプトに渡す引数
script_arg = r"{51576283-45ac-44a4-8252-a4dba0948c0f}"

# コマンドを構成
command = [powershell_path, '-File', script_path, script_arg]

# コマンドを実行
result = subprocess.run(command, capture_output=True, text=True)
