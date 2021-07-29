#Dependencies and imports
from django.shortcuts import redirect, render
from .models import stocks_info, stock_identity, player_money, player_target, player_option, time_tracker

import sqlite3

import quandl

import os.path
from pathlib import Path
from .forms import stockForm

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent
db_path = os.path.join(BASE_DIR, "db.sqlite3")
con = sqlite3.connect(db_path)
cur = con.cursor()

# Create your views here.

def configStart(request):
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    db_path = os.path.join(BASE_DIR, "db.sqlite3")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query_1 = "HD"
    query_2 = "DIS"
    query_3 = "MSFT"

    quandl.ApiConfig.api_key = "Hx9MtbnfaWgzw9knX7Ao"

    data_1 = quandl.get("EOD/" + query_1, start_date = "2014-12-1", end_date = "2015-12-1", collapse="monthly", rows=13, column_index = 1, returns="numpy")
    data_2 = quandl.get("EOD/" + query_2, start_date = "2014-12-1", end_date = "2015-12-1", collapse="monthly", rows=13, column_index = 1, returns="numpy")
    data_3 = quandl.get("EOD/" + query_3, start_date = "2014-12-1", end_date = "2015-12-1", collapse="monthly", rows=13, column_index = 1, returns="numpy")
    stock_database_info_1 = [1, data_1[1][1], 3, data_1[2][1], data_1[3][1], data_1[4][1], data_1[5][1], data_1[6][1], data_1[7][1], data_1[8][1], data_1[9][1], data_1[10][1], data_1[11][1], data_1[12][1], data_1[0][1], query_1, data_1[1][1]] 
    stock_database_info_2 = [2, data_2[1][1], 5, data_2[2][1], data_2[3][1], data_2[4][1], data_2[5][1], data_2[6][1], data_2[7][1], data_2[8][1], data_2[9][1], data_2[10][1], data_2[11][1], data_2[12][1], data_2[0][1], query_2, data_1[1][1]] 
    stock_database_info_3 = [3,  data_3[1][1], 8, data_3[2][1], data_3[3][1], data_3[4][1], data_3[5][1], data_3[6][1], data_3[7][1], data_3[8][1], data_3[9][1], data_3[10][1], data_3[11][1], data_3[12][1], data_3[0][1], query_3, data_1[1][1]] 
   
    cur.executemany("INSERT OR REPLACE INTO stocks_stocks_info (id, jan_value, amount_owned, feb_value, mar_value, april_value, may_value, june_value, july_value, aug_value, sept_value, oct_value, nov_value, december_value, past_dec_value, stock_symbol, current_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [stock_database_info_1, stock_database_info_2, stock_database_info_3])
    """cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.jan_value,)) 
    cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.jan_value,))
    cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.jan_value,))
    cur.execute("UPDATE stocks_stocks_info SET amount_owned = (?) WHERE id = 1", (3)) 
    cur.execute("UPDATE stocks_stocks_info SET amount_owned = (?) WHERE id = 2", (5))
    cur.execute("UPDATE stocks_stocks_info SET amount_owned = (?) WHERE id = 3", (8))
    con.commit()"""

    action_reset = 4
    month_reset = "January"
    money_reset = 500
    cur.execute("UPDATE stocks_player_option SET (action_economy, current_month, players_liquid_money) = (?, ?, ?) WHERE id = 1", (action_reset, month_reset, money_reset)) 
    con.commit()




    return render(request, "stocks/start.html")

def index(request):
    current_month = 2 
    player_information = player_option.objects.get(id=1)
    stock_HD = stocks_info.objects.get(id=1)
    stock_DIS = stocks_info.objects.get(id=2)
    stock_MSFT = stocks_info.objects.get(id=3)
    form = stockForm(request.POST)
    
    player_worth = player_information.players_liquid_money + (stock_HD.current_value * stock_HD.amount_owned) + (stock_DIS.current_value * stock_DIS.amount_owned) + (stock_MSFT.current_value * stock_MSFT.amount_owned)

    context = {
        'action': player_information.action_economy,
        'form': form,
        'player_name': player_information.player_name.upper(),
        'current_cash': player_information.players_liquid_money,
        'player_worth': player_worth,
        'current_month': player_information.current_month.upper(),
        'target_month': player_information.target_month.upper(),
        'worth_target': player_information.worth_target, 
        'stock_info' : stocks_info.objects.all(),
    }

    return render(request, 'stocks/index.html', context)

    

def buy_HD(request):
    player_information = player_option.objects.get(id=1)
    stock_HD = stocks_info.objects.get(id=1)
    stock_DIS = stocks_info.objects.get(id=2)
    stock_MSFT = stocks_info.objects.get(id=3)


    if request.method == "POST": 
        
        form = stockForm(request.POST)
        if form.is_valid():
            stock_checks = stocks_info.objects.get(id=1)
            if (form.cleaned_data['stock_request'] * stock_HD.current_value) < player_information.players_liquid_money:
                new_HD = form.cleaned_data['stock_request'] + stock_checks.amount_owned
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                action_economy = player_information.action_economy + 1
                new_money = player_information.players_liquid_money - (form.cleaned_data['stock_request'] * stock_HD.current_value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 1", (new_HD,))
                cur.execute("UPDATE stocks_player_option SET action_economy = ? WHERE id = 1", (action_economy,))
                con.commit()
            
                
                if player_information.action_economy == 4:
                    con = sqlite3.connect(db_path)
                    cur = con.cursor()
                    current_month = player_information.current_month
                    cur.execute("UPDATE stocks_player_option SET action_economy = (?) WHERE id = 1", (1,))
                    con.commit()
                    
                    if current_month == "January":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("February",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.feb_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.feb_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.feb_value,))
                        con.commit()
                    elif current_month == "February":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("March",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.mar_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.mar_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.mar_value,))
                        con.commit()
                    elif current_month == "March":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("April",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.april_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.april_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.april_value,))
                        con.commit()
                    elif current_month == "April":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("May",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.may_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.may_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.may_value,))
                        con.commit()
                        player_information.current_month = "May"
                    elif current_month == "May":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("June",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.june_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.june_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.june_value,))
                        con.commit()
                    elif current_month == "June":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("July",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.july_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.july_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.july_value,))
                        con.commit()
                    elif current_month == "July":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("August",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.aug_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.aug_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.aug_value,))
                        con.commit()
                    elif current_month == "August":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("September",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.sept_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.sept_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.sept_value,))
                        con.commit()
                    elif current_month == "September":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("October",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.oct_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.oct_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.oct_value,))
                        con.commit()
                    elif current_month == "October":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("November",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.nov_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.nov_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.nov_value,))
                        con.commit()
                    elif current_month == "November":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("December",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.december_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.december_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.december_value,))
                        con.commit()
                    else:
                        value_HD = ""
                
            else: 
                error_message = "You don't have enough money for this purchase."
                player_worth = player_information.players_liquid_money + (stock_HD.current_value * stock_HD.amount_owned) + (stock_DIS.current_value * stock_DIS.amount_owned) + (stock_MSFT.current_value * stock_MSFT.amount_owned)
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_worth,
                'current_month': player_information.current_month.upper(),
                'target_month': player_information.target_month.upper(),
                'worth_target': player_information.worth_target, 
                'stock_info' : stocks_info.objects.all(),
        
                "error_message": error_message.upper() ,
                }

                return render(request, 'stocks/index.html', context)
            

    return redirect('/stocks/')

