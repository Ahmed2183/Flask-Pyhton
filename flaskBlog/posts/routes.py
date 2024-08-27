from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flaskBlog import db
from flaskBlog.models import Post
from flask_login import current_user, login_required

from flaskBlog.posts.forms import PostForm
from flaskBlog.posts.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    picture_file = 'default.jpg'
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        post = Post(title=form.title.data, content=form.content.data, image_file=picture_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post Has Been Created!', 'success')
        return redirect(url_for('main.home'))
    image_file = url_for('static', filename='post_profile_pics/' + current_user.image_file)
    return render_template("create_post.html", title='New Post', image_file=image_file, form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post Has Been Deleted!', 'success')
    return redirect(url_for('main.home'))


""" Descriptions """

# render_template is for html files, url_for is for css files, flash is for alert messages

# request:
"""
Gives you access to details of the incoming HTTP request, such as form data, 
query parameters, and headers.
"""

# abort(403)
"""
abort is a function that allows you to generate a specific HTTP error code (like 404 or 403) 
to stop the request and return an error response.

if post.author != current_user:
Check if post author not equal to current login user then not access the update route
"""

# db are instance that we define in __init__.py

# Blueprint:
"""
Flask mein Blueprint ek module hai jo apki application ko chote-chote parts mein divide 
karne ki facility deta hai.
"""

# current_user: In current_user we get that user info which is login

# @login_required
"""
Decorator From flask_login means to access this route we need to required login first,
Jis routes ka sath @login_required  decorator use hoga wo protected route ban jai ga
"""

# Post.query.get_or_404(post_id)
"""
This means give me the post with this id if it doesn't exist then return a 404
"""

# db.session.add(post):
"""
session represents a set of operations (like inserts, updates, deletes) that you want to perform)
"""

# db.session.commit():
"""
Before committing changes are temporary, After committing changes are permanent in Database
"""

# form.validate_on_submit():
"""
Checks if a form has been submitted and if the input data is valid.
"""

# `f` string ka istemal hota hai username ke data ko message ke saath include karne ke liye.
