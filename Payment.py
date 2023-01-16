from main import db


class Payment(db.Model):
    _tablname_ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    count = db.Column(db.Integer)
    suma = db.Column(db.Integer)
    address = db.Column(db.Text)
    phone_number = db.Column(db.String(40))
    credit_card = db.Column(db.String(100))
