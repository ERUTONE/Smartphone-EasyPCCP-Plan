from typing import Final

# Home

home:       Final[str] = ""
usercfg:    Final[str] = home + "config/usercfg.json"

# Client

template:   Final[str] = home + "main/client/src/template/"

resources:  Final[str] = home + "main/client/resources/"
layout:     Final[str] = resources + "layout/"
widget:     Final[str] = resources + "widget/"
theme:      Final[str] = resources + "theme/"
icon:       Final[str] = resources + "icon/"
img:        Final[str] = resources + "img/"

layout_default: Final[str] = layout + "default"
theme_default:  Final[str] = theme + "default"

# Custom

custom:     Final[str] = home + "custom/"
c_layout:   Final[str] = custom + "layout/"
c_widget:   Final[str] = custom + "widget/"
c_theme:    Final[str] = custom + "theme/"
c_icon:     Final[str] = custom + "icon/"
c_img:      Final[str] = custom + "img/"

# Main

functions:  Final[str] = home + "main/functions/"