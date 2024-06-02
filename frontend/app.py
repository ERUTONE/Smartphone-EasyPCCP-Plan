# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@db:5432/mytodos' # PostgreSQL接続用のURI
db = SQLAlchemy(app)

# ルーティングをBlueprintとして定義します
from flask import Blueprint

# Blueprintオブジェクトを作成します
todos_bp = Blueprint('todos', __name__)

# ToDoモデルを定義します
class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  completed = db.Column(db.Boolean, default=False)
# 一覧ページ
@todos_bp.route('/')
def index():
  todos = Todo.query.all()
  return render_template('index.html', todos=todos)

# ToDo作成ページ
@todos_bp.route('/create', methods=['GET', 'POST'])
def create():
  if request.method == 'POST':
    title = request.form['title']
    todo = Todo(title=title)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('todos.index')) # Blueprint名を指定してリダイレクト
  return render_template('create_todo.html')

# Blueprintをアプリケーションに登録します
app.register_blueprint(todos_bp, url_prefix='/todos')

if __name__ == '__main__':
  db.create_all()
  app.run(host='0.0.0.0', debug=True)