from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskBlog import db, bcrypt
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

from flaskBlog.users.forms import LoginForm, RegistrationForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskBlog.users.utils import send_reset_email
from flaskBlog.common.common import save_picture

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # -->Hash Password
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)  # -->Add Data In User Model/Table
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in',
              'success')  # 2nd argument is category its bootstrap class of alert
        return redirect(url_for('users.login'))  # --> login is route function
    return render_template("register.html", title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,
                       remember=form.remember.data)  # -->remember is Remember Me that we define in LoginForm class in user forms file
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, "user_profile_pics")
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Been Updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='user_profile_pics/' + current_user.image_file)
    return render_template("account.html", title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in',
              'success')
        return redirect(url_for('users.login'))
    return render_template("reset_token.html", title="Reset Password", form=form)


""" Descriptions """

# render_template is for html files, url_for is for css files, flash is for alert messages, paginate is for pagination

# request:
"""
Gives you access to details of the incoming HTTP request, such as form data, 
query parameters, and headers.
"""

# Blueprint:
"""
Flask mein Blueprint ek module hai jo apki application ko chote-chote parts mein divide 
karne ki facility deta hai.
"""

# db, bcrypt are instance that we define in __init__.py

# current_user: In current_user we get that user info which is login

# @login_required
"""
Decorator From flask_login means to access this route we need to required login first,
Jis routes ka sath @login_required  decorator use hoga wo protected route ban jai ga
"""

# login_user and logout_user:
"""
login_user(user): Logs in the user by setting the user’s session data. 
It keeps the user logged in across requests.

logout_user(): Logs out the current user by removing their session data, 
effectively ending their login session.
"""

# form.validate_on_submit():
"""
Checks if a form has been submitted and if the input data is valid.
"""

# bcrypt
"""
bcrypt: For Hashed Password
"""

# db.session.add(user):
"""
session represents a set of operations (like inserts, updates, deletes) that you want to perform)
"""

# db.session.commit():
"""
Before committing changes are temporary, After committing changes are permanent in Database
"""

# request.args.get:
"""
'request.args' URL parameters ko represent karta hai.
.get('page') yai function URL mein 'page' parameter ko get karta hai.
"""

# page = request.args.get('page', 1, type=int)
"""
request.args.get('page', 1, type=int) ka matlab hai ke URL mein agar page parameter diya gaya hai, to uski value le lo. Agar page parameter nahi diya gaya, to default value 1 set kar lo,
type=int means page value should be integer
"""

# User.query.filter_by(username=username).first_or_404():
"""
This statement tries to find a user with the given username. If found, it returns the user object; 
if not, it triggers a 404 error indicating that the user was not found.
"""

# Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
"""
Post.date_posted.desc(): new post will be shown on top
per_page=1 means eik page pr eik post hogi
"""

# `f` string ka istemal hota hai username ke data ko message ke saath include karne ke liye.
