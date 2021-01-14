from flask_mongoengine import BaseQuerySet
from datetime import datetime
from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from app import login, db
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Document):
    username = db.StringField(max_length=64, unique=True, required=True)
    email = db.StringField(max_length=120, unique=True, required=True)
    password_hash = db.StringField(max_length=120)
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    about_me = db.StringField(max_length=150)
    last_seen = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8"))
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    meta = {'collection': 'user', 'queryset_class': BaseQuerySet}


class Post(db.DynamicDocument):
    title = db.StringField(max_length=50)
    body = db.StringField()
    timestamp = db.DateTimeField(default=datetime.datetime.utcnow)
    author = db.StringField()

    meta = {
        'allow_inheritance': True,
        'collection': 'post',
        'queryset_class': BaseQuerySet
        }

    def __repr__(self):
        return f"Post('{self.title}', '{self.timestamp}')"


# pk == primary key
@login.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
