from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email address you entered does not exist.', category='error')
        
    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=['GET', 'POST']) # GET is used for asking server to get some data
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('This email address is already in use.', category='error')
        elif username_exists:
            flash('This username is already in use.', category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(username) < 8:
            flash('Username has to be at least 8 characters long.', category='error')
        elif len(password1) < 8:
            flash('Password has to be at least 8 characters long.', category='error')
        elif len(email) < 4:
            flash('Email address is invalid.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account successfully created!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template("signup.html", user=current_user)

@auth.route("/logout")
@login_required # only if you have been logged in you can access this page
def logout():
    logout_user()
    return redirect(url_for("views.home"))