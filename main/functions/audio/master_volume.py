from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

def add_master_volume(change): # -100 ~ 100 int
    # スピーカーデバイスの取得
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # 現在のミュート状態を取得
    is_muted = volume.GetMute()
    print("Current Mute State:", is_muted)
    
    if is_muted:
        # ミュートを解除する
        volume.SetMute(0, None)
        print("Mute has been turned off.")
    else:
        # 現在の音量を取得（0.0から1.0の範囲）
        current_volume = volume.GetMasterVolumeLevelScalar()
        print("Current volume: %f" % current_volume)
        
        # 音量を変更する（1.0を超えないようにする、0.0未満にならないようにする）
        adjustment = change / 100.0
        new_volume = max(0.0, min(1.0, current_volume + adjustment))
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        print("New volume: %f" % new_volume)

# ------------------- #

def set_master_volume(value): # 0~100 int

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    adjustment = value / 100.0
    volume.SetMasterVolumeLevelScalar(adjustment, None)



# ------------------- #

def toggle_master_volumea():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    is_muted = volume.GetMute()
    print("Current Mute State:", is_muted)
    
    volume.SetMute(not is_muted, None)
    print("Mute state has been toggled.")
    
# ------------------- #