from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd
from datetime import datetime

from .models import Group, User, UsersReceiving, Payment


def index(request):
    return render(request, 'Dashboard/index.html', {})


def upload(request):
    try:
        group_name = request.POST["group_name"]
        group, created = Group.objects.get_or_create(name=group_name)
        records = pd.read_csv(request.FILES["file"])
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
                payment.id_users_receiving.add(user_receiving)
            payment.id_users_receiving.set(users_receiving)
            payment.amount_per_user = amount / (len(users_receiving) + 1)
            payment.save()
        return HttpResponseRedirect(reverse("Dashboard:group", args=(group_name,)))
    except:
        return render(request, 'Dashboard/index.html', {
            "error_message": "There was an error uploading the file."
        })


def group(request, group_name):
    group = Group.objects.get(name=group_name)
    payments = Payment.objects.filter(id_group=group)
    for payment in payments:
        payment.id_user_paying.total_contribution += payment.amount
        users_receiving = UsersReceiving.objects.filter(id_payment=payment)
        for user in users_receiving:
            user.id_user.total_debt += payment.amount_per_user
            user.id_user.save()
        payment.id_user_paying.total_debt += payment.amount_per_user
        payment.id_user_paying.save()
    users = User.objects.all()
    for user in users:
        user.balance = user.total_contribution - user.total_debt
        user.save()
    return render(request, 'Dashboard/group.html', {
        "group": group,
        "users": users,
    })