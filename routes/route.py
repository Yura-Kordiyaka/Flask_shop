from flask import render_template, request, redirect, session, url_for, flash
from User import User
from utilitis.check_file import *
from Image import Img
from werkzeug.utils import secure_filename
from main import app, db


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    form = request.form
    if request.method == "GET":
        return render_template('authorization.html')
    elif request.method == "POST":
        user = User(email=form['email'], password=form['password'], name=form['name'])
        db.session.add(user)
        db.session.commit()
        return redirect('Login')


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    image = Img.query.all()
    category = []
    for i in image:
        if i.category not in category:
            category.append(i.category)
    form = request.form
    if request.method == "GET":
        return render_template('Login.html')
    elif request.method == "POST":
        user = User.query.filter_by(email=form['email'], password=form['password']).first()
        if user:
            session['id'] = user.id
            session['name'] = user.name
            return render_template('user.html', category=category)
        else:
            error = '<h1>incorrect data</h1>'
            return render_template('Login.html', error=error)


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


@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    file = request.files.get('image')
    form = request.form
    if request.method == 'GET':
        return render_template('AddImage.html')
    if request.method == 'POST':
        if not file:
            return 'not upload file', 400
    if session['id']:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = app.config['UPLOAD_FOLDER'] + '/' + filename
            file.save("." + path)
            img = Img(user_id=session['id'], name=file.filename, img=path, cost=form['price'],
                      description=form['description'], name_of_product=form['name_of_product'],
                      category=form['category_of_product'])
            db.session.add(img)
            db.session.commit()
            return redirect(url_for('show_my_images'))


@app.route('/show_my_images', methods=['GET', 'POST'])
def show_my_images():
    image = Img.query.filter_by(user_id=session['id']).all()
    if request.method == 'GET':
        if image:
            return render_template('ShowImage.html', photo=image)
        else:
            return "<h1>you don't have photo</h1>", 400


@app.route('/show_all_images', methods=['GET', 'POST'])
def show_all_images():
    image = Img.query.all()
    if request.method == 'GET':
        if image:
            return render_template('ShowImage.html', photo=image)
        else:
            return "<h1>you don't have photo</h1>", 400


@app.route('/show_by_category/<id>', methods=['GET', 'POST'])
def show_by_category(id):
    image = Img.query.filter_by(category=id).all()
    if request.method == 'GET':
        if image:
            return render_template('show_category.html', category=image)
        else:
            return "<h1>you don't have photo</h1>", 400


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    form = request.form
    image = Img.query.filter_by(id=int(id)).first()
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for('show_my_images'))


@app.route('/editProduct/<int:id>', methods=['GET', 'POST'])
def editProduct(id):
    form = request.form
    image = Img.query.filter_by(id=int(id)).first()
    if request.method == 'GET':
        return render_template('editProduct.html', photo=image)
    if request.method == 'POST':
        if form['price']:
            image.cost = form['price']
        if form['description']:
            image.description = form['description']
        if form['name_of_product']:
            image.name_of_product = form['name_of_product']
        if form['category_of_product']:
            image.category = form['category_of_product']
        db.session.commit()
        return redirect(url_for('show_image'))
        # return "helllo"


@app.route("/logout")
def logout():
    session["name"] = None
    session["id"] = None
    return redirect("/")
