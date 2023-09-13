import functools
from django.shortcuts import redirect
from django.contrib import messages
from account.models import SubStatus


def subscription_required(view_func, redirect_url="sub_packs"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        status = False
        if SubStatus.objects.filter(uid=request.user).exists():
            status = SubStatus.objects.filter(uid=request.user)

        if status:
            return view_func(request, *args, **kwargs)
        messages.info(request, "Please select a subscription plan to continue")
        print("subscription status false")
        return redirect(redirect_url)

    return wrapper
