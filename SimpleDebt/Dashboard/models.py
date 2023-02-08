from django.db import models


class Group(models.Model):
    """
    This model represents a group of users who share expenses.
    Has only one field: name.
    """
    name = models.CharField(max_length=50)


class User(models.Model):
    """
    This model represents a user who belongs to a group.
    Has 5 fields: name, id_group, balance, total_contribution, total_debt.
    """
    name = models.CharField(max_length=50)
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    total_contribution = models.DecimalField(
        decimal_places=2, default=0, max_digits=10
    )
    total_debt = models.DecimalField(
        decimal_places=2, default=0, max_digits=10
    )


class Payment(models.Model):
    """
    This model represents a payment made by a user to other users.
    Has 7 fields: id_user_paying, id_users_receiving, amount,
    amount_per_user, description, date, id_group.
    """
    id_user_paying = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_paying')
    id_users_receiving = models.ManyToManyField(
        User, through="UsersReceiving", related_name="users_receiving"
    )
    amount = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    amount_per_user = models.DecimalField(
        decimal_places=2, default=0, max_digits=10
    )
    description = models.CharField(max_length=50)
    date = models.DateField()
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)


class UsersReceiving(models.Model):
    """
    This model represents the many-to-many relationship between
    a payment and the users receiving it.
    Has 2 fields: id_user, id_payment. Both are foreign keys.
    """
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