def sell_HD(request):
    player_information = player_option.objects.get(id=1)
    stock_HD = stocks_info.objects.get(id=1)
    stock_DIS = stocks_info.objects.get(id=2)
    stock_MSFT = stocks_info.objects.get(id=3)
    if request.method == "POST": 
        form = stockForm(request.POST)
        if form.is_valid():
            player_amount = stocks_info.objects.get(id=1)
            if player_amount.amount_owned >= form.cleaned_data['stock_request']:
                new_HD = player_amount.amount_owned - form.cleaned_data['stock_request']
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                action_economy = player_information.action_economy + 1
                new_money = player_information.players_liquid_money - (form.cleaned_data['stock_request'] * stock_HD.current_value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 1", (new_HD,))
                cur.execute("UPDATE stocks_player_option SET action_economy = ? WHERE id = 1", (action_economy,))
                con.commit()
            
                
                if player_information.action_economy == 4:
                    con = sqlite3.connect(db_path)
                    cur = con.cursor()
                    current_month = player_information.current_month
                    cur.execute("UPDATE stocks_player_option SET action_economy = (?) WHERE id = 1", (1,))
                    con.commit()
                    
                    if current_month == "January":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("February",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.feb_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.feb_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.feb_value,))
                        con.commit()
                    elif current_month == "February":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("March",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.mar_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.mar_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.mar_value,))
                        con.commit()
                    elif current_month == "March":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("April",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.april_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.april_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.april_value,))
                        con.commit()
                    elif current_month == "April":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("May",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.may_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.may_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.may_value,))
                        con.commit()
                        player_information.current_month = "May"
                    elif current_month == "May":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("June",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.june_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.june_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.june_value,))
                        con.commit()
                    elif current_month == "June":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("July",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.july_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.july_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.july_value,))
                        con.commit()
                    elif current_month == "July":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("August",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.aug_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.aug_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.aug_value,))
                        con.commit()
                    elif current_month == "August":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("September",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.sept_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.sept_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.sept_value,))
                        con.commit()
                    elif current_month == "September":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("October",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.oct_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.oct_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.oct_value,))
                        con.commit()
                    elif current_month == "October":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("November",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.nov_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.nov_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.nov_value,))
                        con.commit()
                    elif current_month == "November":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("December",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.december_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.december_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.december_value,))
                        con.commit()
                    else:
                        value_HD = ""
               
            else: 
                error_message = "You don't have that many to sell!"
                player_worth = player_information.players_liquid_money + (stock_HD.current_value * stock_HD.amount_owned) + (stock_DIS.current_value * stock_DIS.amount_owned) + (stock_MSFT.current_value * stock_MSFT.amount_owned)
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_worth,
                'current_month': player_information.current_month.upper(),
                'target_month': player_information.target_month.upper(),
                'worth_target': player_information.worth_target, 
                'stock_info' : stocks_info.objects.all(),
        
                "error_message": error_message.upper() 
                }

                return render(request, 'stocks/index.html', context)



    return redirect('/stocks/')

