from django.urls import path

from . import views


app_name = "base"
urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.init_page, name="init_page"),
    path("login/", views.login, name="login"),
    path("register/<str:flag>", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("<str:id>/index/", views.index, name="index"),
    path("<str:id>/edit_profile/", views.edit_profile, name="edit_profile"),
    path("<str:id>/register_as_driver/", views.register_as_driver, name="register_as_driver"),
    path("<str:id>/request_ride/", views.request_ride, name="request_ride"),
    path("<str:id>/view_my_ride/", views.view_my_ride, name="view_my_ride"),
    path("<str:id>/view_my_ride/<str:ride_id>/edit_ride/", views.edit_my_ride, name="edit_my_ride"),
    path("<str:id>/view_my_ride/<str:ride_id>/cancel_ride/", views.cancel_ride, name="cancel_ride"),
    path("<str:id>/view_open_ride/", views.view_open_ride, name="view_open_ride"),#for driver search
    path("<str:id>/request_join_ride/", views.request_join_ride, name="request_join_ride"),
    path("<str:id>/join_ride/<str:ride_id>/<int:share_passenger_num>/", views.join_ride, name="join_ride"),
    path("<str:id>/view_joined_ride/", views.view_joined_ride, name="view_joined_ride"),
    path("<str:id>/quit_ride/<str:ride_id>/", views.quit_ride, name="quit_ride"),
    path("<str:id>/confirm_ride/<str:ride_id>/", views.confirm_ride, name="confirm_ride"),
    path("<str:id>/view_taken_ride/", views.view_taken_ride, name="view_taken_ride"),
    path("<str:id>/complete_ride/<str:ride_id>/", views.complete_ride, name="complete_ride"),
    path("<str:id>/view_completed_ride/", views.view_completed_ride, name="view_completed_ride"),
    path("<str:id>/view_ride_detail/<str:ride_id>/", views.view_ride_detail, name="view_ride_detail"),
    # path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
]