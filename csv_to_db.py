from models import User, Category, Meal
from config import Config


with open("../untitled/data/delivery_categories.csv", "r") as file:
    lines = file.readlines()
    for i in range(1, len(lines)):
        data = lines[i].split(",")
        print(data)
        category = Category(category_id=int(data[0]), title=data[1].rstrip())
        category.save()

# id,title,price,description,picture,category_id
with open("../untitled/data/meals.csv", "r") as file:
    lines = file.readlines()
    for i in range(1, len(lines)):
        data = lines[i].split(";")
        print(data)
        item = Meal(meal_id=int(data[0]), title=data[1], price=int(data[2]),
                    description=data[3], picture=data[4], category_id=int(data[5].rstrip()),
                    category=Category.objects(category_id=int(data[5].rstrip())).first())
        item.save()

admin = User(name='admin', mail='admin@admin.ru', role='admin')
admin.password = 'veryLongAdminPassword'
guest = User(name='guest')
guest.save()
admin.save()