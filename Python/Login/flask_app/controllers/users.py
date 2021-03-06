from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_new_user(request.form):
        return redirect('/')
    else:
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        print(data)
        User.add_user(data)
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_user_by_email(request.form)
    if not user:
        flash('Email does not exist')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password is incorrect")
    session['user_email'] = user.email
    session['user_name'] = user.first_name
    session['user_id'] = user.id
    print("logged in")
    return redirect('/success')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out")
    return redirect('/')
