
def setSoundMute(mute):
    if mute:
        print("amixer set Master mute")
    else:
        print("amixer set Master unmute")