from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('stocks/', views.index),
    path('buy_HD/', views.buy_HD),
    
]