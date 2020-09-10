from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import MongoEngine
from delivery import app
db = MongoEngine(app)


class Category(db.Document):
    meta = {'collection': 'categories'}
    category_id = db.IntField(required=True)
    title = db.StringField(required=True)

    def __unicode__(self):
        return self.title


class Meal(db.Document):
    meta = {'collection': 'meals'}
    meal_id = db.IntField(required=True)
    title = db.StringField(required=True)
    price = db.IntField(required=True)
    description = db.StringField(required=True)
    picture = db.StringField(required=True)
    category_id = db.IntField(required=True)
    category = db.LazyReferenceField(Category)

    def __unicode__(self):
        return self.title


class MealWithCount(db.Document):
    meta = {'collection': 'meals_with_count'}
    meal = db.LazyReferenceField(Meal)
    count = db.IntField(required=True)


class Order(db.Document):
    meta = {'collection': 'orders'}
    date = db.DateTimeField(required=True)
    sum = db.IntField(required=True)
    status = db.StringField(required=True)
    user = db.LazyReferenceField('User')
    phone = db.StringField(required=True)
    address = db.StringField(required=True)
    meals = db.ListField(db.LazyReferenceField(MealWithCount))

    def __unicode__(self):
        return self.date


class User(db.Document):
    meta = {'collection': 'users'}
    name = db.StringField(required=True)
    mail = db.EmailField()
    password_hash = db.StringField()
    role = db.StringField()
    orders = db.ListField(db.LazyReferenceField(Order))

    def __unicode__(self):
        return self.mail

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)
