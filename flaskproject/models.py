from flaskproject import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favourite_team = db.Column(db.String(100), default='Manchester United')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.favourite_team}')"

class Countries(db.Model):
    Name = db.Column(db.String(120), primary_key=True)
    Flag = db.Column(db.String(1000))

    def __repre__(self):
        return f"Countries('{self.Name}','{self.Flag}')"