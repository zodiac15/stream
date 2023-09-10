from django.urls import path
from . import views

urlpatterns = [
    path('', views.packs, name='sub_packs'),
    path('success/<str:sid>',views.order_success),
    path('webhook',views.my_webhook_view),

]

