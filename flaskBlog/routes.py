from flask import render_template, url_for, flash, redirect, request
from flaskBlog import app, db, bcrypt                             
from flaskBlog.forms import RegistrationForm, LoginForm                                
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required              


posts = [
    {
        'author': 'Blogger1',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_Posted': 'July 2, 2024'
    },
    {
        'author': 'Blogger2',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_Posted': 'July 3, 2024' 
    }
]

#Those two routes are being handled by same home function:
@app.route("/")                                
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)
 
@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():    
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')               #-->Hash Password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)         #-->Add Data In User Model/Table
        db.session.add(user)                                                                              #-->session represents a set of operations (like inserts, updates, deletes) that you want to perform)
        db.session.commit()                                                                               #-->Before committing changes are temporary, After committing changes are permanent in Database
        flash('Your account has been created! You are now able to log in', 'success')   # 2nd argument is category its bootstrap class of alert 
        return redirect(url_for('login'))                                 #--> login is route function
    return render_template("register.html", title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)                     #-->remember is Remember Me that we define in LoginForm class in forms.py
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required                           
def account():
    return render_template("account.html", title='Account')





""" Description """

#app, db etc these all are instance that we define in __init__.py

#`f` string ka istemal hota hai username ke data ko message ke saath include karne ke liye.

#@login_required                           
"""
Decorator From flask_login means to access this route we need to required login first
"""

#request
"""
  next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home'))

'request.args' URL parameters ko represent karta hai.
.get('next') function URL mein next parameter ko retrieve karta hai.

This code means Jab user ek protected page ko access karne ki koshish karta hai aur usay login karna padta hai, to login hone ke baad usay us original protected page par le jai ga 
jahan woh pehle jana chahta tha. Agar koi specific page specify nahi kiya gaya tha, to user ko home page par redirect kiya jata hai.

URL Looks Like: /login?next=%2Faccount       --> means after login take user onto the account page
"""