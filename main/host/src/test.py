from pypresence import Presence
import time
import sys

client_id = '1096423905062813716'
access_token = sys.argv[1]

rpc = Presence(client_id)
rpc.connect()

def toggle_mute():
    try:
        voice_settings = rpc.get_voice_settings()
        new_mute_status = not voice_settings['mute']
        rpc.set_voice_settings(mute=new_mute_status)
        print('Voice settings toggled')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    print('RPC Client ready')
    toggle_mute()

# Keep the script running to maintain the connection
while True:
    time.sleep(15)
