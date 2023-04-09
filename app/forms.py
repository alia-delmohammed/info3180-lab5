# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[
        DataRequired(message='Please provide a movie title.')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message='Please provide a description of the movie.')
    ])
    poster = FileField('Movie Poster', validators=[
        FileRequired(message='Poster is required'),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
