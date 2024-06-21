from main.client.src.component import component, sizedtext

import json


# -------------------------------- #
class widget:
    
    widget_html = ""
    widget_style = []
    components = []
    
    # - public ------------------------------- #
    
    def __init__(self, widget_path, id):
        
        self.widget_html = ""
        self.widget_style = []
        self.components = []
        
        with open(widget_path, "r") as f:
            fd = json.load(f)
            for k, v in fd.items():
                setattr(self, k, v)
            self.cls = fd['class'] if "class" in fd else ""
        self.id = id
        self.cssid = f"w{id}"
        self.scale = { "col": self.column, "row": self.row }
        if hasattr(self, "content") :
            self.content_count = len(self.content)
        else: self.content_count = 0
                
    
    def create_widget(self):
        widget_html = ""
        # title     | object
        _title = None
        if (hasattr(self, "title") and self.title!="") :
            _title = sizedtext(self.title)
            _title.div =f'<div class="widget_title" id="{self.cssid}-title"\
                style="font-size:{_title.font_size};">&nbsp;{_title.text}&nbsp;</div>'
        
        # sync      | function
        if hasattr(self, "sync") and self.sync != "none" :
            ...
        
        # container | style
        if not hasattr(self, "container") : self.container = "vbox"
        widget_html+= '<div class=" subcontainer">'
        self.widget_style.append(self.container_style())
        
        # content   | object, style, function
        if hasattr(self, "content") :
            for i in range(self.content_count):
                _component = component(self, i)
                self.components.append(_component)
                widget_html += _component.create_component()
                self.widget_style.append(_component.get_style())
        
        widget_html += '</div>'
        # if _title: widget_html += _title.div
        self.widget_html = widget_html
        return f'<div class="widget {self.cls}" id="w{self.id}">{widget_html}</div>' + ( _title.div if _title else "" )

    def get_style(self):
        return "\n".join(self.widget_style)
    
    # - private ------------------------------- #
    
    def container_style(self):
        _style = f"\n.widget#{self.cssid} > .subcontainer{{ "
        if self.container == "vbox":
            _style += f"display:grid; align-content: center; margin: 0 auto; width:fit-content;"
        if self.container == "hbox":
            _style += f"display:flex;  align-content: center; margin: 0 auto; width:fit-content;"
        
        return _style + "}"
    
    