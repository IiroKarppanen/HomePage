# Generated by Django 4.0.3 on 2022-04-24 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_stock_current_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='last_update',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
