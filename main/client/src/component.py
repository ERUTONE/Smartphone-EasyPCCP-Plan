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
    
# ---------------------------------------------------- #

class sizedtext:
    font_size = {
        "s" : "0.5em",
        "m" : "1em",
        "l" : "2em",
        "xl": "4em",
        "xxl": "8em"
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
        r"%resources%": r"main/client/resources/",
        r"%custom%": r"custom/"
    }
    
    def siz(self, obj):
        _scales = {
            "s" : "3em",
            "m" : "4em",
            "l" : "6em",
            "xl": "9em",
            "xxl": "100%",
            "xxl": "100%"
        }
        if hasattr(obj, "size") and obj.size in _scales:
            _size = obj.size
        else:
            _size = "m"
        return _scales[_size]
    
    def __init__(self, obj):
        # src: %xxx% to path
        src = obj.src
        _destination = re.match(r"%[^%]+%", src)
        if _destination != None and _destination.group() in self.destinations:
            src = src.replace(_destination.group(), self.destinations[_destination.group()])
        self.src = src
        
        # siz -> length
        self.length = self.siz(obj)
        
        # style: object-fit, position
        if self.length!="100%":
        
            if hasattr(obj, "fill") and obj.fill=="true":
                _object_fit = "width:100%; height:100%; object-fit: cover;"
            else:
                _object_fit = "width:100%; height:100%; object-fit: contain;"
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
        
        self.style = _object_fit + _pos
    
    def get_imgtag(self):
        return f'<img src="{self.src}" style="{self.style}">'