import re
from flask import Blueprint, jsonify, render_template, flash, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Messages, MailingList
from . import db

views = Blueprint('views', __name__) 


#-------------------------------------------------------------------------#
# HOME PAGE

@views.route('/')
def home():
    """ show the website's home page
    Args:
        None
    Returns:
        render_template (function): displays the home's html page
    """
    return render_template("home.html", user=current_user)


#-------------------------------------------------------------------------#
# ABOUT PAGE

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)


#-------------------------------------------------------------------------#
# CONTACT PAGE

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    """ show's the page for the user to contact us
    * Requeries if the email address is invalid or the message
      is too short.

    Args:
        None
    Returns:
        redirect (function): will redirect to the home page
        render_template (function): will show the contact page
    """
    # regex for checking validity of emails from:
    # https://www.c-sharpcorner.com/article/how-to-validate-an-email-address-in-python/
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

    if request.method == 'POST':
        # get info from form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # checking validity
        if len(message) < 10:
            flash("That's a short note... don't be shy!", category='info')
        elif not re.search(regex, email):
            flash("Invalid email address. Try again.", category='error')
        else:
            # adding the new message to the database
            new_message = Messages(name=name, email=email, message=message)
            db.session.add(new_message)
            db.session.commit()
            flash('A carrier pigeon is on its way now!', category='success')
            return redirect(url_for('views.home')) #back to the home page

    return render_template("contact.html", user=current_user)

#-------------------------------------------------------------------------#
# CHOOSE YOUR PATH PAGE

@views.route('/your-path')
def choose_your_path():
    return render_template("chooseyourpath.html", user=current_user)


#-------------------------------------------------------------------------#
# RESOURCES PAGE

@views.route('/resources')
def resources():
    return render_template("resources.html", user=current_user)

