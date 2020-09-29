from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.mongoengine import ModelView
from delivery import app, redirect, session
from delivery.models import User, Category, Order, Meal


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if 'role' in session and session['role'] == 'admin':
            return super(MyAdminIndexView, self).index()
        return redirect('/')


admin = Admin(app, url='/', index_view=MyAdminIndexView())
admin.add_view(ModelView(User))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(Order))
admin.add_view(ModelView(Meal))
