from flask import Flask, request, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SECRET_KEY"] = "some_secret_key"
db = SQLAlchemy(app)


# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    medical_history = db.Column(db.Text, nullable=False)


# Create database and sample data
with app.app_context():
    db.create_all()
    if not User.query.first():
        user1 = User(username="alice", password="password1")
        user2 = User(username="bob", password="password2")
        db.session.add_all([user1, user2])
        db.session.commit()
        health1 = HealthData(user_id=1, medical_history="Alice has allergy to peanuts.")
        health2 = HealthData(user_id=2, medical_history="Bob has high blood pressure.")
        db.session.add_all([health1, health2])
        db.session.commit()


# Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        query = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            session["user_id"] = user[0]
            return redirect(url_for("comments"))
        else:
            return "Invalid credentials"
    return render_template("login.html")


@app.route("/comments", methods=["GET", "POST"])
def comments():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        content = request.form["content"]
        comment = Comment(content=content, user_id=session["user_id"])
        db.session.add(comment)
        db.session.commit()
    comments = Comment.query.all()
    return render_template("comments.html", comments=comments)


@app.route("/health/<int:user_id>")
def health(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    health_data = HealthData.query.filter_by(user_id=user_id).first()
    if health_data:
        return render_template("health.html", health_data=health_data)
    else:
        return "No health data found"


if __name__ == "__main__":
    app.run(debug=True)
