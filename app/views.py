"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from werkzeug.utils import secure_filename
from app.models import Movie
from app.forms import MovieForm
from flask import render_template, request, jsonify, send_file, send_from_directory
from flask_wtf.csrf import generate_csrf
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        poster = request.files.get('poster') # use .get() to check if poster is in the request

        # Check if poster was included in the request before attempting to save it
        filename = secure_filename(poster.filename)
        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        poster.save(os.path.join(UPLOAD_FOLDER, filename))


        # Create a new movie object and save it to the database
        movie = Movie(title=title, description=description, poster=filename if poster else None) # if poster is not included, set filename to None
        db.session.add(movie)
        db.session.commit()

        # Return the success message and movie details
        response = {
            'message': 'Movie Successfully added',
            'title': movie.title,
            'poster': movie.poster,
            'description': movie.description
        }
        return jsonify(response), 201

    # Return the form validation errors
    errors = form_errors(form)
    return jsonify(errors=errors), 400

@app.route('/api/v1/posters/<filename>', methods=['GET'])
def get_poster(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/api/v1/movielist', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify({'movies': [{'id': movie.id,
                                'title': movie.title,
                                'description': movie.description,
                                'poster': f"/api/v1/posters/{movie.poster}"} for movie in movies]})



@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404