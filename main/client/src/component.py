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
    
    def siz(self):
        _scales = {
            "s" : "3em",
            "m" : "4em",
            "l" : "6em",
            "xl": "10em",
            "xxl": "100%"
        }
        if hasattr(self, "size") and self.size in _scales:
            _size = self.size
        else:
            _size = "m"
        return _scales[_size]
        
    # --element----- #
    
    def c_text(self):
        _text = sizedtext(self.text)
        _div = f'<div class="component {self.cls} text " id="{self.cssid}" style="font-size:{_text.font_size};">'
        return _div + _text.text + "</div>"
    
    def c_image(self):
        _image = image(self.src)
        _div = f'<div class="component {self.cls} image" id="{self.cssid}" style="overflow:hidden; width:{self.siz()}; height:{self.siz()}; background-color:red;">'
        _imgtag = f'<img src="{_image.src}" style="height:100%; width:auto; margin: 0 auto;">'
        return _div + _imgtag + '</div>'
    
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
    
    def __init__(self, src):
        # %で囲まれた文字列を置換
        _destination = re.match(r"%[^%]+%", src)
        if _destination != None and _destination.group() in self.destinations:
            src = src.replace(_destination.group(), self.destinations[_destination.group()])
        
        self.src = src