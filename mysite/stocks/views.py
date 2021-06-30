from django.shortcuts import render
from .models import stocks_info, stock_identity, player_money, player_target, player_option, time_tracker

import sqlite3
con = sqlite3.connect('mydatabase.db')
cur = con.cursor()

# Create your views here.

def index(request):
    player_information = player_option.objects.get(id=1)
    player_information.player_total_money = 1000

    context = {
        'player_name': player_information.player_name.upper(),
        'current_cash': player_information.players_liquid_money,
        'player_worth': player_information.players_total_money,
        'current_month': player_information.current_month.upper(),
        'target_month': player_information.target_month.upper(),
        'worth_target': player_information.worth_target, 


    }
    return render(request, 'stocks/index.html', context)

def create_player(request):

    return render(request, 'stocks/create_player.html')