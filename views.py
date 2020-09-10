import json
import time
from flask import render_template, session, redirect, request, jsonify
from config import Config
from forms import RegistrationForm, LoginForm, OrderForm
from models import Category, Meal, User, Order, MealWithCount
from app import app
from datetime import datetime


def auth(user=None):
    if user:
        for k, v in {"name": user.name,  "username": user.mail, "role": user.role, "logged_in": True}.items():
            session[k] = v
    else:
        for key in session.keys():
            session.pop(key)


@app.route('/')
def main_page():
    categories = Category.objects.all()
    meals = Meal.objects.all()
    return render_template("main.html", categories=categories, meals=meals)


@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    form = OrderForm()
    data = []
    sum = 0
    selected_meals = {}
    user = User.objects.filter(name='guest').first()
    if 'data' in session:
        data = session['data']
        selected_meals = {int(key): int(value) for key, value in data.items() if value != 0 and key != ''}
        meals = Meal.objects(__raw__={"meal_id": {"$in": list(selected_meals.keys())}})
        data = []
        for meal in meals:
            sum += int(meal.price) * int(selected_meals[meal.meal_id])
            data.append({'meal_id': meal.meal_id, 'title': meal.title, 'price': meal.price, 'qnt': selected_meals[meal.meal_id]})
    if request.method == "POST":
        if 'logged_in' in session and session['logged_in']:
            form.name.data = session['name']
            form.email.data = session["username"]
            user = User.objects.filter(name=session['name']).first()
        order = Order(date=datetime.now(), sum=sum, status='ordered', user=user,
                      phone=form.phone.data, address=form.address.data)
        order.save()
        user.orders.append(order)
        user.save()
        for key, value in selected_meals.items():
            meal = MealWithCount(meal=Meal.objects.filter(meal_id=key).first(), count=value)
            meal.save()
            order.meals.append(meal)
        order.save()
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
        user = User.objects.filter(mail=form.username.data).first()
        if user and user.password_valid(form.password.data):
            auth(user)
            return redirect("/")
        else:
            error = "Неверное имя или пароль"
    return render_template("auth.html", form=form, err=error, CLIENT_SECRET=Config.CAPTCHA_CLIENT_KEY)


@app.route('/logout/')
def logout():
    if 'username' in session:
        auth()
    return redirect('/')


@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.objects.filter(mail=form.username.data).first()
        if not user:
            user = User(name=form.name.data, mail=form.username.data, role='user')
            user.password = form.password.data
            user.save()
            auth(user)
            return redirect('/')
    return render_template("register.html", form=form, CLIENT_SECRET=Config.CAPTCHA_CLIENT_KEY)


@app.route('/account/')
def account():
    if 'logged_in' in session and session["logged_in"]:
        user = User.objects.filter(name=session['name']).first()
        orders = user.orders
        data = []
        month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'ноября',
                      'декабря']
        for order in orders:
            order = order.fetch()
            meals = order.meals
            meals_list = []
            for item in meals:
                item = item.fetch()
                meal = item.meal.fetch()
                meals_list.append(
                    {'id': meal.meal_id, 'title': meal.title, 'qnt': item.count, 'price': meal.price,
                     'sum': item.count * meal.price})
            data.append({'order_date': str(order.date.day)+' '+month_list[order.date.month]+' в '+order.date.strftime("%H:%M"),
                         'order_sum': order.sum, 'meals': meals_list})
        return render_template("account.html", data=data[::-1])
    return redirect('/auth/')

