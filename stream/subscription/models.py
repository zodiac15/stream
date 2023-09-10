from django.db import models
from django.conf import settings


# Create your models here.


class StripeCustomer(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cust_id = models.CharField(max_length=200)


class Transaction(models.Model):
    cust_id = models.ForeignKey(StripeCustomer, on_delete=models.CASCADE)
    transact_data = models.JSONField()

class Subscription(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sid = models.CharField(max_length=200)
    start = models.CharField(max_length=200)
    end = models.CharField(max_length=200)
    plan = models.CharField(max_length=20)

