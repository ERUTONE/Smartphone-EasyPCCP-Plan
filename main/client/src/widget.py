import regex as re

def create_widget(widget_path, id):
    widget_scale = [int(n) for n in re.findall(r"(\d+)", widget_path)[-2:]]
    
    # title
    
    # sync
    
    # container
    
    # content
    
    return f'<div class="widget" id="w{id}">TODO</div>'

# 