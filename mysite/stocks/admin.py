from django.contrib import admin
from .models import player_worth_monthly, purchase_history, stocks_info, stock_identity, player_money, player_target, player_option, time_tracker

# Register your models here.

admin.site.register(stocks_info)

admin.site.register(stock_identity)

admin.site.register(player_money)

admin.site.register(player_target)

admin.site.register(player_option)

admin.site.register(time_tracker)

admin.site.register(purchase_history)

admin.site.register(player_worth_monthly)