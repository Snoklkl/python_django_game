from django.db import models
from django.db.models.expressions import When

# Create your models here.

#Accepts data from api about the value of the stocks at each month. Also has the stock's symbol, current_value (in relation to game state), and the amount of the stock that is owned by the player.
class stocks_info(models.Model):
    jan_value = models.FloatField(default=0.0)
    amount_owned = models.IntegerField(default = 3)
    feb_value = models.FloatField(default=0.0)
    mar_value = models.FloatField(default=0.0)
    april_value = models.FloatField(default=0.0)
    may_value = models.FloatField(default=0.0)
    june_value = models.FloatField(default=0.0)
    july_value = models.FloatField(default=0.0)
    aug_value = models.FloatField(default=0.0)
    sept_value = models.FloatField(default=0.0)
    oct_value = models.FloatField(default=0.0)
    nov_value = models.FloatField(default=0.0)
    december_value = models.FloatField(default=0.0)
    past_dec_value = models.FloatField(default=0.0)
    stock_symbol = models.CharField(max_length=20, default="ABC")
    current_value = models.FloatField(default=0.0)
 
#Maintains a player state that manages the amount of money the player has, what time it is in game, information about the next check, and player's name and year inputs (this specifically is not currently implemented)
class player_option(models.Model):
    player_name = models.CharField(max_length=16, default="player")
    player_year = models.IntegerField(default=2020)
    players_liquid_money = models.FloatField(default=500.0)
    players_total_money = models.FloatField(default=10000.0)
    worth_target = models.FloatField(default=50.0)
    action_economy = models.IntegerField(default=5)
    current_month = models.CharField(max_length=16, default='January')
    target_month = models.CharField(max_length=16, default="March")

class purchase_history(models.Model):
    stock_symbol = models.CharField(max_length=20, default="None")
    amount_purchased = models.IntegerField(default = 0)
    purchase_method = models.CharField(max_length=16, default="buy")
    when_purchased = models.CharField(max_length=20, default="Blank")
    value_purchased = models.FloatField(default= 0.0)
    
class player_worth_monthly(models.Model):
    worth_end = models.FloatField(default=10000.0)


#Unused models
class time_tracker(models.Model):
    action_economy = models.IntegerField(default=5)
    current_month = models.CharField(max_length=16, default='January')
    target_month = models.CharField(max_length=16, default="March")

class stock_identity(models.Model):
    stock_symbol = models.CharField(max_length=5)

class player_money(models.Model):
    players_liquid_money = models.FloatField(default=500.0)
    players_total_money = models.FloatField(default=10000.0)

class player_target(models.Model):
    march_target = models.FloatField(default=50.0)
    june_target = models.FloatField(default=100.0)
    sept_target = models.FloatField(default=150.0)
    december_target = models.FloatField(default=200.0)

 
