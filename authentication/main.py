import os
from flask import Flask, redirect, render_template, request, session, url_for, g
from helpers import get_users, hash_password

__winc_id__ = '8fd255f5fe5e40dcb1995184eaa26116'
__human_name__ = 'authentication'

app = Flask(__name__)

app.secret_key = os.urandom(16)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User: {self.username}>"

users = get_users()

@app.route('/home')
def redirect_index():
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html', title='Index')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/lon')
def lon():
    return render_template('lon.html', title='League of Nations')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = hash_password(request.form["password"])
        for x in users:
            if users[x] == password:
                session["username"] = username
                g.username = session["username"]
            else:
                g.username = None
                return redirect(url_for("dashboard"))
        return redirect(url_for("login", error=True))
    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", title= 'Dashboard')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)