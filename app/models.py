#Eigenentwicklung: 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login

#Eigenentwicklung: Die User und Server klassen für die Datenbank, enthält die Funktion der Passwortverschlüsselung sowie Überprüfung.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servername = db.Column(db.String(50), unique=True)
    ip = db.Column(db.String(50), unique=True)
    os = db.Column(db.String(50))

    def __repr__(self):
        return '<Server %r>' % self.servername  
    def serialize(self):
        return {
        'id': self.id,
        'servername': self.servername,
        'ip': self.ip,
        'os': self.os,
        }