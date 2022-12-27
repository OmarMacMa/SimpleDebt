from django.shortcuts import render
import pandas as pd
from datetime import datetime

from .models import Group, User, UsersReceiving, Payment


def index(request):
    group, created = Group.objects.get_or_create(name="HEMT")
    records = pd.read_csv("../records.csv")
    for index, record in records.iterrows():
        user_paying, created = User.objects.get_or_create(name=record["UserPaying"], id_group=group)
        users_receiving = []
        for user in record["UsersReceiving"].split(";"):
            user_receiving, created = User.objects.get_or_create(name=user, id_group=group)
            users_receiving.append(user_receiving)
        amount = float(record["Amount"])
        date = datetime.strptime(record["Date"], "%Y-%m-%d")
        payment = Payment.objects.create(id_user_paying=user_paying, amount=amount, description=record["Description"], date=date, category=record["Category"], id_group=group)
        for user_receiving in users_receiving:
            UsersReceiving.objects.create(id_user=user_receiving, id_payment=payment)
        payment.id_users_receiving.set(users_receiving)
        payment.amount_per_user = amount / (len(users_receiving) + 1)
        payment.save()
    return render(request, 'Dashboard/index.html', {})

def group(request, id_group):
    pass