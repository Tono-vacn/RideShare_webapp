from django.urls import path

from . import views


app_name = "base"
urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.init_page, name="init_page"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("<str:id>/index/", views.index, name="index"),
    path("<str:id>/edit_profile/", views.edit_profile, name="edit_profile"),
]