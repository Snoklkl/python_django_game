# Generated by Django 3.2.3 on 2021-07-02 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0011_stocks_info_amount_owned'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks_info',
            name='past_dec_value',
            field=models.FloatField(default=0.0),
        ),
    ]
