from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://yura:parol@localhost:3306/avrorization'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

with app.app_context():
    from utilitis.rout import *
    from User import *

    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
