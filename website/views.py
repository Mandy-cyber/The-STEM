import re
import base64
from io import BytesIO
import urllib.request
import requests
from flask import Blueprint, jsonify, render_template, flash, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from PIL import Image
from .models import User, Messages, MailingList, Resource, SimilarPeople
from . import db
from .findres import find_resources
from .wildcard import find_similar_people

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
    # TODO allow user to press button to query new results and reshuffle resources
    # find_resources()
    resources = Resource.query.all()
    return render_template("resources.html", user=current_user, resources=resources)


#-------------------------------------------------------------------------#
# PROFILE PAGE

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # get info from forms
        wildcard = request.form.get('wildcard')
        edulevel = request.form.get('edulevel')

        if wildcard != None:
            # checking validity
            if len(wildcard) < 4:
                flash("Hmm, that's a bit too short. Try another word!", category='info')
            else:
                flash("Wildcard noted...", category='success')
                current_user.wildFactor = wildcard
                db.session.commit()
                img_links = find_similar_people(wildcard=wildcard, current_user=current_user)
                ppl = SimilarPeople.query.filter_by(user_id=current_user.id).all()

                # IMAGE LOADING, SAVING, & ENCRYPTION/DECRYPTION
                #-------------------------------------------------#
                ## Will fix this in the future!
                # images = []
                # for person in ppl:
                #     lnk = person.lnk
                #     response = requests.get(lnk)
                #     # urllib.request.urlretrieve(lnk)
                #     im = Image.open(BytesIO(response.content))
                #     # data = BytesIO()
                #     # im.save(im, "JPEG") # save img in-memory
                #     encoded_img_data = base64.b64encode(im.getvalue()) # encode the img
                #     images.append(encoded_img_data.decode('utf-8'))

                links = []
                for person in ppl:
                    lnk = person.lnk
                    links.append(lnk)

                return render_template("profile.html", user=current_user, links=links)
        else:
            if edulevel == None:
                flash("Please provide information before pressing submit <3", category='error')
            else:
                flash("Education level updated successfully.", category='success')
                current_user.eduLevel = str(edulevel)
                db.session.commit()
                return redirect(url_for('views.resources'))
            
    ppl = SimilarPeople.query.filter_by(user_id=current_user.id).all()
    for person in ppl:
        lnk = person.lnk

    # IMAGE LOADING, SAVING, & ENCRYPTION/DECRYPTION
    # images = []
    links = []
    for person in ppl:
        lnk = person.lnk
        links.append(lnk)

    # IMAGE LOADING, SAVING, & ENCRYPTION/DECRYPTION
    #-------------------------------------------------#
    ## Will fix this in the future!
    # images = []
    # for person in ppl:
    #     lnk = person.lnk
    #     response = requests.get(lnk)
    #     # urllib.request.urlretrieve(lnk)
    #     im = Image.open(BytesIO(response.content))
    #     # data = BytesIO()
    #     # im.save(im, "JPEG") # save img in-memory
    #     encoded_img_data = base64.b64encode(im.getvalue()) # encode the img
    #     images.append(encoded_img_data.decode('utf-8'))

    # user_info = User.query.filter_by(id=current_user.id).first()
    # print(user_info.eduLevel)
    return render_template("profile.html", user=current_user, links=links)