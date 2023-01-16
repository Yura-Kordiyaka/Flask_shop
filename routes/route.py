from flask import render_template, request, redirect, session, url_for, flash
from User import User
from Payment import Payment
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
            flash('you input incorrect data', 'error')
            return render_template('Login.html')


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
    image = Img.query.all()
    category = []
    for i in image:
        if i.category not in category:
            category.append(i.category)
    image = Img.query.filter_by(user_id=session['id']).all()
    if request.method == 'GET':
        if image:
            return render_template('ShowImage.html', photo=image, category=category)
        else:
            return render_template('ShowImage.html', count=0)


@app.route('/show_all_images', methods=['GET', 'POST'])
def show_all_images():
    image = Img.query.all()
    if request.method == 'GET':
        if image:
            return render_template('ShowImage.html', photo=image)
        else:
            return render_template('ShowImage.html')


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
        return redirect(url_for('show_my_images'))
        # return "helllo"


@app.route("/home")
def home():
    return render_template('user.html')


@app.route('/add_to_basket/<int:id>', methods=['GET', 'POST'])
def add_to_basket(id):
    if not session.get('cart'):
        session['cart'] = []
    j = 0
    if session['cart']:
        for i in session['cart']:
            if i['product_id'] == id:
                i['qty'] += 1
                j += 1
        if j == 0:
            session["cart"].append(dict({'product_id': id,
                                         'qty': 1}))

    else:
        session["cart"].append(dict({'product_id': id, 'qty': 1}))
    return redirect(url_for('show_all_images'))


@app.route('/delete_from_basket/<int:id>', methods=['GET', 'POST'])
def delete_from_basket(id):
    for i in range(len(session['cart'])):
        if session['cart'][i]['product_id'] == id:
            session['cart'].pop(i)
    return redirect(url_for('show_my_basket'))


@app.route('/show_my_basket', methods=['GET', 'POST'])
def show_my_basket():
    basket = []
    product1 = {}
    suma = 0
    if request.method == 'GET':
        if session['cart']:
            for i in session['cart']:
                img = Img.query.filter_by(id=i['product_id']).first()
                if img:
                    product1 = ({'count': i['qty'],
                                 'product': img})
                    basket.append(dict(product1))
            for i in basket:
                suma += i['count'] * i['product'].cost

            return render_template('Basket.html', photo=basket, suma=suma)
        else:
            return render_template('Basket.html', photo=None, suma=0)
    if request.method == 'POST':
        return 'hello'


@app.route('/Payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'GET':
        return render_template('Payment.html')
    if request.method == 'POST':
        form = request.form
        for i in session['cart']:
            img = Img.query.filter_by(id=i['product_id']).first()
            payment = Payment(user_id=session['id'], product_id=img.id, count=i['qty'],
                              suma=i['qty'] * img.cost, address=form['address'],
                              phone_number=form['phone_number'], credit_card=form['credit_card'])
            db.session.add(payment)
        db.session.commit()
        session['cart'] = None
        flash('payment has done successfully', 'success')
        return redirect(url_for('home'))


@app.route('/My_cabinet', methods=['GET', 'POST'])
def My_cabinet():
    my_product = Payment.query.all()
    list_product = []
    suma = 0
    for i in my_product:
        img = Img.query.filter_by(id=i.product_id).first()
        if img.user_id == session['id']:
            list_product.append({'my_product': img,
                                 'number_of_phone': i.phone_number,
                                 'count': i.count})
            suma += img.cost * i.count
    if len(list_product) != 0:
        return render_template('My_cabinet.html', photo=list_product, suma=suma)
    else:
        return render_template('My_cabinet.html', photo=None, suma=suma)


@app.route("/logout")
def logout():
    session["name"] = None
    session["id"] = None
    session['cart'] = None
    return redirect("/")
