import os
import secrets
from PIL import Image
from flask import current_app


def save_picture(form_picture, folder_name):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, f'static/{folder_name}', picture_fn)

    # Resize the image to 125x125 pixels
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


""" Description """

# secrets: For creating random hex keys

# current_app.root_path application ka root directory provide karta hai

# picture_path = os.path.join(current_app.root_path, 'static/user_profile_pics', picture_fn)
"""
Yeh line full path banati hai jahan picture ko save kiya jayega.
"""

# _, f_ext = os.path.splitext(form_picture.filename)
"""
Underscore (_) ko use kiya jata hai jab aap kisi variable ko assign karte hain lekin aap us variable ka aage use nahi karna chahte.
f_name, f_ext: f_name means file name of uploaded picture, f_name ko '_' sa hamna ignore kia
f_ext menas file extension of uploaded picture
"""
