from django.urls import path

from . import views


app_name = "Dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("group/<str:group_name>", views.group, name="group"),
    path("upload", views.upload, name="upload")

]