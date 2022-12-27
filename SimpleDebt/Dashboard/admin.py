from django.contrib import admin
from .models import Group, User, UsersReceiving, Payment


admin.site.register(Group)
admin.site.register(User)
admin.site.register(UsersReceiving)
admin.site.register(Payment)
