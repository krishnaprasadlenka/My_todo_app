import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


# Save todo.db in the same folder as app.py
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<{self.sno}> {self.title}"


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        if 'title' in request.form and 'desc' in request.form:
            title = request.form["title"]
            desc = request.form["desc"]
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
        elif 'search' in request.form:
            search_term = request.form["search"]
            allTodo = Todo.query.filter(db.or_(
                Todo.title.like(f"%{search_term}%"),
                Todo.desc.like(f"%{search_term}%")
            )).all()
            return render_template("index.html", allTodo=allTodo)

    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)


@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "This is the product page"


@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == "POST":
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("hello_world"))
    return render_template("update.html", todo=todo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("hello_world"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)