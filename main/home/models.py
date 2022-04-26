from django.db import models

# Create your models here.

class shortcut(models.Model):
    name = models.CharField(max_length=15)
    site_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class stock(models.Model):
    ticker = models.CharField(max_length=15)
    stock_prices = models.CharField(max_length=5000, blank=True)
    dates = models.CharField(max_length=5000, blank=True)
    chart_colors = models.CharField(max_length=1000, blank=True)
    current_price = models.CharField(max_length=10, blank=True)
    last_update = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.ticker

class weather(models.Model):
    city = models.CharField(max_length=30)
    temperature = models.CharField(max_length=4, blank=True)
    condition = models.CharField(max_length=30, blank=True)
    humidity = models.CharField(max_length=5, blank=True)
    wind_speed = models.CharField(max_length=8, blank=True)
    time = models.CharField(max_length=6, blank=True)
    last_update = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.city


class background(models.Model):
    name = models.CharField(max_length=500)
    status = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name
