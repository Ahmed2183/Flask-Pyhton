from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Post Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    submit = SubmitField('Post')


""" Descriptions """

# For flask_wtf: pip install flask flask-wtf

"""
After Installing New Packages Every Time You Need To: 
Update requirements.txt: pip freeze > requirements.txt
"""
