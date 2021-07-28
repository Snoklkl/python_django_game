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

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

#Setting up Connection to database
BASE_DIR = Path(__file__).resolve().parent.parent
db_path = os.path.join(BASE_DIR, "db.sqlite3")
con = sqlite3.connect(db_path)
cur = con.cursor()

'''

#Api query variables for stock prices monthly
query_1 = "HD"
query_2 = "DIS"
query_3 = "MSFT"

quandl.ApiConfig.api_key = "Hx9MtbnfaWgzw9knX7Ao"

data_1 = quandl.get("EOD/" + query_1 , start_date = "2014-12-1", end_date = "2015-12-1", collapse="monthly", rows=13, column_index = 1, returns="numpy")
data_2 = quandl.get("EOD/" + query_2, start_date = "2014-12-1", end_date = "2015-12-1", collapse="monthly", rows=13, column_index = 1, returns="numpy")
data_3 = quandl.get("EOD/" + query_3, start_date = "2014-12-1", end_date = "2015-12-1", collapse="monthly", rows=13, column_index = 1, returns="numpy")
    

#Putting the results of the GET into variables and then into the database

stock_database_info_1 = [1, data_1[1][1], data_1[2][1], data_1[3][1], data_1[4][1], data_1[5][1], data_1[6][1], data_1[7][1], data_1[8][1], data_1[9][1], data_1[10][1], data_1[11][1], data_1[12][1], 3 ,data_1[0][1], query_1] 
stock_database_info_2 = [2, data_2[1][1], data_2[2][1], data_2[3][1], data_2[4][1], data_2[5][1], data_2[6][1], data_2[7][1], data_2[8][1], data_2[9][1], data_2[10][1], data_2[11][1], data_2[12][1], 5, data_2[0][1], query_2] 
stock_database_info_3 = [3,  data_3[1][1], data_3[2][1], data_3[3][1], data_3[4][1], data_3[5][1], data_3[6][1], data_3[7][1], data_3[8][1], data_3[9][1], data_3[10][1], data_3[11][1], data_3[12][1], 8, data_3[0][1], query_3] 

cur.executemany("INSERT OR REPLACE INTO stocks_stocks_info  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [stock_database_info_1, stock_database_info_2, stock_database_info_3])
con.commit()

'''

# Create your views here.

