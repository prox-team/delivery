from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from app import app, session, redirect
from models import User, Category, Order, Meal, db


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if 'role' in session and session['role'] == 'admin':
            return super(MyAdminIndexView, self).index()
        return redirect('/')


admin = Admin(app, url='/', index_view=MyAdminIndexView())
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Meal, db.session))