def buy_DIS(request):
    player_information = player_option.objects.get(id=1)
    stock_HD = stocks_info.objects.get(id=1)
    stock_DIS = stocks_info.objects.get(id=2)
    stock_MSFT = stocks_info.objects.get(id=3)
    if request.method == "POST": 
        form = stockForm(request.POST)
        if form.is_valid():
            
            if (form.cleaned_data['stock_request'] * stock_DIS.current_value) < player_information.players_liquid_money:
                player_amount = stocks_info.objects.get(id=2)
                new_DIS = form.cleaned_data['stock_request'] + player_amount.amount_owned
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                action_economy = player_information.action_economy + 1
                new_money = player_information.players_liquid_money - (form.cleaned_data['stock_request'] * stock_DIS.current_value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 2", (new_DIS,))
                cur.execute("UPDATE stocks_player_option SET action_economy = ? WHERE id = 1", (action_economy,))
                con.commit()
            
                
                if player_information.action_economy == 4:
                    con = sqlite3.connect(db_path)
                    cur = con.cursor()
                    current_month = player_information.current_month
                    cur.execute("UPDATE stocks_player_option SET action_economy = (?) WHERE id = 1", (1,))
                    con.commit()
                    
                    if current_month == "January":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("February",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.feb_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.feb_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.feb_value,))
                        con.commit()
                    elif current_month == "February":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("March",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.mar_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.mar_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.mar_value,))
                        con.commit()
                    elif current_month == "March":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("April",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.april_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.april_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.april_value,))
                        con.commit()
                    elif current_month == "April":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("May",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.may_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.may_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.may_value,))
                        con.commit()
                        player_information.current_month = "May"
                    elif current_month == "May":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("June",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.june_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.june_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.june_value,))
                        con.commit()
                    elif current_month == "June":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("July",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.july_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.july_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.july_value,))
                        con.commit()
                    elif current_month == "July":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("August",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.aug_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.aug_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.aug_value,))
                        con.commit()
                    elif current_month == "August":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("September",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.sept_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.sept_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.sept_value,))
                        con.commit()
                    elif current_month == "September":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("October",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.oct_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.oct_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.oct_value,))
                        con.commit()
                    elif current_month == "October":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("November",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.nov_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.nov_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.nov_value,))
                        con.commit()
                    elif current_month == "November":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("December",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.december_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.december_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.december_value,))
                        con.commit()
                    else:
                        value_HD = ""
            else: 
                error_message = "You don't have enough money for this purchase."
                player_worth = player_information.players_liquid_money + (stock_HD.current_value * stock_HD.amount_owned) + (stock_DIS.current_value * stock_DIS.amount_owned) + (stock_MSFT.current_value * stock_MSFT.amount_owned)
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_worth,
                'current_month': player_information.current_month.upper(),
                'target_month': player_information.target_month.upper(),
                'worth_target': player_information.worth_target, 
                'stock_info' : stocks_info.objects.all(),
        
                "error_message": error_message.upper() 
                }

                return render(request, 'stocks/index.html', context)

    return redirect('/stocks/')

