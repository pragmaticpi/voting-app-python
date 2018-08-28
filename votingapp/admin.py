from flask_admin.contrib.sqla import ModelView

from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response

from flask_basicauth import BasicAuth

from votingapp import app

# Basic Auth for admin
basic_auth = BasicAuth(app)

# Username & Password for basic auth
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

# Custom Model View to present candidate votes model as home page in Admin
class MyModelView(ModelView):
   def __init__(self, model, session, *args, **kwargs):
        super(MyModelView, self).__init__(model, session, *args, **kwargs)
        self.static_folder = 'static'
        self.endpoint = 'admin'
        self.name = 'CandidateVotes'

# Check for authentication
class AdminView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))
