# Generated by Django 4.0.3 on 2022-04-24 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_stock_chart_colors_stock_dates_stock_stock_prices'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='current_price',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='chart_colors',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='stock',
            name='dates',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_prices',
            field=models.CharField(max_length=5000),
        ),
    ]