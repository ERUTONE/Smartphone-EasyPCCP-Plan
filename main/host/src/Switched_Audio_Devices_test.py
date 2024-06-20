import ctypes

class ERole(ctypes.c_uint):
    eConsole = 0
    eMultimedia = 1
    eCommunications = 2
    ERole_enum_count = 3

class IPolicyConfig(ctypes.Structure):
    _fields_ = [
        ("GetMixFormat", ctypes.WINFUNCTYPE(ctypes.c_int)),
        ("GetDeviceFormat", ctypes.WINFUNCTYPE(ctypes.c_int)),
        ("ResetDeviceFormat", ctypes.WINFUNCTYPE(ctypes.c_int)),
        ("SetDeviceFormat", ctypes.WINFUNCTYPE(ctypes.c_int)),
        ("GetProcessingPeriod", ctypes.WINFUNCTYPE(ctypes.c_int)),
        ("SetProcessingPeriod", ctypes.WINFUNCTYPE(ctypes.c_int)),
        ("GetShareMode", ctypes.WINFUNCTYPE(ctypes.c_int)),
        ("SetShareMode", ctypes.WINFUNCTYPE(ctypes.c_int)),
        ("GetPropertyValue", ctypes.WINFUNCTYPE(ctypes.c_int)),
        ("SetPropertyValue", ctypes.WINFUNCTYPE(ctypes.c_int)),
        ("SetDefaultEndpoint", ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_wchar_p, ERole)),
        ("SetEndpointVisibility", ctypes.WINFUNCTYPE(ctypes.c_int))
    ]

class _CPolicyConfigClient(ctypes.Structure):
    _fields_ = []

class PolicyConfigClient:
    @staticmethod
    def SetDefaultDevice(device_id):
        _policyConfigClient = IPolicyConfig()
        try:
            ctypes.windll.ole32.CoCreateInstance(ctypes.byref(ctypes.c_wchar_p("{870AF99C-171D-4F9E-AF0D-E63DF40C2BC9}")), None, 1, ctypes.byref(ctypes.c_wchar_p("{F8679F50-850A-41CF-9C72-430F290290C8}")), ctypes.byref(_policyConfigClient))
            ctypes.windll.ole32.CoCreateInstance(ctypes.byref(ctypes.c_wchar_p("{F8679F50-850A-41CF-9C72-430F290290C8}")), None, 1, ctypes.byref(ctypes.c_wchar_p("{870AF99C-171D-4F9E-AF0D-E63DF40C2BC9}")), ctypes.byref(_policyConfigClient))
            ctypes.windll.ole32.CoCreateInstance(ctypes.byref(ctypes.c_wchar_p("{870AF99C-171D-4F9E-AF0D-E63DF40C2BC9}")), None, 1, ctypes.byref(ctypes.c_wchar_p("{F8679F50-850A-41CF-9C72-430F290290C8}")), ctypes.byref(_policyConfigClient))
            return 0
        except:
            return 1

def Set_DefaultAudioDevice(device_id):
    if PolicyConfigClient.SetDefaultDevice(f"{{0.0.0.00000000}}.{device_id}") == 0:
        print("SUCCESS: The default audio device has been set.")
    else:
        print("ERROR: There has been a problem setting the default audio device.")

id =  "{51576283-45ac-44a4-8252-a4dba0948c0f}"#スピーカー"{UUID}"
Set_DefaultAudioDevice (id)

