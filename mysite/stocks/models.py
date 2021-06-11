from django.db import models

# Create your models here.

class stocks_info(models.Model):
    jan_value = models.IntegerField(default=0)
    feb_value = models.IntegerField()
    mar_value = models.IntegerField()
    april_value = models.IntegerField()
    may_value = models.IntegerField()
    june_value = models.IntegerField()
    july_value = models.IntegerField()
    aug_value = models.IntegerField()
    sept_value = models.IntegerField()
    oct_value = models.IntegerField()
    nov_value = models.IntegerField()
    december_value = models.IntegerField()
    stock_symbol = models.CharField(max_length=4)

class player_info(models.Model):
    player_name = models.CharField(max_length=16)
    player_year = models.IntegerField(default=2020)
    players_liquid_money = models.IntegerField()
    players_total_money = models.IntegerField()
    stock_1 = models.IntegerField()
    stock_2 = models.IntegerField()
    stock_3 = models.IntegerField()
    stock_4 = models.IntegerField()
    stock_5 = models.IntegerField()
    stock_6 = models.IntegerField()
    stock_7 = models.IntegerField()
    stock_8 = models.IntegerField()
    stock_9 = models.IntegerField()
    stock_10 = models.IntegerField()

class player_targets(models.Model):
    march_target = models.IntegerField()
    june_target = models.IntegerField()
    sept_target = models.IntegerField()
    december_target = models.IntegerField()

class time_trackers(models.Model):
    actions_base = models.IntegerField(default=5)
    current_month = models.CharField(max_length=16, default='January')
    target_month = models.CharField(max_length=16, default="March")
