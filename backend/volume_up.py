from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# 音量コントロールのためのインターフェースを取得
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# 音量を上げる（0.0から1.0の範囲で設定）
volume.SetMasterVolumeLevelScalar(0.5, None)
