from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
import pandas as pd
from datetime import datetime

from .models import Group, User, UsersReceiving, Payment


"""def index(request):
    return render(request, 'Dashboard/index.html', {})"""


def register(request):
    return render(request, 'Dashboard/register.html', {})


def upload(request):
    """try:
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
        return HttpResponseRedirect(reverse("Dashboard:group", args=(group_name,)))"""
    try:
        if request.POST["group_name"] == "":
            return HttpResponseRedirect(reverse("Dashboard:registered"), {"error_message": "Please enter a group name"})
        group_name = request.POST["group_name"]
        group, created = Group.objects.get_or_create(name=group_name)
        user_paying, created = User.objects.get_or_create(name=request.POST["user_paying"], id_group=group)
        users_receiving = []
        for user in request.POST["users_receiving"].split(","):
            user_receiving, created = User.objects.get_or_create(name=user, id_group=group)
            users_receiving.append(user_receiving)
        amount = float(request.POST["amount"])
        date = datetime.strptime(request.POST["date"], "%d/%m/%Y")
        payment = Payment.objects.create(id_user_paying=user_paying, amount=amount, description=request.POST["description"], date=date, category=request.POST["category"], id_group=group)
        for user_receiving in users_receiving:
            UsersReceiving.objects.create(id_user=user_receiving, id_payment=payment)
            payment.id_users_receiving.add(user_receiving)
        payment.id_users_receiving.set(users_receiving)
        payment.amount_per_user = amount / (len(users_receiving) + 1)
        payment.save()
        payment.id_user_paying.total_contribution += payment.amount
        for user_receiving in users_receiving:
            user_receiving.total_debt += payment.amount_per_user
            user_receiving.save()
        payment.id_user_paying.total_debt += payment.amount_per_user
        payment.id_user_paying.save()
        users = User.objects.filter(id_group=group)
        for user in users:
            user.balance = user.total_contribution - user.total_debt
            user.save()
        return HttpResponseRedirect(reverse("Dashboard:registered"), {
            "group_name": group_name,
        })
    except:
        return HttpResponseRedirect(reverse("Dashboard:registered"), {
            "error_message": "There was an error uploading the record.",
        })


def registered(request):
    return render(request, 'Dashboard/registered.html', {})


def group_name(request):
    group = get_object_or_404(Group, name=request.POST["group_name"])
    return HttpResponseRedirect(reverse("Dashboard:group", args=(group.name,)))


def group(request, group_name):
    group = Group.objects.get(name=group_name)
    users = User.objects.filter(id_group=group)
    return render(request, 'Dashboard/group.html', {
        "group": group,
        "users": users,
    })