from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import pythoncom

def add_application_volume(app, change): 
    # app: アプリケーション名（拡張子を含む）、change: 音量の変更量（%）

    pythoncom.CoInitialize()

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        process = session.Process
        if process and process.name().lower() == app.lower():
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            
            is_muted = volume.GetMute()
            print(f"{app} Current Mute State: {is_muted}")
            
            if is_muted:
                volume.SetMute(0, None)
                print(f"{app} has been unmuted.")

            current_volume = volume.GetMasterVolume()
            new_volume = max(0.0, min(1.0, current_volume + change / 100.0))
            volume.SetMasterVolume(new_volume, None)
            print(f"{app} Current Volume: {current_volume}")
            print(f"{app} New Volume: {new_volume}")
            return

    pythoncom.CoUninitialize()


# ----------------------------------------------------------- #


def set_application_volume(app, value):
    # app: アプリケーション名（拡張子を含む）、value: 設定する音量（%）

    pythoncom.CoInitialize()

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        process = session.Process
        if process and process.name().lower() == app.lower():
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            
            is_muted = volume.GetMute()
            print(f"{app} Current Mute State: {is_muted}")
            
            if is_muted:
                volume.SetMute(0, None)
                print(f"{app} has been unmuted.")
            
            new_volume = max(0.0, min(1.0, value / 100.0))
            volume.SetMasterVolume(new_volume, None)
            print(f"{app} New Volume: {new_volume}")
            return

    pythoncom.CoUninitialize()


# ----------------------------------------------------------- #


def toggle_application_volume(app):
    # app: アプリケーション名（拡張子を含む）

    pythoncom.CoInitialize()

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        process = session.Process
        if process and process.name().lower() == app.lower():
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)

            is_muted = volume.GetMute()
            print(f"{app} Current Mute State: {is_muted}")
            
            volume.SetMute(not is_muted, None)
            print(f"{app} Mute state has been toggled to: {not is_muted}")
            return

    pythoncom.CoUninitialize()


# ----------------------------------------------------------- #


def get_application_volume_mute(app):
    # app: アプリケーション名（拡張子を含む）

    pythoncom.CoInitialize()

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        process = session.Process
        if process and process.name().lower() == app.lower():
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            current_volume = volume.GetMasterVolume()
            current_volume_percent = int(current_volume * 100)
            print(f"{app} Current Volume: {current_volume_percent}%")
            return current_volume_percent

    # Program end: uninitialize COM library
    pythoncom.CoUninitialize()

    # Return None if the application is not found
    return None

# Example usage:
volume = get_application_volume("chrome.exe")
if volume is not None:
    print(f"Chrome current volume is {volume}%")
else:
    print("Chrome is not running or was not found.")



# ----------------------------------------------------------- #

