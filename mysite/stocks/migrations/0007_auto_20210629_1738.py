# Generated by Django 3.2.3 on 2021-06-29 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_alter_stocks_info_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player_money',
            name='players_beginning_money',
        ),
        migrations.AlterField(
            model_name='player_money',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='player_money',
            name='players_liquid_money',
            field=models.FloatField(default=500.0),
        ),
        migrations.AlterField(
            model_name='player_money',
            name='players_total_money',
            field=models.FloatField(default=10000.0),
        ),
        migrations.AlterField(
            model_name='player_option',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='player_option',
            name='player_name',
            field=models.CharField(default='player', max_length=16),
        ),
        migrations.AlterField(
            model_name='player_target',
            name='december_target',
            field=models.FloatField(default=200.0),
        ),
        migrations.AlterField(
            model_name='player_target',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='player_target',
            name='june_target',
            field=models.FloatField(default=100.0),
        ),
        migrations.AlterField(
            model_name='player_target',
            name='march_target',
            field=models.FloatField(default=50.0),
        ),
        migrations.AlterField(
            model_name='player_target',
            name='sept_target',
            field=models.FloatField(default=150.0),
        ),
        migrations.AlterField(
            model_name='stock_identity',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='stocks_info',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='time_tracker',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
