from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flaskBlog import db, login_manager, app
from flask_login import UserMixin

""" Get User From User ID """


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


""" DataBase Models """


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='reset-password')

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='reset-password', max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


""" Description """

# id,username,title etc these all are attributes

# class names are also table names in DB but in lowercase. For example class User table name is user

# db, login_manager etc these all are instances that we define in __init__.py

# db.relationship:
"""
'Post' table (ya model) ke saath relationship establish karni hai. In relationship we referencing the Post class
"""

# self: By using the “self” we can access the attributes and methods of the same class

# backref & lazy:
"""
backref ek shortcut hai jo Post model mein ek author attribute automatically add kardy ga.
lazy parameter SQLAlchemy ko batata hai ke data kab load karna hai.True ka matlab hai ke data lazily load hoga, yani jab specifically usko access kiya jayega tabhi load hoga.

Jab aap User instance ka posts attribute access karte hain, toh aapko us user ke saare posts milte hain.
Jab aap Post instance ka author attribute access karte hain, toh aapko us post ka author (User) milta hai.
"""

# In ForeignKey we referencing the user table name with the column id. We specify that this is Foreign key which means that it has a relationship to our User model

# UserMixin:
"""
UserMixin ek class hai jo Flask-Login ko user authentication aur session management ke liye zaroori methods provide karti hai like:
is_authenticated: Ye check karta hai ki user authenticated hai ya nahi.
is_active: Ye check karta hai ki user ka account active hai ya nahi.
is_anonymous: Ye check karta hai ki user anonymous hai ya nahi (i.e., login nahi hua).
get_id: Ye method user ka unique identifier return karta hai jo session management ke liye use hota hai.
"""

# @login_manager.user_loader:
""" 
Decorator: Ek aisa function hai jo kisi doosre function ko asaani se modify kar deta hai.
@login_manager.user_loader decorator ek function ko specify karta hai jo session mein stored user ID se user object ko reload karta hai.
"""

# get_reset_token
"""
Purpose: Yeh function ek token generate karta hai jo password reset ke liye use hota hai.

URLSafeTimedSerializer class ko Serializer ke naam se use kia ha, jo eik secure, URL-safe token generate karta hai jo specific time ke baad expire ho jata hai.

s.dumps({'user_id': self.id}): This creates a token by encoding the user ID (self.id) into a string.
.decode('utf-8'): Converts the token from bytes to a string format
"""

# verify_reset_token
"""
Purpose: Check if the token is valid and extract the user information.

s = Serializer(app.config['SECRET_KEY']): Same secret key used for token verification.

user_id = s.loads(token, salt='reset-password', max_age=expires_sec)['user_id']:
Decodes the token and extracts the data, and retrieves the user ID from the decoded data.

expires_sec=1800 means token expires in 1800 seconds (default 30 minutes).
salt ek extra security layer hai jo token ya password ko unique aur secure banata hai.
"""

# @staticmethod: Iss Decorator sa uss method/Function ko class se directly call kiya ja sakta hai bina class ke kisi object ko create kiye.
