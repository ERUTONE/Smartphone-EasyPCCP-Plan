import os
import pyautogui
from datetime import datetime

def get_user_directory():
    # ユーザーディレクトリのパスを取得する関数
    return os.path.expanduser('~')

def timestamped_filename(ext, name = ""):
    # 現在の日時を使用してファイル名を生成
    current_time = datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d %H-%M-%S')
    return f'{name+" "if name!="" else ""}{timestamp}{ext}'

def get_screenshot_folder():
    user_directory = get_user_directory()
    
    if os.name == 'nt':  # Windowsの場合
        return os.path.join(user_directory, 'Pictures', 'Screenshots')
    else:  # macOSの場合
        return os.path.join(user_directory, 'Desktop')
