from pycaw.pycaw import AudioUtilities

devices = AudioUtilities.GetAllDevices()
for device in devices:
    print(device.FriendlyName)
