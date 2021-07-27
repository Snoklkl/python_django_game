from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('stocks/', views.index),
    path('buy_HD/', views.buy_HD),
    path('buy_DIS/', views.buy_DIS),
    path('buy_MSFT/', views.buy_MSFT),
    path('sell_HD/', views.sell_HD),
    path('sell_DIS/', views.sell_DIS),
    path('sell_MSFT/', views.sell_MSFT),
]