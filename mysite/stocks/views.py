from django.shortcuts import render
from .models import stocks_info, stock_identity, player_money, player_target, player_option, time_tracker

import sqlite3
con = sqlite3.connect('mydatabase.db')
cur = con.cursor()
import quandl
quandl.Apiconfig.api_key = "Hx9MtbnfaWgzw9knX7Ao"

data_1 = quandl.get("WARSAWSE/WIG20LEV", start_date = "2016-12-1", end_date = "2017-12-1", collapse="monthly")
data_2 = quandl.get("WARSAWSE/NCINDEX", start_date = "2016-12-1", end_date = "2017-12-1", collapse="monthly")
data_3 = quandl.get("WARSAWSE/TBSP_INDEX", start_date = "2016-12-1", end_date = "2017-12-1", collapse="monthly")


info_list = [
    ("ABC", ),
    ("BBC", ),
    ("NBC", ),
]

cur.execute("INSERT INTO stocks_info VALUES ('ABC', ' ')")

cur.execute("INSERT INTO stocks_info VALUES ('BBC', ' ')")

cur.executemany("insert into stocks_info values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", info_list)





stock_list = stocks_info.objects.all()
for stock in stock_list:
    i = 1
    stock_i = stock_list.objects.get(id=i)
    i += 1

# Create your views here.

def index(request):
    player_information = player_option.objects.get(id=1)


  
   


    context = {
        'player_name': player_information.player_name.upper(),
        'current_cash': player_information.players_liquid_money,
        'player_worth': player_information.players_total_money,
        'current_month': player_information.current_month.upper(),
        'target_month': player_information.target_month.upper(),
        'worth_target': player_information.worth_target, 
        'stock_info' : stocks_info.objects.all(),


    }
    return render(request, 'stocks/index.html', context)

def create_player(request):

    return render(request, 'stocks/create_player.html')