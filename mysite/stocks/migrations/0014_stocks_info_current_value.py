# Generated by Django 3.2.3 on 2021-07-27 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0013_alter_stocks_info_stock_symbol'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks_info',
            name='current_value',
            field=models.FloatField(default=0.0),
        ),
    ]
