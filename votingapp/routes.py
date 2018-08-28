from flask import Flask, render_template, flash, redirect, session, request, url_for, logging

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from votingapp import app, db
from votingapp.forms import RegistrationForm, LoginForm
from votingapp.models import User, CandidateVotes

# Creating tables and populating candidate data on first request send to the application
@app.before_first_request
def setup():
    # Drop tables if exists
    db.drop_all()

    # Creating tables
    db.create_all()

    #Inserting rows in candidatevotes table
    db.session.add(CandidateVotes(candidate_name='Candidate A'))
    db.session.add(CandidateVotes(candidate_name='Candidate B'))
    db.session.add(CandidateVotes(candidate_name='Candidate C'))
    db.session.add(CandidateVotes(candidate_name='Candidate D'))
    
    # Commit
    db.session.commit()

# Index/Home Route
@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')

# About Route
@app.route("/about")
def about():
    return render_template('about.html')

# Register Route
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():

        username=form.username.data
        user = User.query.filter_by(username=username).first()

        # Check if username exists
        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('register')) 
        else:
            # Hashing the password
            password=generate_password_hash(form.password.data)

            # Inserting new user data
            user = User(username=username, password=password)

            db.session.add(user)
            db.session.commit()

            flash('Registration successful', 'success')
            return redirect(url_for('index'))

    return render_template('register.html', form=form)

# Login Route
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user:
            password_hash = user.password

            # Compare password
            if check_password_hash(password_hash, password):
                session['logged_in'] = True
                session['username'] = username

                flash('Login successful', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = "Password incorrect"
                return render_template('login.html', error=error, form=form)
        else:
            error = "Username does not match"
            return render_template('login.html', error=error, form=form)

    return render_template('login.html', form=form)

# Check if user is already logged in and trying to access dashboard
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Not authorized, Login or register to view', 'danger')
            return redirect(url_for('login'))
    return wrap

# Dashboard Route
@app.route("/dashboard", methods=['GET', 'POST'])
# Only Logged in users can access dashboard page
@is_logged_in
def dashboard():
    if request.method == 'POST':

        # Check if user has selected any candiate
        if 'candidate' in request.form:
            # Check if user has already submitted the vote
            if User.query.filter_by(username=session['username']).first().has_voted:
                flash("You already voted for the best candidate", 'danger')
                return redirect(url_for('index'))
            else:
                candidate_name = request.form['candidate']

                # Increasing the vote by 1
                voted_candidate = CandidateVotes.query.filter_by(candidate_name=candidate_name).first()
                voted_candidate.votes = voted_candidate.votes + 1
                
                # Setting true that user has submitted the vote
                user_voted = User.query.filter_by(username=session['username']).first()
                user_voted.has_voted = True
                
                db.session.commit()

                flash("Thank you for the vote", 'success')
                return redirect(url_for('index'))
        else:
            flash('Please select a candidate to vote', 'danger')
            return redirect(url_for('dashboard'))
    else:
        # Fetching the candidates name in case of GET request
        candidate_list = CandidateVotes.query.all()
        return render_template('dashboard.html', candidate_list=candidate_list)

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    flash("Logout successfully", 'success')
    return redirect(url_for('index'))
