from flask import Blueprint, jsonify, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import User
from . import db

views = Blueprint('views', __name__) 

@views.route('/')
def home():
    """ show the website's home page
    Args:
        None
    Returns:
        render_template (function): displays the home's html page
    """
    return render_template("home.html", user=current_user)