def sell_DIS(request):
    player_information = player_option.objects.get(id=1)
    stock_HD = stocks_info.objects.get(id=1)
    stock_DIS = stocks_info.objects.get(id=2)
    stock_MSFT = stocks_info.objects.get(id=3)
    if request.method == "POST": 
        form = stockForm(request.POST)
        if form.is_valid():
            player_amount = stocks_info.objects.get(id=2)
            if player_amount.amount_owned >= form.cleaned_data['stock_request']:

                new_DIS = player_amount.amount_owned - form.cleaned_data['stock_request']
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                action_economy = player_information.action_economy + 1
                new_money = player_information.players_liquid_money + (form.cleaned_data['stock_request'] * stock_DIS.current_value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 2", (new_DIS,))
                cur.execute("UPDATE stocks_player_option SET action_economy = ? WHERE id = 1", (action_economy,))
                con.commit()
            
                
                if player_information.action_economy == 4:
                    con = sqlite3.connect(db_path)
                    cur = con.cursor()
                    current_month = player_information.current_month
                    cur.execute("UPDATE stocks_player_option SET action_economy = (?) WHERE id = 1", (1,))
                    con.commit()
                    
                    if current_month == "January":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("February",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.feb_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.feb_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.feb_value,))
                        con.commit()
                    elif current_month == "February":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("March",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.mar_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.mar_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.mar_value,))
                        con.commit()
                    elif current_month == "March":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("April",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.april_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.april_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.april_value,))
                        con.commit()
                    elif current_month == "April":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("May",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.may_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.may_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.may_value,))
                        con.commit()
                        player_information.current_month = "May"
                    elif current_month == "May":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("June",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.june_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.june_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.june_value,))
                        con.commit()
                    elif current_month == "June":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("July",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.july_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.july_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.july_value,))
                        con.commit()
                    elif current_month == "July":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("August",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.aug_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.aug_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.aug_value,))
                        con.commit()
                    elif current_month == "August":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("September",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.sept_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.sept_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.sept_value,))
                        con.commit()
                    elif current_month == "September":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("October",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.oct_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.oct_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.oct_value,))
                        con.commit()
                    elif current_month == "October":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("November",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.nov_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.nov_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.nov_value,))
                        con.commit()
                    elif current_month == "November":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("December",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.december_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.december_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.december_value,))
                        con.commit()
                    else:
                        value_HD = ""
            else: 
                error_message = "You don't have that many to sell!"
                player_worth = player_information.players_liquid_money + (stock_HD.current_value * stock_HD.amount_owned) + (stock_DIS.current_value * stock_DIS.amount_owned) + (stock_MSFT.current_value * stock_MSFT.amount_owned)
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_worth,
                'current_month': player_information.current_month.upper(),
                'target_month': player_information.target_month.upper(),
                'worth_target': player_information.worth_target, 
                'stock_info' : stocks_info.objects.all(),
        
                "error_message": error_message.upper() 
                }

                return render(request, 'stocks/index.html', context)
    return redirect('/stocks/')


def buy_MSFT(request):
    player_information = player_option.objects.get(id=1)
    stock_HD = stocks_info.objects.get(id=1)
    stock_DIS = stocks_info.objects.get(id=2)
    stock_MSFT = stocks_info.objects.get(id=3)
    if request.method == "POST": 
        form = stockForm(request.POST)
        if form.is_valid():
          
            if (form.cleaned_data['stock_request'] * stock_MSFT.current_value) < player_information.players_liquid_money:
                player_amount = stocks_info.objects.get(id=3)
                new_MSFT = form.cleaned_data['stock_request'] + player_amount.amount_owned
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                action_economy = player_information.action_economy + 1
                new_money = player_information.players_liquid_money - (form.cleaned_data['stock_request'] * stock_MSFT.current_value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 3", (new_MSFT,))
                cur.execute("UPDATE stocks_player_option SET action_economy = ? WHERE id = 1", (action_economy,))
                con.commit()
            
                
                if player_information.action_economy == 4:
                    con = sqlite3.connect(db_path)
                    cur = con.cursor()
                    current_month = player_information.current_month
                    cur.execute("UPDATE stocks_player_option SET action_economy = (?) WHERE id = 1", (1,))
                    con.commit()
                    
                    if current_month == "January":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("February",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.feb_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.feb_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.feb_value,))
                        con.commit()
                    elif current_month == "February":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("March",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.mar_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.mar_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.mar_value,))
                        con.commit()
                    elif current_month == "March":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("April",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.april_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.april_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.april_value,))
                        con.commit()
                    elif current_month == "April":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("May",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.may_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.may_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.may_value,))
                        con.commit()
                        player_information.current_month = "May"
                    elif current_month == "May":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("June",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.june_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.june_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.june_value,))
                        con.commit()
                    elif current_month == "June":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("July",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.july_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.july_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.july_value,))
                        con.commit()
                    elif current_month == "July":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("August",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.aug_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.aug_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.aug_value,))
                        con.commit()
                    elif current_month == "August":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("September",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.sept_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.sept_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.sept_value,))
                        con.commit()
                    elif current_month == "September":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("October",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.oct_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.oct_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.oct_value,))
                        con.commit()
                    elif current_month == "October":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("November",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.nov_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.nov_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.nov_value,))
                        con.commit()
                    elif current_month == "November":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("December",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.december_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.december_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.december_value,))
                        con.commit()
                    else:
                        value_HD = ""

            else: 
                error_message = "You don't have enough money for this purchase."
                player_worth = player_information.players_liquid_money + (stock_HD.current_value * stock_HD.amount_owned) + (stock_DIS.current_value * stock_DIS.amount_owned) + (stock_MSFT.current_value * stock_MSFT.amount_owned)
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_worth,
                'current_month': player_information.current_month.upper(),
                'target_month': player_information.target_month.upper(),
                'worth_target': player_information.worth_target, 
                'stock_info' : stocks_info.objects.all(),
        
                "error_message": error_message.upper() 
                }

                return render(request, 'stocks/index.html', context)

    return redirect('/stocks/')

