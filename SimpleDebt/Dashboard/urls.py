from django.urls import path

from . import views


app_name = "Dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("registered", views.registered, name="registered"),
    path("group/<str:group_name>", views.group, name="group")
]