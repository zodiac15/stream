from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from account.models import SubStatus
from .models import StripeCustomer, Transaction, Subscription
import stripe
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import json
import environ
from django.conf import settings
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))

endpoint_secret = env('STRIPE_ENDPOINT_SECRET')
stripe.api_key = env('STRIPE_API_KEY')


# Create your views here.
@login_required
def packs(request):
    sub = None
    status = False
    if SubStatus.objects.filter(uid=request.user).exists():
        status = SubStatus.objects.filter(uid=request.user)
        sub = Subscription.objects.filter(uid=request.user).last()

    return render(request, 'subscription/packs.html', {'user': request.user, 'status': status, 'data': sub})


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(event['data']['object']['id'], expand=['line_items'], )
        customer = stripe.Customer.retrieve(session.customer)
        subscription = stripe.Subscription.retrieve(event['date']['object']['subscription'])

        print(customer, subscription)

    # Passed signature verification
    return HttpResponse(status=200)


def order_success(request, sid):
    session = stripe.checkout.Session.retrieve(sid)
    customer = stripe.Customer.retrieve(session.customer)
    subscription = stripe.Subscription.retrieve(session.subscription)
    c = StripeCustomer(uid=request.user, cust_id=customer.id)
    c.save()
    t = Transaction(cust_id=c, transact_data=session)
    t.save()
    s = Subscription(uid=request.user, sid=subscription.id, plan=subscription.plan.interval)
    s.start = datetime.fromtimestamp(subscription.plan.created).strftime("%d %B, %Y")
    et = datetime.fromtimestamp(subscription.plan.created) + timedelta(30)
    s.end = et.strftime("%d %B, %Y")
    s.save()
    status = SubStatus(uid=request.user, subscribed=True)
    status.save()

    print(customer.id, subscription.plan.created)
    return render(request, "subscription/success.html", {'data': s})
