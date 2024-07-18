from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Audio endpoint volume interfaceを取得
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def add_master_volume(change):         # ARG change = -100 to 100
    current_volume = get_master_volume()
    new_volume = min(max(current_volume + change, 0), 100)
    set_master_volume(new_volume)

def set_master_volume(level):          # ARG level = 0 to 100
    level = min(max(level, 0), 100)
    volume.SetMasterVolumeLevelScalar(level / 100, None)

def get_master_volume():               # RETURN 0 to 100
    return int(volume.GetMasterVolumeLevelScalar() * 100)

def set_master_volume_mute(mute):      # ARG mute = True or False
    volume.SetMute(mute, None)

def toggle_master_volume_mute():       # RETURN True or False
    current_mute = get_master_volume_mute()
    set_master_volume_mute(not current_mute)
    return get_master_volume_mute()

def get_master_volume_mute():          # RETURN True or False
    return volume.GetMute() == 1