import json, regex as re

class widget:
    def __init__(self, widget_path, id):
        
        with open(widget_path, "r") as f:
            for k, v in json.load(f).items():
                setattr(self, k, v)
        self.id = id
        self.scale = { "col": self.column, "row": self.row }
                
    
    def create_widget(self):
        # title
        
        # sync
        
        # container
        
        # content
        
        return f'<div class="widget" id="w{self.id}">TODO</div>'
