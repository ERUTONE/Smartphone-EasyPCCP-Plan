print("client importing...")
from app import app

print(app.config)

@app.route("/")
def hello():
    return "hello from client!"