import main.globals as g

def time(format="hh:mm:ss"):
    # TODO
    with open(g.functions+"datetime/time.js") as f:
        ...
    return f"TIME {format}"

def date(format="YYYY/MM/DD"):
    # TODO
    return f"DATE {format}"

def dow(format=""):
    # TODO
    return f"DOW {format}"
