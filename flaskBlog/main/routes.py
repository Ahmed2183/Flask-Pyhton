from flask import Blueprint, request, render_template
from flaskBlog.models import Post

main = Blueprint('main', __name__)


# Those two routes "/" and "/home" are being handled by same home function:
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title='About')


""" Descriptions """

# render_template is for html files, paginate is for pagination

# Blueprint:
"""
Flask mein Blueprint ek module hai jo apki application ko chote-chote parts mein divide 
karne ki facility deta hai.
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

# posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
"""
Post.date_posted.desc(): new post will be shown on top
per_page=1 means eik page pr eik post hogi
"""

# `f` string ka istemal hota hai username ke data ko message ke saath include karne ke liye.
