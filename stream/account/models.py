from django.db import models
from django.conf import settings


class SubStatus(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False)


class Watchlist(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mid = models.CharField(max_length=30)
