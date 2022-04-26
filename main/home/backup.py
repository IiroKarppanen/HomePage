from tkinter.ttk import LabeledScale
from django.shortcuts import render, redirect
from .models import shortcut, stock
from .forms import shortcutForm
import favicon
import os
import requests
from PIL import Image

from yahooquery import Ticker
from yahoo_fin import stock_info
from datetime import datetime as dt, timedelta
import datetime
import numpy as np
import pandas as pd


# Create your views here.

def get_data():
    shortcuts = shortcut.objects.all()

    urls = []
    for i in shortcuts.iterator():
        urls.append(i.site_url)

    # Calculate how many add shortcut button to use and make a list
    amount = 10 - shortcut.objects.count()

    shortcut_list = []

    for i in range(amount):
        shortcut_list.append("Add Shortcut")

    # Get stock price

    tickers = stock.objects.all()

    stocks = []
    for i in tickers.iterator():
        stocks.append(i.ticker)

    labels = []
    data = []
    current_prices = []
    colors = []

    index = 0
    for i in stocks:

        ticker = Ticker(stocks[index])
    
        day = dt.today() - timedelta(days=7)

        df = ticker.history(start=day, interval = '1h')
        df.reset_index(inplace=True)
        df = df.rename(columns = {'index':'date'})

        prices = df['open'].values
        dates = df['date'].values

        date = []
        price = []

        for i in prices:
            price.append(round(float(i), 2))

        for i in dates:
            dtt = dt.utcnow()
            dt64 = np.datetime64(dtt)
            ts = (dt64 - np.datetime64(i)) / np.timedelta64(1, 's')
            time = dt.today() - timedelta(seconds=ts)
            time = time.strftime("%d.%m")

            date.append(time)

        current = round(stock_info.get_live_price(stocks[index]),3)
        current_prices.append(current)

        index += 1

        labels.append(date)
        data.append(price)

        if price[0] < price[-1]:
            colors.append("49, 210, 108")
        if price[0] == price[-1]:
            colors.append("49, 210, 108")
        if price[0] > price[-1]:
            colors.append("255, 110, 110")
        

    combined_list = zip(stocks, current_prices)
    combined_list2  = zip(data, colors)

    shortcut_context = {
        'shortcuts': shortcuts,
        'shortcut_list': shortcut_list,
        'labels': labels,
        'current': current,
        'combined_list': combined_list,
        'combined_list2': combined_list2
    }

    return shortcut_context 


def home(request):

    context = get_data()

    return render(request, "home/base.html", context)

def add_shortcut(request):
    context = get_data()
    form = shortcutForm()

    if request.method == 'POST':
        form = shortcutForm(request.POST)
        if form.is_valid():

            form.save()

            # Get site icon

            try:
            
                url = favicon.get(form.instance.site_url)
                url = url[0].url

                # With youtube shortcut use custom icon
          
                if "youtube" in url:
                    path = r'C:\Users\iirok\OneDrive\Desktop\HomePage\main\home\static\img'
                    output = os.path.join(path, "youtube.png")
                    image = Image.open(output)
                    output = os.path.join(path, str(form.instance.name) + ".png")
                    image.save(fp=output)
                    return redirect('home')

                # Download icon from site

                path = r'C:\Users\iirok\OneDrive\Desktop\HomePage\main\home\static\img'
                output = os.path.join(path, str(form.instance.name) + ".png")

                r = requests.get(url)
                with open(output, 'wb') as outfile:
                    outfile.write(r.content)

                # Resize image

                image = Image.open(output)
                ratio = image.size[1] / image.size[0] 
                print(ratio)

                image = image.resize((48,48), resample=Image.NEAREST)
                image.save(fp=output)


            except:

                # Use default icon if site icon is not available

                path = r'C:\Users\iirok\OneDrive\Desktop\HomePage\main\home\static\img'
                output = os.path.join(path, "default_shortcut.png")
                image = Image.open(output)
                output = os.path.join(path, str(form.instance.name) + ".png")
                image.save(fp=output)
              
            return redirect('home')

    context['form'] = form

    return render(request, "home/add_shortcut.html", context)

def delete_shortcut(request, item_id):
    item = shortcut.objects.get(pk=item_id)
    item.delete()

    try:
        to_delete = os.path.join(r'C:\Users\iirok\OneDrive\Desktop\HomePage\main\home\static\img', str(item) + str(".png"))
        os.remove(to_delete)
    except:
        pass

    return redirect('home')

from django.db import models

# Create your models here.

class shortcut(models.Model):
    name = models.CharField(max_length=15)
    site_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class stock(models.Model):
    ticker = models.CharField(max_length=15)

    def __str__(self):
        return self.ticker






