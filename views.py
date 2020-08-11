import json

from flask import render_template, session, redirect, request, jsonify
from config import Config
from forms import RegistrationForm, LoginForm, OrderForm
from models import Category, Meal, db, User, Order, Association
from app import app
from random import shuffle
from datetime import datetime


@app.route('/')
def main():
    categories = db.session.query(Category).all()
    meals = db.session.query(Meal).all()
    shuffle(categories)
    return render_template("main.html", categories=categories, meals=meals)


@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    form = OrderForm()
    data = []
    sum = 0
    selected_meals = {}
    user_id = 1
    if 'data' in session:
        data = session['data']
        selected_meals = {int(key): int(value) for key, value in data.items() if value != 0}
        meals = db.session.query(Meal).filter(Meal.id.in_(selected_meals.keys())).all()
        data = []
        for meal in meals:
            sum += int(meal.price) * int(selected_meals[meal.id])
            data.append({'id': meal.id, 'title': meal.title, 'price': meal.price, 'qnt': selected_meals[meal.id]})
    if request.method == "POST":
        if 'logged_in' in session and session['logged_in']:
            form.name.data = session['name']
            form.email.data = session["username"]
            user_id = session['user_id']
        order = Order(date=datetime.now(), sum=sum, status='ordered', user_id=user_id, mail=form.email.data,
                      phone=form.phone.data, address=form.address.data)
        db.session.add(order)
        for key in selected_meals.keys():
            meal = db.session.query(Meal).filter(Meal.id == key).first()
            order.meals.append(meal)
        db.session.commit()
        for key, value in selected_meals.items():
            db.session.query(Association).filter(
            db.and_(Association.order_id == order.id, Association.meal_id == key)).update(
            {'counter': value})
        db.session.commit()
        return redirect('/order_done/')
    return render_template("cart.html", data=data, form=form)


@app.route('/addtocart/', methods=['GET', 'POST'])
def addtocart():
    if request.method == "POST":
        session['data'] = json.loads(request.data)
    return jsonify(True)


@app.route('/order_done/', methods=['GET', 'POST'])
def order_done():
    return render_template("ordered.html")


@app.route("/auth/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None
    if request.method == "POST":
        user = User.query.filter_by(mail=form.username.data).first()
        if user and user.password_valid(form.password.data):
            session["name"] = user.name
            session["username"] = user.mail
            session["user_id"] = user.id
            session['logged_in'] = True
            session['role'] = user.role
            return redirect("/")
        else:
            error = "Неверное имя или пароль"
    return render_template("auth.html", form=form, err=error, CLIENT_SECRET=Config.CAPTCHA_CLIENT_KEY)


@app.route('/logout/')
def logout():
    if 'username' in session:
        session["name"] = None
        session["username"] = None
        session["user_id"] = None
        session['logged_in'] = False
        session['role'] = None
    return redirect('/')


@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        user = db.session.query(User).filter(User.mail == form.username.data).first()
        if not user:
            user = User(name=form.name.data, mail=form.username.data, password=form.password.data, role='user')
            db.session.add(user)
            db.session.commit()
            session["name"] = user.name
            session["name"] = user.name
            session["username"] = user.mail
            session["user_id"] = user.id
            session["role"] = user.role
            session['logged_in'] = True
            return redirect('/')
    return render_template("register.html", form=form, CLIENT_SECRET=Config.CAPTCHA_CLIENT_KEY)


@app.route('/account/')
def account():
    if 'user_id' in session and session["user_id"]:
        id = session["user_id"]
        orders = db.session.query(Order).filter(Order.user_id == id).all()
        data = []
        month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'ноября',
                      'декабря']
        for order in orders:
            meals = db.session.query(Association).filter(Association.order_id == order.id).all()
            meals_list = []
            for item in meals:
                meals_list.append(
                    {'id': item.meal_id, 'title': item.meal.title, 'qnt': item.counter, 'price': item.meal.price,
                     'sum': item.counter * item.meal.price})
            data.append({'order_date': str(order.date.day)+' '+month_list[order.date.month]+' в '+order.date.strftime("%H:%M"),
                         'order_sum': order.sum, 'meals': meals_list})
        return render_template("account.html", data=data)
    return redirect('/auth/')
