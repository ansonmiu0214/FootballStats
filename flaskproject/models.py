from flaskproject import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favourite_team = db.Column(db.String(100), default='Manchester United')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.favourite_team}')"


class Countries(db.Model):
    name = db.Column(db.String(120), primary_key=True)
    flag_url = db.Column(db.String(1000))
    country = db.relationship('Competitions', backref='cname', lazy=True)

    def __repr__(self):
        return f"Countries('{self.name}','{self.flag_url}')"


class Competitions(db.Model):
    compid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    logo = db.Column(db.String(300))
    country = db.Column(db.String(300), db.ForeignKey('countries.name'))

    def __repr__(self):
        return f"Competitions('{self.compid}','{self.name}','{self.logo}')"


class Teams(db.Model):
    teamid = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(300))
    country = db.Column(db.String(300), db.ForeignKey('countries.name'))
    team_logo_url = db.Column(db.String(300))
    stadium_id = db.Column(db.Integer)
    stadium_name = db.Column(db.String(300))
    stadium_capacity = db.Column(db.Integer)
    stadium_image = db.Column(db.String(300))
    compid = db.Column(db.Integer, db.ForeignKey('competitions.compid'))
    competition = db.relationship('Competitions', backref='teams', lazy=True)

    def __repr__(self):
        return f"Teams('{self.teamid}','{self.team_logo_url}','{self.stadium_id}','{self.country}','{self.stadium_name}','{self.stadium_capacity}','{self.stadium_image}','{self.compid}','{self.team_name}')"