def index(request):
    current_month = 1 
    player_information = player_option.objects.get(id=1)
    stock_HD = stocks_info.objects.get(id=1)
    stock_DIS = stocks_info.objects.get(id=2)
    stock_MSFT = stocks_info.objects.get(id=3)
    form = stockForm(request.POST)
   
    if player_information.action_economy != 1:
        player_information.action_economy = player_information.action_economy - 1
    else: 
        player_information.action_economy = 4
        current_month = current_month + 1
        if current_month == 2:
            value_HD = stock_HD.jan_value
            value_DIS = stock_DIS.jan_value
            value_MSFT = stock_MSFT.jan_value
        elif current_month == 3:
            value_HD = stock_HD.feb_value
            value_DIS = stock_DIS.feb_value
            value_MSFT = stock_MSFT.feb_value
        elif current_month == 4:
            value_HD = stock_HD.mar_value
            value_DIS = stock_DIS.mar_value
            value_MSFT = stock_MSFT.mar_value
        elif current_month == 5:
            value_HD = stock_HD.april_value
            value_DIS = stock_DIS.april_value
            value_MSFT = stock_MSFT.april_value
        elif current_month == 6:
            value_HD = stock_HD.may_value
            value_DIS = stock_DIS.may_value
            value_MSFT = stock_MSFT.may_value
        elif current_month == 7:
            value_HD = stock_HD.june_value
            value_DIS = stock_DIS.june_value
            value_MSFT = stock_MSFT.june_value
        elif current_month == 8:
            value_HD = stock_HD.july_value
            value_DIS = stock_DIS.july_value
            value_MSFT = stock_MSFT.july_value
        elif current_month == 9:
            value_HD = stock_HD.aug_value
            value_DIS = stock_DIS.aug_value
            value_MSFT = stock_MSFT.aug_value
        elif current_month == 10:
            value_HD = stock_HD.sept_value
            value_DIS = stock_DIS.sept_value
            value_MSFT = stock_MSFT.sept_value
        elif current_month == 11:
            value_HD = stock_HD.oct_value
            value_DIS = stock_DIS.oct_value
            value_MSFT = stock_MSFT.oct_value
        elif current_month == 12:
            value_HD = stock_HD.nov_value
            value_DIS = stock_DIS.nov_value
            value_MSFT = stock_MSFT.nov_value
        elif current_month == 13:
            value_HD = stock_HD.december_value
            value_DIS = stock_DIS.december_value
            value_MSFT = stock_MSFT.december_value
        else:
            value_HD = ""
        

    

    player_worth = player_information.players_liquid_money + (value_HD * stock_HD.amount_owned) + (value_DIS * stock_DIS.amount_owned) + (value_MSFT * stock_MSFT.amount_owned)
    context = {
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
    if request.method == "POST": 
        
        form = stockForm(request.POST)
        if form.is_valid():
            stock_checks = stocks_info.objects.get(id=1)
            value = stock_checks.jan_value
            if (form.cleaned_data['stock_request'] * value) < player_information.players_liquid_money:
                new_HD = form.cleaned_data['stock_request'] + stock_checks.amount_owned
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                new_money = player_information.players_liquid_money - (form.cleaned_data['stock_request'] * value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 1", (new_HD,))
                con.commit()
            else: 
                error_message = "You don't have enough money for this purchase."
                
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_information.players_total_money,
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
    error_message = ""
    if request.method == "POST": 
        form = stockForm(request.POST)
        if form.is_valid():
            stock_checks = stocks_info.objects.get(id=2)
            value = stock_checks.jan_value
            player_amount = stocks_info.objects.get(id=1)
            if player_amount.amount_owned >= form.cleaned_data['stock_request']:
                new_HD = player_amount.amount_owned -form.cleaned_data['stock_request']
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                new_money = player_information.players_liquid_money + (form.cleaned_data['stock_request'] * value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 1", (new_HD,))
                con.commit()
            else: 
                error_message = "You don't have that many to sell!"
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_information.players_total_money,
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
    if request.method == "POST": 
        form = stockForm(request.POST)
        if form.is_valid():
            stock_checks = stocks_info.objects.get(id=2)
            value = stock_checks.jan_value
            if (form.cleaned_data['stock_request'] * value) < player_information.players_liquid_money:
                player_amount = stocks_info.objects.get(id=2)
                new_DIS = form.cleaned_data['stock_request'] + player_amount.amount_owned
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                new_money = player_information.players_liquid_money - (form.cleaned_data['stock_request'] * value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 2", (new_DIS,))
                con.commit()
            else: 
                error_message = "You don't have enough money for this purchase."
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_information.players_total_money,
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
    if request.method == "POST": 
        form = stockForm(request.POST)
        if form.is_valid():
            stock_checks = stocks_info.objects.get(id=2)
            value = stock_checks.jan_value
            player_amount = stocks_info.objects.get(id=2)
            if player_amount.amount_owned >= form.cleaned_data['stock_request']:

                new_DIS = form.cleaned_data['stock_request'] + player_amount.amount_owned
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                new_money = player_information.players_liquid_money + (form.cleaned_data['stock_request'] * value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 2", (new_DIS,))
                con.commit()
            else: 
                error_message = "You don't have that many to sell!"
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_information.players_total_money,
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
    if request.method == "POST": 
        form = stockForm(request.POST)
        if form.is_valid():
            stock_checks = stocks_info.objects.get(id=3)
            value = stock_checks.jan_value
            if (form.cleaned_data['stock_request'] * value) < player_information.players_liquid_money:
                player_amount = stocks_info.objects.get(id=3)
                new_MSFT = form.cleaned_data['stock_request'] + player_amount.amount_owned
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                new_money = player_information.players_liquid_money - (form.cleaned_data['stock_request'] * value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 3", (new_MSFT,))
                con.commit()

            else: 
                error_message = "You don't have enough money for this purchase."
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_information.players_total_money,
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
    if request.method == "POST": 
        form = stockForm(request.POST)
        if form.is_valid():
            stock_checks = stocks_info.objects.get(id=2)
            value = stock_checks.jan_value
            player_amount = stocks_info.objects.get(id=3)
            if player_amount.amount_owned >= form.cleaned_data['stock_request']:
            
                new_MSFT = form.cleaned_data['stock_request'] + player_amount.amount_owned
                BASE_DIR = Path(__file__).resolve().parent.parent
                db_path = os.path.join(BASE_DIR, "db.sqlite3")
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                new_money = player_information.players_liquid_money + (form.cleaned_data['stock_request'] * value)
                cur.execute("UPDATE stocks_player_option SET players_liquid_money = ? WHERE id = 1", (new_money,))
                cur.execute("UPDATE stocks_stocks_info SET amount_owned = ? WHERE id = 3", (new_MSFT,))
                con.commit()
            else: 
                error_message = "You don't have that many to sell!"
                context = {
                'form': form,
                'player_name': player_information.player_name.upper(),
                'current_cash': player_information.players_liquid_money,
                'player_worth': player_information.players_total_money,
                'current_month': player_information.current_month.upper(),
                'target_month': player_information.target_month.upper(),
                'worth_target': player_information.worth_target, 
                'stock_info' : stocks_info.objects.all(),
        
                "error_message": error_message.upper() 
                }

                return render(request, 'stocks/index.html', context)

    return redirect('/stocks/')