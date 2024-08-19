import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskBlog import app, db, bcrypt, mail
from flaskBlog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, \
    ResetPasswordForm
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


# Those two routes are being handled by same home function:
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=5)  # -->paginate is for pagination
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # -->Hash Password
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)  # -->Add Data In User Model/Table
        db.session.add(
            user)  # -->session represents a set of operations (like inserts, updates, deletes) that you want to perform)
        db.session.commit()  # -->Before committing changes are temporary, After committing changes are permanent in Database
        flash('Your account has been created! You are now able to log in',
              'success')  # 2nd argument is category its bootstrap class of alert
        return redirect(url_for('login'))  # --> login is route function
    return render_template("register.html", title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,
                       remember=form.remember.data)  # -->remember is Remember Me that we define in LoginForm class in forms.py
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resize the image to 125x125 pixels
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Been Updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post Has Been Created!', 'success')
        return redirect(url_for('home'))
    return render_template("create_post.html", title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post Has Been Updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post Has Been Deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,
                                                                                         per_page=5)  # -->paginate is for pagination
    return render_template("user_posts.html", posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in',
              'success')
        return redirect(url_for('login'))
    return render_template("reset_token.html", title="Reset Password", form=form)


""" Description """

# app, db etc these all are instance that we define in __init__.py

# `f` string ka istemal hota hai username ke data ko message ke saath include karne ke liye.

# @login_required
"""
Decorator From flask_login means to access this route we need to required login first
"""

# request
"""
  next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home'))

'request.args' URL parameters ko represent karta hai.
.get('next') function URL mein next parameter ko retrieve karta hai.

This code means Jab user ek protected page ko access karne ki koshish karta hai aur usay login karna padta hai, to login hone ke baad usay us original protected page par le jai ga 
jahan woh pehle jana chahta tha. Agar koi specific page specify nahi kiya gaya tha, to user ko home page par redirect kiya jata hai.

URL Looks Like: /login?next=%2Faccount       --> means after login take user onto the account page
"""

# secrets: For creating random hex keys

# current_user: In current_user we get that user info which is login

# _, f_ext = os.path.splitext(form_picture.filename)
"""
Underscore (_) ko use kiya jata hai jab aap kisi variable ko assign karte hain lekin aap us variable ka aage use nahi karna chahte.
f_name, f_ext: f_name means file name of uploaded picture f_name ko '_' sa hamna ignore kia
f_ext menas file extension of uploaded picture

"""

# app.root_path application ka root directory provide karta hai

# picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
"""
Yeh line full path banati hai jahan picture ko save kiya jayega.
"""

# Post.query.get_or_404(post_id)
"""
This means give me the post with this id if it doesn't exist then return a 404
"""

# abort(403)
"""
If post author not equal to current login user then not access the update route
"""

# page = request.args.get('page', 1, type=int)
"""
request.args.get('page', 1, type=int) ka matlab hai ke URL mein agar page parameter diya gaya hai, to uski value le lo. Agar page parameter nahi diya gaya, to default value 1 set kar lo,
type=int means page value should be integer
"""

# posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
"""
Post.date_posted.desc(): new post will be shown on top
per_page=1 means eik page pr eik post hogi

"""
