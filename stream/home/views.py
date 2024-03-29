from django.shortcuts import render
from tmdbv3api import TMDb, Movie
from .forms import SearchForm
from account.models import Watchlist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import environ
from django.conf import settings
import os
from .decorators import subscription_required

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))

tmdb = TMDb()

tmdb.api_key = env('TMDB')


def index(request):
    movie = Movie()
    now_play = movie.now_playing()
    popular = movie.popular()
    top_rated = movie.top_rated()
    return render(request, 'home/index.html',
                  {'popular': popular, 'now_playing': now_play, 'top': top_rated})


def movie_detail(request, mid):
    movie = Movie()
    m = movie.details(mid)
    similar = movie.recommendations(mid)
    v = m.videos
    tr = ''
    watchlisted = False
    if request.user.is_authenticated:
        watchlisted = Watchlist.objects.filter(uid=request.user, mid=mid).exists()

    for i in v['results']:
        if 'Trailer' in i.values():
            tr = i['key']

    return render(request, 'home/movie_info.html',
                  {'movie': m, 'watchlisted': watchlisted, 'trailer': tr, 'similar': similar[:4]})

@login_required
@subscription_required
def watch_movie(request, mid):
    movie = Movie()
    m = movie.details(mid)
    similar = movie.recommendations(mid)
    v = m.videos
    tr = ''

    for i in v['results']:
        if 'Trailer' in i.values():
            tr = i['key']

    return render(request, 'home/watch.html',
                  {'movie': m, 'trailer': tr, 'similar': similar})


def now_playing(request):
    movie = Movie()
    now_play = movie.now_playing()
    return render(request, 'home/browse.html', {'title': 'Now Playing', 'movies': now_play})


def popular_movies(request):
    movie = Movie()
    popular = movie.popular()
    return render(request, 'home/browse.html', {'title': 'Popular Right Now', 'movies': popular})


def top_movies(request):
    movie = Movie()
    top_rated = movie.top_rated()
    return render(request, 'home/browse.html', {'title': 'Top Rated', 'movies': top_rated})


@csrf_exempt
def search(request):
    m = Movie()
    context = {}
    form = SearchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        q = form.cleaned_data['query']
        results = m.search(q)
        context['results'] = results
    context['form'] = form
    return render(request, 'home/search.html', context)


@csrf_exempt
@login_required
def add_to_watchlist(request, mid):
    if request.method == 'POST':
        w = Watchlist(uid=request.user, mid=mid)
        w.save()
    return redirect('/movie/' + str(mid) + '/')
