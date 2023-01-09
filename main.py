from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://yura:parol@localhost:3306/avrorization'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
db.init_app(app)

with app.app_context():
    from routes.route import *
    from User import *
    from Image import *
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
