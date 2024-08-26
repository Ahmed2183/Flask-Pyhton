import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from flaskBlog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Resize the image to 125x125 pixels
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)


""" Descriptions """

# mail etc these all are instance that we define in __init__.py

# url_for is for css files

# secrets: For creating random hex keys

# current_app.root_path application ka root directory provide karta hai

# picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
"""
Yeh line full path banati hai jahan picture ko save kiya jayega.
"""

# _, f_ext = os.path.splitext(form_picture.filename)
"""
Underscore (_) ko use kiya jata hai jab aap kisi variable ko assign karte hain lekin aap us variable ka aage use nahi karna chahte.
f_name, f_ext: f_name means file name of uploaded picture, f_name ko '_' sa hamna ignore kia
f_ext menas file extension of uploaded picture

"""

# Message: For Mail Text/Message which you want to write
