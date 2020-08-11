from models import User, Category, Meal, db
from config import Config


def update():
    with open("data/delivery_categories.csv", "r") as file:
        lines = file.readlines()
        for i in range(1, len(lines)):
            data = lines[i].split(",")
            category = Category(id=data[0], title=data[1])
            db.session.add(category)

    # id,title,price,description,picture,category_id
    with open("data/meals.csv", "r") as file:
        lines = file.readlines()
        for i in range(1, len(lines)):
            data = lines[i].split(";")
            item = Meal(id=int(data[0]), title=data[1], price=int(data[2]),
                        description=data[3], picture=data[4], category_id=int(data[5]))
            db.session.add(item)
    guest = User(name='guest', mail='guest', password=Config.PASSWORD, role='guest')
    admin = User(name='admin', mail='admin', password=Config.PASSWORD, role='admin')
    db.session.add(guest)
    db.session.add(admin)
    db.session.commit()
