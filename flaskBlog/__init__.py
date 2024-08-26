from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskBlog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Manage All Instance
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Manage All Routes
    # Note: import all routes after creation of db variable
    from flaskBlog.users.routes import users
    from flaskBlog.posts.routes import posts
    from flaskBlog.main.routes import main

    # Manage All BluePrints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app


""" Descriptions """

# app = Flask(__name__) :
"""
Flask class ko use karte hue ek naya instance banaya ja raha, Agar yeh file directly run ho rahi hai to __name__ ki value __main__ hoti hai. 
Agar is file ko kisi aur file se import kiya jaye, to __name__ us module ka naam hota hai. 'app' means Ek naya Flask application.
"""

# db = SQLAlchemy(app):
""" 
SQLAlchemy: This is SQLAlchemy Database instance, means SQLAlchemy ko Flask application ke saath initialize kar rahe hain, taake aap database operations easily perform kar sakein.
"""

# bcrypt = Bcrypt(app):                  -->We create bcrypt instance
""" 
Bcrypt: For Hashed Password
"""

# login_manager = LoginManager(app):      -->We create login_manager instance
"""
LoginManager: To handle user session management aur authentication. To implement login aur logout functionalities
"""

# login_manager.login_view = 'login'
"""
'login' is our Login Funtion of login route, this line means jab koi user jo login nahi hua, kisi protected route ko access karne ki koshish kare, to usay automatically login page par redirect kiya jaye.
Jis routes ka sath @login_required  decorator use hoga wo protected route ban jai ga
"""

# login_manager.login_message_category = 'info'
"""
Kisi protected route ko bina login kia jo error message show hota ha yai line uski styling ha jesa info, danger, primary etc
"""

# from flaskBlog.users.routes import users
"""
users is the name of variable in our users route that is the instance of our blueprint class
"""

# create_app function:
"""
Basically we're going to initialize the extensions at the top of our file but without the app variable
create_app function Flask application ko setup karne aur configure karne ka ek organized method hai, jisse aap easily different settings aur components ko manage kar sakte hain.
"""
