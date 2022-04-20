from datetime import datetime
from coffeeCalc import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='client', lazy=True)
    notes = db.relationship('Note', backref='client', lazy=True)

    def __repre__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_country = db.Column(db.String(100), nullable=False)
    origin_to_port_distance = db.Column(db.String(100), nullable=False)
    end_location = db.Column(db.String(100), nullable=False)
    port_to_client_distance = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.String(100), nullable = False)
    carbon_cost = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    note_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Note('{self.content}')"

class Country(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    region = db.Column(db.Text, nullable = False)
    port = db.Column(db.Text, nullable = False)
    region_to_port_cost = db.Column(db.Integer, nullable = False)
    port_to_UK_cost = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Country('{self.title}')"
    