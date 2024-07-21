import json, weakref
import main.globals as g
from main.client.src.component import component, sizedtext

# weakref
_add_onload_js_queue = weakref.ref(g.host.add_onload_js_queue)

# -------------------------------- #
class widget:
    
    widget_html = ""
    components = []
    
    # - public ------------------------------- #
    
    def __init__(self, widget_path, id):
        
        self.components = []
        
        with open(widget_path, "r") as f:
            fd = json.load(f)
            for k, v in fd.items():
                setattr(self, k, v)
            self.cls = fd['class'] if "class" in fd else ""
            self.sync = fd['sync'] if "sync" in fd else "none"
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
        self.sync_action = []
        
        # container | style
        if not hasattr(self, "container") : self.container = "vbox"
        widget_html+= '<div class=" subcontainer">'
        
        # content   | object, style, function
        if hasattr(self, "content") :
            for i in range(self.content_count):
                _component = component(self, i)
                self.components.append(_component)
                widget_html += _component.create_component()
                self.sync_action.append(_component.get_syncaction())
                _component = None
        
        widget_html += '</div>'
        # if _title: widget_html += _title.div
        return f'<div class="widget {self.cls}" id="w{self.id}">{widget_html}</div>' + ( _title.div if _title and _title.text!="" else "" )

    def get_style(self):
        return self.container_style()
    
    # - private ------------------------------- #
    
    def container_style(self):
        _style = f"\n.widget#{self.cssid} > .subcontainer{{ "
        if self.container == "vbox":
            _style += f"display:grid; align-content: center; margin: 0 auto; " # width:fit-content;
        if self.container == "hbox":
            _style += f"display:flex;  align-content: center; margin: 0 auto; width:fit-content;"
        
        return _style + "}"
    
    #TODO maybe delete soon
    def set_sync(self):
        if not hasattr(self, "sync_action") or len(self.sync_action)==0: return
        
        if self.sync == "websocket":
            for action in self.sync_action:
                trigger = action
    
    