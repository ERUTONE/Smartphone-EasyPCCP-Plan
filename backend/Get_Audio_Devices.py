import winreg

def Get_Devices():
    reg_root = r"Software\Microsoft"
    reg_key = reg_root + r"\Windows\CurrentVersion\MMDevices\Audio\Render"
    print("Active Sound devices:")
    
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key) as key:
            for i in range(winreg.QueryInfoKey(key)[0]): 
                sub_key_name = winreg.EnumKey(key, i)
                sub_key_path = reg_key + '\\' + sub_key_name + r"\Properties"
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key_path) as sub_key:
                    device_name = winreg.QueryValueEx(sub_key, "{a45c254e-df1c-4efd-8020-67d146a850e0},2")[0]
                    print("  " + str(device_name))
                    print("    " + sub_key_name)
    except FileNotFoundError:
        print("The registry path does not exist.")
    except PermissionError:
        print("Permission denied. Please run as administrator.")
    except Exception as e:
        print(f"An error occurred: {e}")

Get_Devices()



# Active Sound devices:
#   スピーカー
#     {43966c92-6c3d-41a3-bd3f-7f061a619756}
#   ヘッドホン
#     {51576283-45ac-44a4-8252-a4dba0948c0f}
#   RTK FHD HDR
#     {ef219f8e-3965-4d2f-bd00-ccf793ba1c89}