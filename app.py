from flask import Flask, render_template, redirect, request, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
app.app_context()

class Users(db.Model):
    id = db.Column(db.Integer)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=["GET", "POST"])
def index():
    if 'username' in session:
        return render_template("index.html", username=session['username'])
    
    else:
        return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and Bcrypt.check_password_hash(user.password, password):
            session['username'] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid username or password")
    else:
        return render_template("login.html")
        

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template("register.html", error="Username already exists")
        else:
            new_user = Users(email=email, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect("/")
    else:
        return render_template("register.html")

@app.route('/logout')

def logout():
    session.pop('username',None)
    return redirect("/")
        
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, host="0.0.0.0", port=5000)