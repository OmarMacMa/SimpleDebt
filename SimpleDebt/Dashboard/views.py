import openai
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import RegisterForm
from .models import Group, Payment, User, UsersReceiving


# Function to classify a description
def determine_category(description):
    """
    Classify a description using OpenAI's Curie text classification model.
    """
    # OpenAI API Key
    openai.api_key = settings.OPENAI_API_KEY
    # Categories
    categories = ["Food", "Drinks", "Groceries", "Health", "Fitness",
                  "Education", "Clothing", "Transportation", "Entertainment",
                  "Shopping", "Rent", "Utilities", "Other"]
    # Prompt for the model
    prompt = "From the following list of categories, \
              please select the one that best describes this description:\n"
    for category in categories:
        prompt += f"- {category}\n"
    prompt += f"Description: {description}\n"
    prompt += "Category:"
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
    category = response.choices[0].text
    # Retry up to 3 times if the response is not in the list of categories
    for i in range(3):
        if category in categories:
            break
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=prompt,
            temperature=0.8,
            max_tokens=3,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        category = response.choices[0].text
    return category


# Index view redirection
def index(request):
    """
    Redirects to the 'register' view.
    """
    return HttpResponseRedirect(reverse("Dashboard:register"))


# Register view
def register(request):
    """
    Responsible for registering a payment and updating the database.
    If the request is a GET, renders the 'register' view with the form.
    If the request is a POST, validates the form data and registers the payment
    updating the balances of the users and rendering the 'registered' view.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Validate that a group name has been entered
            if form.cleaned_data["group_name"] == "":
                return render(request, "Dashboard/registered.html", {
                    "error": "Please enter a group name"
                })
            # Get or create the group
            group_name = form.cleaned_data["group_name"]
            group, created = Group.objects.get_or_create(name=group_name)
            # Get or create the user paying
            user_paying = form.cleaned_data["user_paying"]
            user_paying, created = User.objects.get_or_create(
                name=user_paying, id_group=group
            )
            # Get or create the users receiving
            users_receiving = []
            for user in form.cleaned_data["users_receiving"].split(","):
                user_receiving, created = User.objects.get_or_create(
                    name=user, id_group=group
                )
                users_receiving.append(user_receiving)
            # Get the amount, date and description, and determine the category
            amount = form.cleaned_data["amount"]
            date = form.cleaned_data["date"]
            description = form.cleaned_data["description"]
            category = determine_category(description)
            # Create the payment and update the database
            payment = Payment.objects.create(
                id_user_paying=user_paying, amount=amount,
                description=description, date=date,
                category=category, id_group=group
            )
            # Add the users receiving to the payment
            for user_receiving in users_receiving:
                UsersReceiving.objects.create(
                    id_user=user_receiving, id_payment=payment
                )
                payment.id_users_receiving.add(user_receiving)
            # Set the payment amount per user
            payment.id_users_receiving.set(users_receiving)
            payment.amount_per_user = amount / (len(users_receiving) + 1)
            payment.save()
            # Update the user_paying's total contribution and total debt
            user_paying.total_contribution += amount
            user_paying.total_debt += payment.amount_per_user
            user_paying.save()
            # Update the users receiving's total debt
            for user_receiving in users_receiving:
                user_receiving.total_debt += payment.amount_per_user
                user_receiving.save()
            # Update the users' balances
            users = User.objects.filter(id_group=group)
            for user in users:
                user.balance = user.total_contribution - user.total_debt
                user.save()
            # Redirect to the 'registered' view
            return render(request, "Dashboard/registered.html", {
                "group_name": group_name
            })
    else:
        form = RegisterForm()
    # Render the 'register' view
    return render(request, "Dashboard/register.html", {
        "form": form
    })


# Registered view
def registered(request):
    """
    Render the 'registered' view.
    """
    return render(request, 'Dashboard/registered.html', {})


# Group view
def group(request, group_name):
    """
    Render the 'group' view which displays the group's
    table of debts and balances.
    """
    group = Group.objects.get(name=group_name)
    users = User.objects.filter(id_group=group)
    return render(request, 'Dashboard/group.html', {
        "group": group,
        "users": users,
    })