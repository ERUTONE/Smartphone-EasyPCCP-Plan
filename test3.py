from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pycaw.constants import eRender, eConsole
from pycaw.utils import AudioDeviceManager

def list_audio_devices():
    devices = AudioUtilities.GetSpeakers()
    return devices

def set_default_audio_device(device_id):
    device_manager = AudioDeviceManager()
    device_manager.SetDefaultAudioPlaybackDevice(device_id, eConsole)

def main():
    devices = list_audio_devices()
    print("Available audio devices:")
    for i, device in enumerate(devices):
        print(f"{i}: {device.FriendlyName}")

    choice = int(input("Select the device number to set as default: "))
    selected_device = devices[choice]
    set_default_audio_device(selected_device.id)
    print(f"Set default audio device to: {selected_device.FriendlyName}")

if __name__ == "__main__":
    main()
