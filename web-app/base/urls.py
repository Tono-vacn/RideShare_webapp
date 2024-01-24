from django.urls import path

from . import views


app_name = "base"
urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.init_page, name="init_page"),
]