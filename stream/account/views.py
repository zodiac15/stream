from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from .models import Watchlist
from tmdbv3api import Movie
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string



def sign_up(request):
    if request.user.is_authenticated:
        return redirect('account_index')
    context = {}
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)

        #send welcome email
        msg_plain = render_to_string('account/welcome_email.txt', {'username':  user.username})
        msg_html = render_to_string('account/welcome_email.html', {'name':  user.username})

        send_mail(
            f'Thanks for signing up, {user.username}!',
            msg_plain,
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=msg_html,
        )

        return render(request, 'account/index.html')
    context['form'] = form
    return render(request, 'account/signup.html', context)


@login_required
def index(request):
    user = request.user
    results = []
    for e in Watchlist.objects.filter(uid=request.user):
        movie = Movie()
        m = movie.details(e.mid)
        results.append(m)
    return render(request, 'account/index.html', {'user': user.username, 'results':results[:8]})


@login_required
def watchlist(request):
    results = []
    for e in Watchlist.objects.filter(uid=request.user):
        movie = Movie()
        m = movie.details(e.mid)
        results.append(m)
    return render(request, 'account/watchlist.html', {'results': results})


@login_required
@csrf_exempt
def logout(request):
    auth_logout(request)
    return redirect('home')
