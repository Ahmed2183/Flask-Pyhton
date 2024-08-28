from flask import url_for
from flask_mail import Message

from flaskBlog import mail


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

# Message: For Mail Text/Message which you want to write
