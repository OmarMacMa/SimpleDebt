from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=50)


class User(models.Model):
    name = models.CharField(max_length=50)
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    total_contribution = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    total_debt = models.DecimalField(decimal_places=2, default=0, max_digits=10)


class Payment(models.Model):
    id_user_paying = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_paying')
    id_users_receiving = models.ManyToManyField(User, through="UsersReceiving", related_name="users_receiving")
    amount = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    amount_per_user = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    description = models.CharField(max_length=50)
    date = models.DateField()
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)

class UsersReceiving(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_payment = models.ForeignKey(Payment, on_delete=models.CASCADE)