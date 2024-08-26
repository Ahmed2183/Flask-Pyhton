from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500


""" Descriptions """

# @errors.app_errorhandler decorator is used to define custom error handlers for your Flask application.

# Empty __init__.py files in folder Why?
"""
In Python, a package is a directory that contains an __init__.py file. This file tells Python that the directory should be treated as a package, 
which can contain modules and sub-packages

If the directory does not contain an __init__.py file, Python will not recognize it as a package. 
You cannot directly import modules from this directory.

Note: Modules in Python are files containing Python code that define functions, classes, and variables.
"""
