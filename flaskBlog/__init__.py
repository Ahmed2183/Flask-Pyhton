from flask import Flask           
from flask_sqlalchemy import SQLAlchemy              
from flask_bcrypt import Bcrypt
from flask_login import LoginManager                       
import os

app = Flask(__name__)                   
app.config['SECRET_KEY'] = '03ea24882b4a5cfad1af4b8bb2a2fdd7'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir}/site.db"  
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'          
login_manager.login_message_category = 'info'          

from flaskBlog import routes



""" Description """

#render_template is for html files, url_for is for css files, flash is for alert messages

#app = Flask(__name__) :
"""
Flask class ko use karte hue ek naya instance banaya ja raha, Agar yeh file directly run ho rahi hai to __name__ ki value __main__ hoti hai. 
Agar is file ko kisi aur file se import kiya jaye, to __name__ us module ka naam hota hai. 'app' means Ek naya Flask application.
"""

#SECRET_KEY:
""" 
To use forms we need to set a SECRET KEY for our application, SECRET KEY will protect against modifying cookies and cross-site forgery attacks and things like that
For random string character use the secrets built-in module, Type in cmd/terminal:
$ python
>>> import secrets
>>> secrets.token_hex(16)    -->Means provide me 16 random string characters
>>> exit()
"""

#DataBase Connection
"""
'SQLALCHEMY_DATABASE_URI' setting ke zariye aap SQLAlchemy ko batate hain ke kaunsa database use karna hai.
'sqlite:///{basedir}/site.db' ka matlab hai ke aap SQLite database use kar rahe hain aur uska file name site.db hai.
"""

#db = SQLAlchemy(app):
""" 
SQLAlchemy: This is SQLAlchemy Database instance, means SQLAlchemy ko Flask application ke saath initialize kar rahe hain, taake aap database operations easily perform kar sakein.
""" 

#import routes after creation of db variable

#bcrypt = Bcrypt(app):                  -->We create bcrypt instance
""" 
Bcrypt: For Hashed Password
"""

#login_manager = LoginManager(app):      -->We create login_manager instance
"""
LoginManager: To handle user session management aur authentication. To implement login aur logout functionalities
"""

#login_manager.login_view = 'login'          
"""
'login' is our Login Funtion of login route, this line means jab koi user jo login nahi hua, kisi protected route ko access karne ki koshish kare, to usay automatically login page par redirect kiya jaye.
Jis routes ka sath @login_required  decorator use hoga wo protected route ban jai ga
"""

#login_manager.login_message_category = 'info'
"""
Kisi protected route ko bina login kia jo error message show hota ha yai line uski styling ha jesa info, danger, primary etc
"""          