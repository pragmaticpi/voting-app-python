from votingapp import db

# User Table Schema
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    has_voted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User('{self.username}')"

# Candidate Table Schema
class CandidateVotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(20), unique=True, nullable=False)
    votes = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, candidate_name):
        self.candidate_name = candidate_name

    def __repr__(self):
        return f"CandidateVotes('{self.candidate_name}', '{self.votes}')"
