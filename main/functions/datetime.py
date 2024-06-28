import main.globals as g
import main.host.src.host as host

host.add_onload_js_queue(g.functions+"_datetime/datetime.js", type="path", static=True)

def time(format="hh:mm:ss"):
    host.add_onload_js_queue(f'startClockUpdate("{format}");', type="code")
    return f'<div class="txt_datetime_{format}" style="display:inline-block;"></div>'

def date(format="YYYY/MM/DD"):
    host.add_onload_js_queue(f'startClockUpdate("{format}");', type="code")
    return f'<div class="txt_datetime_{format}" style="display:inline-block;"></div>'

def dow(format=""):
    if not format.startswith("dow"): format = "dow"+format
    host.add_onload_js_queue(f'startClockUpdate("{format}");', type="code")
    return f'<div class="txt_datetime_{format}" style="display:inline-block;"></div>'
