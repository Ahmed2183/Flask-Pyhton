import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f"{os.environ.get('SQLALCHEMY_DATABASE_URI')}"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")


""" Descriptions """

# os.path.abspath(os.path.dirname(__file__)):
"""
Yeh line aapko current file ke directory ka absolute path deti hai. 
"""

# load_dotenv() :Load environment variables from .env file

# SECRET_KEY and SQLALCHEMY_DATABASE_URI i set in System Environment Variable and get from there

# MAIL_USERNAME and MAIL_PASSWORD get from .env file

# .env & System Environment Variable
"""
Use .env for local, non-sensitive configurations and system environment variables for sensitive or production settings 
to keep environments secure and flexible.
"""

# SECRET_KEY:
""" 
To use forms we need to set a SECRET KEY for our application, SECRET KEY will protect against modifying cookies and cross-site forgery attacks and things like that
For random string character use the secrets built-in module, Type in cmd/terminal:
$ python
>>> import secrets
>>> secrets.token_hex(16)    -->Means provide me 16 random string characters
>>> exit()
"""

# DataBase Connection
"""
'SQLALCHEMY_DATABASE_URI' setting ke zariye aap SQLAlchemy ko batate hain ke kaunsa database use karna hai.
'sqlite:///{basedir}/site33.db' ka matlab hai ke aap SQLite database use kar rahe hain aur uska file name site33.db hai.
"""

# Mail
"""
For Sending Mail:

app.config['MAIL_SERVER'] = 'smtp.googlemail.com':
Yeh line aapko batati hai ke kon sa mail server use ho raha hai. Yahan smtp.googlemail.com use ho raha hai, jo ke Google ka SMTP(Simple Mail Transfer Protocol) server hai.

app.config['MAIL_PORT'] = 587:
Yeh line port number set karti hai jahan se mail server se connection banaya jata hai. 587 Gmail's secure SMTP port ha
Gmail's secure SMTP ports are 465 and 587: Port 465 is secured via SSL (Secure Sockets Layer), and 578 works over TLS (Transport Layer Security).
We use TLS (Transport Layer Security)

app.config['MAIL_USE_TLS'] = True  --> We use TLS (Transport Layer Security) which is 587

app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USER")   -->Set Email Account Username, get from environment variable 
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASS")   -->Set Email Account Password, get from environment variable 
"""
