from django.shortcuts import render
from .models import stocks_info, stock_identity, player_money, player_target, player_option, time_tracker

import sqlite3

import quandl
import numpy as np

"""

data_1 = quandl.get("WARSAWSE/WIG20LEV", start_date = "2016-12-1", end_date = "2017-12-1", collapse="monthly", rows=12)
data_2 = quandl.get("WARSAWSE/NCINDEX", start_date = "2016-12-1", end_date = "2017-12-1", collapse="monthly", rows=12)
data_3 = quandl.get("WARSAWSE/TBSP_INDEX", start_date = "2016-12-1", end_date = "2017-12-1", collapse="monthly", rows=12)



info_list = [
    ("ABC", data_1[1], data_1[2], data_1[3], data_1[4], data_1[5], data_1[6], data_1[7], data_1[8], data_1[9], data_1[10], data_1[11], data_1[12], data_1[13], 8),
    ("BBC", data_2[1], data_2[2], data_2[3], data_2[4], data_2[5], data_2[6], data_2[7], data_2[8], data_2[9], data_2[10], data_2[11], data_2[12], data_2[13], 5),
    ("NBC", data_3[1], data_3[2], data_3[3], data_3[4], data_3[5], data_3[6], data_3[7], data_3[8], data_3[9], data_3[10], data_3[11], data_3[12], data_3[13], 3),
]


cur.executemany("insert into stocks_info values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", info_list)


"""
query_1 = "HD"
query_2 = "DIS"
query_3 = "MSFT"

quandl.ApiConfig.api_key = "Hx9MtbnfaWgzw9knX7Ao"
data_1 = quandl.get("EOD/" + query_1 , start_date = "2014-12-1", end_date = "2015-12-1", collapse="monthly", rows=13, column_index = 1, returns="numpy")
data_2 = quandl.get("EOD/" + query_2, start_date = "2014-12-1", end_date = "2015-12-1", collapse="monthly", rows=13, column_index = 1, returns="numpy")
data_3 = quandl.get("EOD/" + query_3, start_date = "2014-12-1", end_date = "2015-12-1", collapse="monthly", rows=13, column_index = 1, returns="numpy")
    
import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
db_path = os.path.join(BASE_DIR, "db.sqlite3")
    
con = sqlite3.connect(db_path)
cur = con.cursor()

stock_database_info_1 = [1, data_1[1][1], data_1[2][1], data_1[3][1], data_1[4][1], data_1[5][1], data_1[6][1], data_1[7][1], data_1[8][1], data_1[9][1], data_1[10][1], data_1[11][1], data_1[12][1], 3 ,data_1[0][1], query_1] 
stock_database_info_2 = [2, data_2[1][1], data_2[2][1], data_2[3][1], data_2[4][1], data_2[5][1], data_2[6][1], data_2[7][1], data_2[8][1], data_2[9][1], data_2[10][1], data_2[11][1], data_2[12][1], 5, data_2[0][1], query_2] 
stock_database_info_3 = [3,  data_3[1][1], data_3[2][1], data_3[3][1], data_3[4][1], data_3[5][1], data_3[6][1], data_3[7][1], data_3[8][1], data_3[9][1], data_3[10][1], data_3[11][1], data_3[12][1], 8, data_3[0][1], query_3] 


cur.executemany("INSERT OR REPLACE INTO stocks_stocks_info  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [stock_database_info_1, stock_database_info_2, stock_database_info_3])

con.commit()



# Create your views here.

def index(request):
    player_information = player_option.objects.get(id=1)


    context = {
        "data_1": data_1,
        'data_conf': stock_database_info_1,
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