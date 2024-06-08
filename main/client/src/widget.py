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
    def __init__(self, widget_path, id):
        
        with open(widget_path, "r") as f:
            for k, v in json.load(f).items():
                setattr(self, k, v)
        self.id = id
        self.scale = { "col": self.column, "row": self.row }
                
    
    def create_widget(self):
        widget_str = ""
        # title
        _title = None
        if (hasattr(self, "title") and self.title!="") :
            _title = sizedtext(self.title)
            _title.div =f'<div class="widget_title" \
                style="font-size:{_title.font_size};">{_title.text}</div>'
        
        # sync
        if hasattr(self, "sync") and self.sync != "none" :
            ...
        
        # container
        if not hasattr(self, "container") : self.container = "vbox"
        widget_str+= '<div class="components">'
        
        # content
        if hasattr(self, "content") :
            for component in self.content:
                ...
        
        widget_str += '</div>'
        if _title: widget_str += _title.div
        return f'<div class="widget" id="w{self.id}">{widget_str}</div>'
