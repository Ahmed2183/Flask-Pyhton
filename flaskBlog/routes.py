from flask import render_template, url_for, flash, redirect
from flaskBlog import app
from flaskBlog.forms import RegistrationForm, LoginForm                                
from flaskBlog.models import User, Post               


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
    form = RegistrationForm()
    if form.validate_on_submit():                                        #`f` string ka istemal hota hai username ke data ko message ke saath include karne ke liye.
        flash(f'Account Created for {form.username.data}!', 'success')   # 2nd argument is category its bootstrap class of alert 
        return redirect(url_for('home'))                                 #--> home is route function
    return render_template("register.html", title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", title='Login', form=form)

