import json, regex as re


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
        

class widget:
    
    widget_style = {
        ".components":[]
    }
    
    def __init__(self, widget_path, id):
        
        with open(widget_path, "r") as f:
            for k, v in json.load(f).items():
                setattr(self, k, v)
        self.id = id
        self.scale = { "col": self.column, "row": self.row }
        if hasattr(self, "content") :
            self.content_count = len(self.content)
        else: self.content_count = 0
                
    
    def create_widget(self):
        widget_str = ""
        # title     | object
        _title = None
        if (hasattr(self, "title") and self.title!="") :
            _title = sizedtext(self.title)
            _title.div =f'<div class="widget_title" \
                style="font-size:{_title.font_size};">{_title.text}</div>'
        
        # sync      | function
        if hasattr(self, "sync") and self.sync != "none" :
            ...
        
        # container | style
        if not hasattr(self, "container") : self.container = "vbox"
        widget_str+= f'<div class="components" id="cs{self.id}">'
        self.widget_style['.components'].append(self.container_style(self.container))
        
        # content   | object, style, function
        if hasattr(self, "content") :
            for i in range(self.content_count):
                _component = self.content[i]
                _component["id"] = i
                # text
                if _component["type"] == "text" :
                    widget_str += self.cp_text(_component)
                self.widget_style[f".components > #c{i}"] = []
        
        widget_str += '</div>'
        if _title: widget_str += _title.div
        return f'<div class="widget" id="w{self.id}">{widget_str}</div>'

    def get_style(self):
        style_str = f'#w{self.id} > .components{{ {" ".join(self.widget_style[".components"])} }}\n'
        #TODO add content styles
        return style_str
    
    # -------------------------------- #
    
    def container_style(self, container):
        if container == "vbox":
            _style = f"display:grid; grid-template-columns:1fr; align-content: center;"
        
        return _style
    
    def cp_text(self, component):
        _text = sizedtext(component["text"])
        _id = component["id"]
        _div = f'<div class="component text" id="c{_id}" style="font-size:{_text.font_size};">'
        _div += _text.text
        return _div + "</div>"