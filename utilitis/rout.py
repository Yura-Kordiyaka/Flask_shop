from flask import Flask, render_template, request, redirect
from User import User
from main import app, db


@app.route('/', methods=['GET', 'POST'])
def authorization():
    form = request.form
    if request.method == "GET":
        return render_template('authorization.html')
    elif request.method == "POST":
        user = User(email=form['email'], password=form['password'], name=form['name'])
        db.session.add(user)
        db.session.commit()
        return '<h1>you have successfully logged in</h1>'


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    form = request.form
    if request.method == "GET":
        return render_template('Login.html')
    elif request.method == "POST":
        user = User.query.filter_by(email=form['email'], password=form['password']).first()
        if user:
            return render_template('user.html', user_name=user.name)
        else:
            return '<h1>incorrect data</h1>'


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = request.form
    if request.method == "GET":
        return render_template('Change_password.html')
    elif request.method == "POST":
        user = User.query.filter_by(email=form['email'], password=form['password_old']).first()
        if user:
            user.set_password(form['password_new'])
            db.session.commit()
            return "<h1>password successfully changed</h1>"
        else:
            return "<h1>Incorrect data</h1>"
