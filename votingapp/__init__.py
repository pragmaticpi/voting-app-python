from flask import Flask
from votingapp.config import Config
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin

# Initializing flask application
app = Flask(__name__)

#Loading config properties for sqlite database
app.config.from_object(Config)

# secret key for session
app.config['SECRET_KEY'] = '3bf6d5030d340a64f3afff54af81f38b'

# Initializing database
db = SQLAlchemy(app)

from votingapp import routes
from votingapp.models import User, CandidateVotes
from votingapp.admin import AdminView, MyModelView

# Adding both models to the admin view
admin = Admin(app, name='Admin', index_view=MyModelView(CandidateVotes, db.session, url='/admin'))
admin.add_view(AdminView(User, db.session))
