from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path("gethistory/", views.gethistory),
    path("history/", views.history),
    path("gethd/", views.gethd),
    path("getdis/", views.getdis),
    path("getmsft/", views.getmsft),
    path('loss/', views.failState),
    path('start/', views.configStart),
    path('retry/', views.restart),
    path('stocks/', views.index),
    path('buy_HD/', views.buy_HD),
    path('buy_DIS/', views.buy_DIS),
    path('buy_MSFT/', views.buy_MSFT),
    path('sell_HD/', views.sell_HD),
    path('sell_DIS/', views.sell_DIS),
    path('sell_MSFT/', views.sell_MSFT),
]