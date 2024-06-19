import regex as re

class component:
    
    # --public------ #
    
    component_style = []
    
    def __init__(self, parent_widget, content_num):
        self.component_style = []
        
        _content_dict = parent_widget.content[content_num]
        self.parent = parent_widget
        for k, v in _content_dict.items():
            setattr(self, k, v)
        self.cssid = f"{self.parent.cssid}c{content_num}"
        self.cls = _content_dict['class'] if "class" in _content_dict else ""
    
    def create_component(self):
        if not hasattr(self, "type"): return "ERROR: No type specified"
        
        if self.type == "text":
            self.component_style.append("margin: 0 auto;")
            return self.c_text()
        if self.type == "image":
            return self.c_image()
        if self.type == "button-icon":
            return self.c_button_icon()
        
        return f"ERROR: No {self.type} type generator<br>"
    
    def get_style(self):
        if len(self.component_style) == 0: return ""
        _selector = f".widget#{self.parent.cssid} > .subcontainer > .component#{self.cssid}"
        return f'{_selector}{{ {" ".join(self.component_style)} }}'
    
    # --private----- #
    

        
    # --element----- #
    
    def c_text(self):
        _text = sizedtext(self.text)
        _div = f'<div class="component {self.cls} text " id="{self.cssid}" style="font-size:{_text.font_size};">'
        return _div + _text.text + "</div>\n"
    
    def c_image(self):
        _image = image(self)
        _div = f'<div class="component {self.cls} image" id="{self.cssid}" \
            style="overflow:hidden; width:{_image.length}; height:{_image.length}; position: relative;">'

        _imgtag = _image.get_imgtag()
        
        if _image.length=="100%":
            return _imgtag
        return _div + _imgtag + '</div>\n'
    
    def c_button_icon(self):
        _icon = image(self, allow_fill=False)
        _div = f'<button name=b_{self.cssid} class="component {self.cls} button button-icon" id="{self.cssid}"\
            style="overflow:hidden; width:{_icon.length}; height:{_icon.length}; position: relative;">'
            
        return _div + _icon.get_imgtag() + '</button>\n'
# ---------------------------------------------------- #

class sizedtext:
    font_size = {
        "s" : "0.5rem",
        "m" : "1rem",
        "l" : "2rem",
        "xl": "4rem",
        "xxl": "8rem"
    }
    
    def __init__(self, sizedtxt):
        scale = re.match(r"^[^:]+(?=:)", sizedtxt)
        text = sizedtxt[(0 if scale==None else len(scale.group())+1):]
        if scale==None: scale = "m"
        else: scale = scale.group()
        
        self.original = sizedtxt                # m:text
        self.text = text                        # text
        self.scale = scale                      # s, m, l, xl, xxl
        self.font_size = self.font_size[scale]  # em
        
class image:
    destinations = {
        r"%resources%": r"main/client/resources",
        r"%custom%": r"custom"
    }
    component_scales = {
        "s" : "3rem",
        "m" : "4rem",
        "l" : "6rem",
        "xl": "9rem",
        "xxl": "100%"
    }
    innner_scales = {
        "s" : "50%",
        "m" : "75%",
        "l" : "100%"
    }

    def siz(self, obj, allow_fill):
        _size = "m"
        if hasattr(obj, "size"):
            if (_outersize := re.match(r"^[^:]+:?", obj.size)) != None:
                _outersize = re.match(r"[^:]+", _outersize.group()).group()
                if _outersize in self.component_scales:
                    _size = _outersize
        
        if _size=="xxl" and not allow_fill:
            _size = "xl"
        
        return self.component_scales[_size]
    
    def innersize(self, obj):
        _size = "l"
        if hasattr(obj, "size"):
            if (_innnersize := re.search(r":[^:]+", obj.size)) != None:
                _size = _innnersize.group()[1:]
                if not _size in self.innner_scales:
                    _size = "l"
        return self.innner_scales[_size]
    
    def filetype(self):
        return re.search(r"[^\.]+$", self.src).group()
    
    def flatcolor(self):
        if self.color[0] != "#": return ""
        # hex RGB to HSB
        # TODO: not available for HSB, only Brightness
        
        # hex to int
        self.color = self.color.replace("#", "")
        if len(self.color)==3:
            self.color = ''.join([c*2 for c in self.color])
        r = int(self.color[0:2], 16)
        g = int(self.color[2:4], 16)
        b = int(self.color[4:6], 16)
        
        maxv = max(r,g,b)
        # minv = min(r,g,b)
        # maxc = "r"
        # if g > r: maxc = "g"
        # if b > g: maxc = "b"
        
        # # hue degree 0-360
        # if r==g==b:
        #     hue = 0
        # elif maxc == "r":
        #     hue = 60 * ((g - b) / (maxv - minv))
        # elif maxc == "g":
        #     hue = 60 * ((b - r) / (maxv - minv)) + 120
        # elif maxc == "b":
        #     hue = 60 * ((r - g) / (maxv - minv)) + 240
        
        # # saturation %
        # saturation = (maxv - minv) / maxv
        
        # brightness %
        brightness = maxv / 255
        
        _style = f" filter: brightness({brightness*100}%); "
        return _style
    
    def __init__(self, obj, allow_fill=True):
        # src: %xxx% to path
        src = obj.src
        _destination = re.match(r"%[^%]+%", src)
        if _destination != None and _destination.group() in self.destinations:
            src = src.replace(_destination.group(), self.destinations[_destination.group()])
        self.src = src
        
        # siz -> length
        self.length = self.siz(obj,allow_fill)
        
        # size: object-fit, position
        if self.length!="100%":
        
            if hasattr(obj, "fill") and obj.fill=="true":
                _object_fit = "width:100%; height:100%; object-fit: cover;"
            else:
                _innerscale = self.innersize(obj)
                _object_fit = f"width:{_innerscale}; height:{_innerscale}; object-fit: contain;"
            _pos = ""
        
        else:
            if hasattr(obj, "fill") and obj.fill=="height":
                # cut horizontal side
                _object_fit = "width:auto; height:100%;"
                _pos = "position: absolute; left:50%; top:50%; transform: translate(-50%, -50%);"
            else:
                # cut vertival side
                _object_fit = "width:100%; height:100%;" # TODO: 画像サイズが画面サイズに負けてると結局切れる
                _pos = "position: static !important;"
        
        # color
        if hasattr(obj, "color"):
            self.color = obj.color
        else: 
            self.color = "#ffffff"
            
        self.style = _object_fit + _pos + self.flatcolor()
    
    def get_imgtag(self):    
        return f'<img src="{self.src}" style="{self.style}">'