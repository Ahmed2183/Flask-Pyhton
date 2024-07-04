#For flask: pip install flask
"""
To Check Flask Install Correctly, Type in cmd/terminal:
$ python
>>> import flask
>>> exit()
"""

"""
To run any Python file, you first need to set the environment variable for that file:
set FLASK_APP=flaskBlog.py

By setting the environment variable, you can use simple commands like to start your application: 
flask run  

Without setting this, you would have to specify the file each time, such as: 
flask --app flaskBlog.py run.
"""

"""
Note:-
Debug Mode: In Debug Mode Changes Reloaded Automatically And We Didn't Have To Restart That Web Server

To run any Python file, you first need to set the environment variable for that file:
set FLASK_APP=flaskBlog.py

To run that file in debug mode:
set FLASK_DEBUG=1

Run the file with the command:
flask run
"""

"""
To run application directly using python
"""

from flask import Flask, render_template, url_for           #-->render_template is for html files and url_for is for css files
from forms import RegistrationForm, LoginForm               #-->import from forms.py


app = Flask(__name__)                   #-->Flask class ko use karte hue ek naya instance banaya ja raha, Agar yeh file directly run ho rahi hai to __name__ ki value __main__ hoti hai. 
                                        #Agar is file ko kisi aur file se import kiya jaye, to __name__ us module ka naam hota hai. 'app' means Ek naya Flask application.

""" 
To use forms we need to set a SECRET KEY for our application, SECRET KEY will protect against modifying cookies and cross-site forgery attacks and things like that
For random string character use the secrets built-in module, Type in cmd/terminal:
$ python
>>> import secrets
>>> secrets.token_hex(16)    -->Means provide me 16 random string characters
>>> exit()
"""
app.config['SECRET_KEY'] = '03ea24882b4a5cfad1af4b8bb2a2fdd7'

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

# @app.route("/register")
# def about():
#     form = RegistrationForm()
#     return render_template("register.html", title='Register', form=form)

# @app.route("/login")
# def about():
#     form = LoginForm()
#     return render_template("login.html", title='Login', form=form)



""" 
Note:-
If you dont want to set the environment variable then there's another way to run our application directly using python:
python flaskBlog.py

Ye below condition check karti hai ke agar ye script directly run ho rahi hai (matlab, import nahi ho rahi dusri file se), 
toh niche wali lines execute hongi. 
"""

#To use python add below code
if __name__ == '__main__':
    app.run(debug=True)    #-->debug=True means run app in Debug Mode
