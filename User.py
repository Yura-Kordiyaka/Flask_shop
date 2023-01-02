from main import db


class User(db.Model):
    _tablname_ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    @property
    def serialize(self):
        return {
            'Hello': self.name
        }

    def set_password(self, password):
        self.password = password
        return self.password
