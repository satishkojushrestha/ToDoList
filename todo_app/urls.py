from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "landing"),
    path("<int:user_id>/logged", views.logged_user, name="logged"),
    path("signup", views.signup, name = "signup"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name="logout"),
    path("<int:userid>/addtask", views.addtask, name="addtask"),
    path("<int:userid>/delete", views.removetask, name="deletetask"),
]