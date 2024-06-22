import main.globals as g
import main.host.src.host as host

host.add_onload_js_queue("main/functions/datetime/datetime.js")

def time(format="hh:mm:ss"):
    host.add_onload_js_queue(f'startClockUpdate("{format}");', type="code")
    _div = f'<div id="txt_datetime_{format}" style="display:inline-block;"></div>'
    return _div

def date(format="YYYY/MM/DD"):
    host.add_onload_js_queue(f'startClockUpdate("{format}");', type="code")
    _div = f'<div id="txt_datetime_{format}" style="display:inline-block;"></div>'
    return _div

def dow(format=""):
    if not format.startswith("dow"): format = "dow"+format
    host.add_onload_js_queue(f'startClockUpdate("{format}");', type="code")
    _div = f'<div id="txt_datetime_{format}" style="display:inline-block;"></div>'
    return _div
