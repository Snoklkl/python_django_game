from django.db import models

# Create your models here.

class stocks_info(models.Model):
    stock_symbol = models.CharField(max_length=5, default="ABC")
    jan_value = models.FloatField(default=0.0)
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
    amount_owned = models.IntegerField(default = 3)
 

class player_option(models.Model):
    player_name = models.CharField(max_length=16, default="player")
    player_year = models.IntegerField(default=2020)
    players_liquid_money = models.FloatField(default=500.0)
    players_total_money = models.FloatField(default=10000.0)
    worth_target = models.FloatField(default=50.0)
    action_economy = models.IntegerField(default=5)
    current_month = models.CharField(max_length=16, default='January')
    target_month = models.CharField(max_length=16, default="March")


    

    

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

 
