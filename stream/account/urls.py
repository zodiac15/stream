from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='account_index'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('watchlist/', views.watchlist, name='watchlist')
]
