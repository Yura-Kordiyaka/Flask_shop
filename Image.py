from main import db


class Img(db.Model):
    _tablname_ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    cost = db.Column(db.Integer, nullable=False)
    name_of_product = db.Column(db.String(100))
    category = db.Column(db.Text, nullable=False)


