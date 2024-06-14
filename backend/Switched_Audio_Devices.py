import subprocess

# PowerShell 実行ファイルのパス
powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"

# 実行する PowerShell スクリプトのパス
script_path = r"backend\Switched_Audio_Devices.ps1"

# スクリプトに渡す引数
script_arg = r"{51576283-45ac-44a4-8252-a4dba0948c0f}"

# コマンドを構成
command = [powershell_path, '-File', script_path, script_arg]

# コマンドを実行
result = subprocess.run(command, capture_output=True, text=True)

# ! Notification

# pyを実行する前に、実行権限を与える必要がある
# Windows Powershellを管理者権限で開き、以下のコマンドを実行する。
# Set-ExecutionPolicy RemoteSigned
# メッセージが表示され入力を促されたら、「Y」で続行する。
# これで準備は完了