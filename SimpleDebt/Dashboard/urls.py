from django.urls import path

from . import views


app_name = "Dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("group/<int:id_group>/", views.group, name="group"),

]