def sell_MSFT(request):
    player_information = player_option.objects.get(id=1)
    stock_HD = stocks_info.objects.get(id=1)
    stock_DIS = stocks_info.objects.get(id=2)
    stock_MSFT = stocks_info.objects.get(id=3)
    if request.method == "POST": 
        form = stockForm(request.POST)
        if form.is_valid():
            player_amount = stocks_info.objects.get(id=3)
            if player_amount.amount_owned >= form.cleaned_data['stock_request']:
                new_MSFT = player_amount.amount_owned - form.cleaned_data['stock_request'] 
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                action_economy = player_information.action_economy + 1
                new_money = player_information.players_liquid_money + (form.cleaned_data['stock_request'] * stock_MSFT.current_value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 3", (new_MSFT,))
                cur.execute("UPDATE stocks_player_option SET action_economy = ? WHERE id = 1", (action_economy,))
                con.commit()
            
                
                if player_information.action_economy == 4:
                    con = sqlite3.connect(db_path)
                    cur = con.cursor()
                    current_month = player_information.current_month
                    cur.execute("UPDATE stocks_player_option SET action_economy = (?) WHERE id = 1", (1,))
                    con.commit()
                    
                    if current_month == "January":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("February",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.feb_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.feb_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.feb_value,))
                        con.commit()
                    elif current_month == "February":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("March",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.mar_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.mar_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.mar_value,))
                        con.commit()
                    elif current_month == "March":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("April",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.april_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.april_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.april_value,))
                        con.commit()
                    elif current_month == "April":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("May",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.may_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.may_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.may_value,))
                        con.commit()
                        player_information.current_month = "May"
                    elif current_month == "May":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("June",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.june_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.june_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.june_value,))
                        con.commit()
                    elif current_month == "June":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("July",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.july_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.july_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.july_value,))
                        con.commit()
                    elif current_month == "July":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("August",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.aug_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.aug_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.aug_value,))
                        con.commit()
                    elif current_month == "August":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("September",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.sept_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.sept_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.sept_value,))
                        con.commit()
                    elif current_month == "September":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("October",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.oct_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.oct_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.oct_value,))
                        con.commit()
                    elif current_month == "October":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("November",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.nov_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.nov_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.nov_value,))
                        con.commit()
                    elif current_month == "November":
                        cur.execute("UPDATE stocks_player_option SET current_month = (?) WHERE id = 1", ("December",))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 1", (stock_HD.december_value,)) 
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 2", (stock_DIS.december_value,))
                        cur.execute("UPDATE stocks_stocks_info SET current_value = (?) WHERE id = 3", (stock_MSFT.december_value,))
                        con.commit()
                    else:
                        value_HD = ""
            else: 
                error_message = "You don't have that many to sell!"
                player_worth = player_information.players_liquid_money + (stock_HD.current_value * stock_HD.amount_owned) + (stock_DIS.current_value * stock_DIS.amount_owned) + (stock_MSFT.current_value * stock_MSFT.amount_owned)
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_worth,
                'current_month': player_information.current_month.upper(),
                'target_month': player_information.target_month.upper(),
                'worth_target': player_information.worth_target, 
                'stock_info' : stocks_info.objects.all(),
        
                "error_message": error_message.upper() 
                }

                return render(request, 'stocks/index.html', context)

    return redirect('/stocks/')