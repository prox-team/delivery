from werkzeug.security import generate_password_hash, check_password_hash
from delivery import db


class Category(db.Document):
    meta = {'collection': 'categories', 'allow_inheritance': True}
    category_id = db.IntField(required=True)
    title = db.StringField(required=True)

    def __unicode__(self):
        return self.title


class Meal(db.Document):
    meta = {'collection': 'meals', 'allow_inheritance': True}
    meal_id = db.IntField(required=True)
    title = db.StringField(required=True)
    price = db.IntField(required=True)
    description = db.StringField(required=True)
    picture = db.StringField(required=True)
    category_id = db.IntField(required=True)
    category = db.ReferenceField(Category)

    def __unicode__(self):
        return self.title


class MealWithCount(db.Document):
    meta = {'collection': 'meals_with_count', 'allow_inheritance': True}
    meal = db.ReferenceField(Meal)
    count = db.IntField(required=True)


class Order(db.Document):
    meta = {'collection': 'orders', 'allow_inheritance': True}
    date = db.DateTimeField(required=True)
    sum = db.IntField(required=True)
    status = db.StringField(required=True)
    user = db.ReferenceField('User')
    phone = db.StringField(required=True)
    address = db.StringField(required=True)
    meals = db.ListField(db.ReferenceField(MealWithCount))

    def __unicode__(self):
        return self.date


class User(db.Document):
    meta = {'collection': 'users', 'allow_inheritance': True}
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
