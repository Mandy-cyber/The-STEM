import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Messages, MailingList, Resource, SimilarPeople
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__) 

# REMEMBER AMANDA: you can pass variables like render_template("login.html", myVariable="Testing123")
# and then in the html file put {{myVariable}} and it will show the variable value

#--------------------------------------------------------------------------------------------
# LOGIN

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ allow a user to login to their account
    * Requeries if the user or email does not exist,
      or if the password was incorrect

    Args: 
        None
    Returns:
        redirect (function): to take user to the home page
        render_template (function): to take user to the login html page
    """
    # a user will only get 4 attempts to login,
    # anymore and they will not have the option to do so
    wrong_attempts = 0
    
    if request.method == 'POST':
        # get info from the form
        username = request.form.get('username')
        password = request.form.get('password')
        # find the user
        user = User.query.filter_by(username=username).first()
        if user: #if user exists
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                #bring user to the home page
                # TODO make views.home
                return redirect(url_for('views.home'))
            else:
                # purposefully don't specify which one, for security purposes
                flash('Incorrect username or password', category='error')
        else:
            flash("Incorrect username or password", category='error')
            
    return render_template("login.html", user=current_user)


#--------------------------------------------------------------------------------------------
# LOGOUT

@auth.route('/logout')
@login_required
def logout():
    """ logs out the current user
    Args:
        None
    Returns:
        redirect (function): redirects the user back to the login page
    """
    logout_user()
    return redirect(url_for('auth.login'))



#--------------------------------------------------------------------------------------------
# SIGNUP

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """ let's a user create an account
    * Requeries if:
        - the fullname does not have at least 2 words
        - the username is already taken
        - the email already exists or is invalid
        - the passwords do not match or the password
          is too short

    Args:
        None
    
    Returns:
        redirect (function): redirects the user to the home page
        render_template (function): displays the signup page
    """
    if request.method == 'POST':
        # getting info from signup form
        fullName = request.form.get('fullName')
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # regex for checking validity of emails from:
        # https://www.c-sharpcorner.com/article/how-to-validate-an-email-address-in-python/
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

        # validation checks
        username_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if len(list(fullName)) < 2:
            flash('Please input your first and last name correctly.', category='error')
        elif username_exists:
            flash('Sorry, this username is taken!', category='error')
        elif email_exists:
            flash('An account is already associated with this email.', category='error')
        elif not re.search(regex, email):
            flash('Invalid email address. Please try again.', category='error')
        elif password1 != password2:
            flash('Passwords do not match. Please try again.', category='error')
        elif len(password1) < 8:
            flash('Password should be at least 8 characters. Please try again', category='error')
        else:
            # add user to database
            new_user = User(fullName=fullName, 
                            username=username,
                            email=email, 
                            # hash and salt password before adding it to the database
                            password=generate_password_hash(password1,method='sha256', salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home')) # go to the home page
    
    return render_template('signup.html', user=current_user)
