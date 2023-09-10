from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('movie/<int:mid>/', views.movie_detail),
    path('watch/<int:mid>/', views.watch_movie),
    path('now-playing/', views.now_playing, name='now_playing'),
    path('top-rated/', views.top_movies, name='top_movies'),
    path('popular/', views.popular_movies, name='popular'),
    path('search/', views.search, name='search'),
    path('add-to-watchlist/<int:mid>/', views.add_to_watchlist)
]
