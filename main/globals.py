from typing import Final

template:   Final[str] = "main/client/src/template/"

resources:  Final[str] = "main/client/resources/"
layout:     Final[str] = resources + "layout/"
widget:     Final[str] = resources + "widget/"
theme:      Final[str] = resources + "theme/"
icon:       Final[str] = resources + "icon/"
img:        Final[str] = resources + "img/"

layout_default: Final[str] = layout + "default.json"
theme_default:  Final[str] = theme + "default.css"

custom:     Final[str] = "custom/"
c_layout:   Final[str] = custom + "layout/"
c_widget:   Final[str] = custom + "widget/"
c_theme:    Final[str] = custom + "theme/"
c_icon:     Final[str] = custom + "icon/"
c_img:      Final[str] = custom + "img/"

functions:  Final[str] = "main/functions/"