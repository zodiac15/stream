from django.contrib import admin
from .models import StripeCustomer,Subscription,Transaction

# Register your models here.
admin.site.register(Subscription)
admin.site.register(StripeCustomer)
admin.site.register(Transaction)

