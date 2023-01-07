import openai
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import RegisterForm
from .models import Group, Payment, User, UsersReceiving


def determine_category(description):
    # OpenAI API Key
    openai.api_key = settings.OPENAI_API_KEY
    # Categories
    categories = ["Food", "Drinks", "Groceries", "Health", "Fitness", "Education", "Clothing", "Transportation", "Entertainment", "Shopping", "Rent", "Utilities", "Other"]
    # Prompt
    prompt = "From the following list of categories, please select the one that best describes this description:\n"
    for category in categories:
        prompt += f"- {category}\n"
    prompt += f"Description: {description}\n"
    prompt += "Category: "
    # Response
    response = openai.Completion.create(
        model="text-curie-001",
        prompt=prompt,
        temperature=0.8,
        max_tokens=3,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text



def index(request):
    return HttpResponseRedirect(reverse("Dashboard:register"))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["group_name"] == "":
                return render(request, "Dashboard/registered.html", {"error": "Please enter a group name"})
            group_name = form.cleaned_data["group_name"]
            group, created = Group.objects.get_or_create(name=group_name)
            user_paying = form.cleaned_data["user_paying"]
            user_paying, created = User.objects.get_or_create(name=user_paying, id_group=group)
            users_receiving = []
            for user in form.cleaned_data["users_receiving"].split(","):
                user_receiving, created = User.objects.get_or_create(name=user, id_group=group)
                users_receiving.append(user_receiving)
            amount = form.cleaned_data["amount"]
            date = form.cleaned_data["date"]
            description = form.cleaned_data["description"]
            category = determine_category(description)
            payment = Payment.objects.create(id_user_paying=user_paying, amount=amount, description=description, date=date, category=category, id_group=group)
            for user_receiving in users_receiving:
                UsersReceiving.objects.create(id_user=user_receiving, id_payment=payment)
                payment.id_users_receiving.add(user_receiving)
            payment.id_users_receiving.set(users_receiving)
            payment.amount_per_user = amount / (len(users_receiving) + 1)
            payment.save()
            user_paying.total_contribution += amount
            for user_receiving in users_receiving:
                user_receiving.total_debt += payment.amount_per_user
                user_receiving.save()
            user_paying.total_debt += payment.amount_per_user
            user_paying.save()
            users = User.objects.filter(id_group=group)
            for user in users:
                user.balance = user.total_contribution - user.total_debt
                user.save()
            return render(request, "Dashboard/registered.html", {"group_name": group_name})
    else:
        form = RegisterForm()
    return render(request, "Dashboard/register.html", {"form": form})


def registered(request):
    return render(request, 'Dashboard/registered.html', {})


def group(request, group_name):
    group = Group.objects.get(name=group_name)
    users = User.objects.filter(id_group=group)
    return render(request, 'Dashboard/group.html', {
        "group": group,
        "users": users,
    })
