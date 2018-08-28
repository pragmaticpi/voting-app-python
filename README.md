# voting-app-python

The application is a basic voting application written in python with Flask as the web framework. SQLite is used as the database which will be stored as a file in project structure.

* Jinja2 as template engine.
* Flask-SQLAlchemy as ORM tool.
* Flask-Admin to generate admin page.
* Flask-BasicAuth for authentication on admin page only which is separate  	 from normal user login.
* Flask-WTF for generating forms. 
* Werkzeug utility library for password hashing.

## Routes:-

Method	| Path	| Description
------------- | ------------------------- | -------------
GET	| / or /home	| Home Page	
GET	| /about	| About Page
GET, POST	| /register	| User Registration
GET, POST | /login	| User Login
GET, POST	| /dashboard	| Voting Dashboard
POST	| /logout		| User Logout

## Setting Up:-

Make sure you have Python 3+ installed on your system.

### Setup the virtual environment
    
    virtualenv voting_env --python=python3

### Install the dependencies
	    
   	pip install -r requirements.txt

### Run the application

   	python app.py

   The application can now be accessed at http://localhost:5000
