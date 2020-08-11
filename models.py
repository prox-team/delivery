from flask_sqlalchemy import SQLAlchemy, event
from sqlalchemy import event
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Association(db.Model):
    __tablename__ = 'orders_meals_association'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), primary_key=True)
    counter = db.Column(db.Integer, default=0)
    order = db.relationship("Order", backref="order_associations")
    meal = db.relationship("Meal", backref="meal_associations")


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mail = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    meals = db.relationship("Meal", secondary="orders_meals_association")


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    picture = db.Column(db.String(15), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    mail = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False)
    orders = db.relationship('Order')

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)


