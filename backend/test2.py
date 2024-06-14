import subprocess
import time
import pyautogui
# import os
# import signal

# Discordの実行ファイルパスを指定します
discord_path = r"C:\Users\n1230084.STCN2\AppData\Local\Discord\Update.exe"

# Discordをバックグラウンドで起動
subprocess.Popen([discord_path])

# Discordが起動するのを待つ（適宜調整）
time.sleep(1)

# 特定のキーボード入力を送信
# 例として、Ctrl+Shift+Iを送信（Discordの開発者ツールを開くショートカット）
pyautogui.hotkey('ctrl', 'shift', 'm')

# os.kill(process.pid, signal.SIGTERM)