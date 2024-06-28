from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from datetime import datetime
from time import time

# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.Unicode(255), nullable=False,
                      server_default=u'', unique=True)
    confirmed_at = db.Column(db.DateTime())
    password_hash = db.Column(db.String(255), nullable=False, server_default='')
    # User information
    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='0')
    # User information
    registry = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # Admin
    admin = db.Column(db.Boolean())


    def is_admin(self):
        return self.admin

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Flask - Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Required for administrative interface
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.get(id)


# Flask-Login profile loader function @login_required
@login.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

