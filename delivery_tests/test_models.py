import pytest
from faker import Faker
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from delivery.models import *

client = MongoClient()
fake = Faker()
db.disconnect()
app.config['MONGODB_DB'] = 'delivery_test'
db = MongoEngine(app)


class TestViews:
    def setup(self):
        for i in range(10):
            user = User(name=fake.name(), mail=fake.email(), role=fake.word()).save()
            Category(category_id=i, title=fake.word()).save()
            meal = Meal(meal_id=i, title=fake.word(), price=fake.random_int(), description=fake.text(),
                 picture=fake.image_url(), category_id=i).save()
            meal = MealWithCount(meal=meal, count=fake.random_int())
            order = Order(date=fake.date_time(), sum=fake.random_int(), status=fake.word(), user=user,
                  phone=fake.phone_number(), address=fake.address()).save()


    def teardown(self):
        client.drop_database('delivery_test')

    def test_user_passwordhash(self):
        user = User(name=fake.name(), mail=fake.email(), role='user').save()
        password = fake.password()
        user.password = password
        user.save()
        assert user.password_valid(password) == True

    def test_is_db_is_testing_db(self):
        assert User._get_db().name == 'delivery_test'

    def test_count(self):
        assert User.objects.count() == 10
        assert Category.objects.count() == 10
        assert Meal.objects.count() == 10
