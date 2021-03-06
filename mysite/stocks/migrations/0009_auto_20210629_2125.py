# Generated by Django 3.2.3 on 2021-06-30 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0008_auto_20210629_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='player_option',
            name='action_economy',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='player_option',
            name='current_month',
            field=models.CharField(default='January', max_length=16),
        ),
        migrations.AddField(
            model_name='player_option',
            name='target_month',
            field=models.CharField(default='March', max_length=16),
        ),
    ]
