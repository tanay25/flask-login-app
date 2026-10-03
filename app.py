from flask import Flask,render_template, request, redirect, session
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY","mysecrectkey")

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST","localhost"),
        user=os.getenv("DB_USER","root"),
        password=os.getenv("DB_PASSWORD","root123"),
        database=os.getenv("DB_NAME","flaskdb")
    )

@app.route('/')
def home():
    if "user" in session:
        return redirect('/welcome')
    return redirect('/login')

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        hashed_password=generate_password_hash(password)
        db=get_db()
        cursor=db.cursor()
        cursor.execute("INSERT INTO users (username,password) VALUES (%s,%s)",(username,hashed_password))
        db.commit()
        cursor.close()
        db.close()
        return redirect('/login')
    return render_template("register.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        db=get_db()
        cursor=db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s",(username,))
        user=cursor.fetchone()
        cursor.close()
        db.close()
        if user and check_password_hash(user["password"],password):
            session["user"]=user["username"]
            return redirect('/welcome')
        else:
            return "Invalid credentials"
    return render_template("login.html")

@app.route("/welcome")
def welcome():
    if "user" not in session:
        return redirect('/login')
    return render_template("welcome.html",username=session["user"])

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect('/login')

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
    