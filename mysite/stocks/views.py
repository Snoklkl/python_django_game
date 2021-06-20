from django.shortcuts import render
from .models import stocks_info, stock_identity, player_money, player_target, player_option, time_tracker

import sqlite3
con = sqlite3.connect('mydatabase.db')
cur = con.cursor()

# Create your views here.

def index(request):
    return render(request, 'stocks/index.html')

def create_player(request):

    return render(request, 'stocks/create_player.html')