from cProfile import label
from tkinter.ttk import LabeledScale
from turtle import back
from django.shortcuts import render, redirect
from .models import background, shortcut, stock, weather
from .forms import shortcutForm, stockForm, weatherForm
import favicon
import os
import requests, json
from PIL import Image

from yahooquery import Ticker
from yahoo_fin import stock_info
from datetime import datetime as dt, timedelta, timezone
import datetime
import numpy as np

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

    # Check if home screen has any widgets, return if false
    if stock.objects.exists() == False and weather.objects.exists() == False:
        shortcut_context = {
        'shortcuts': shortcuts,
        'shortcut_list': shortcut_list,
         }
        return shortcut_context 

    # Calculate if data should be updated, updates every 5 mins.

    try:
        stocks = stock.objects.all()
        timestamps = []
        for i in stocks.iterator():
            timestamps.append(i.last_update)
        date_time_str = timestamps[0]
    except:
        cities = weather.objects.all()
        timestamps = []
        for i in cities.iterator():
            timestamps.append(i.last_update)
        date_time_str = timestamps[0]
            
    date_time_obj = dt.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    last_update = dt.today() - date_time_obj

    minutessince = int(last_update.total_seconds() / 60)
    
    if minutessince > 5:
        update_stock_database()
        update_weather_database()

    # Get context 

    stocks = stock.objects.all()
    cities = weather.objects.all()

    shortcut_context = {
        'shortcuts': shortcuts,
        'shortcut_list': shortcut_list,
        'stocks': stocks,
        'cities': cities
    }

    return shortcut_context 


def home(request):

    context = get_data()

    backgrounds = background.objects.all()
    for i in backgrounds.iterator():
        if i.status == "active":
            current_background = i.name

    form = stockForm()
    form2 = weatherForm()
    form3 = shortcutForm()
    context['form'] = form
    context['form2'] = form2
    context['form3'] = form3
    context['site_background'] = current_background
    context['backgrounds'] = backgrounds

    if 'submit-form1' in request.POST:
        form = stockForm(request.POST)
        if form.is_valid():
            try:
                stock_info.get_live_price(form.instance.ticker)

                test = form.save(commit=False)
                test.last_update= dt.today()
                test.save()

                stocks = stock.objects.all()
                update_stocks = []

                index = 0
                for i in stocks.iterator():
                    update_stocks.append(i.ticker)
                    i.ticker = update_stocks[index]
                    i.save()
                    index += 1 
                
                update_stock_database()

                return redirect('home')

            except Exception as error:
                print(error)

    if 'submit-form2' in request.POST:
        form2 = weatherForm(request.POST)
        if form2.is_valid():
            try:
                # Check if city exists
                BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
                CITY = "Lappeenranta"
                API_KEY = "80a0b6e9e8019ea97ceb2137ba302c7b"

                URL = BASE_URL + "q=" + CITY + "&units=metric&appid=" + API_KEY

                # HTTP request
                requests.get(URL)

                # If city exists continue

                test = form2.save(commit=False)
                test.last_update = dt.today()
                test.save()

                cities = weather.objects.all()
                update_cities = []

                index = 0
                for i in cities.iterator():
                    update_cities.append(i.city)
                    i.city = update_cities[index]
                    i.save()
                    index += 1 

                update_weather_database()

                return redirect('home')

            except Exception as error:
                print(error)

    if 'remove-widgets' in request.POST:
        stockWidgets = stock.objects.all()
        stockWidgets.delete()
        weatherWidgets = weather.objects.all()
        weatherWidgets.delete()


    if 'addShortcut' in request.POST:
        form3 = shortcutForm(request.POST)
        if form3.is_valid():

            form3.save()

            # Get site icon

            try:
            
                url = favicon.get(form3.instance.site_url)
                url = url[0].url

                # With youtube shortcut use custom icon
                if "youtube" in url:
                    path = r'C:\Users\iirok\OneDrive\Desktop\HomePage\main\home\static\img'
                    output = os.path.join(path, "youtube_default.png")
                    image = Image.open(output)
                    output = os.path.join(path, str(form3.instance.name) + ".png")
                    image.save(fp=output)
                    return redirect('home')

                # With google use custom icon
                if "google" in url or "Google" in url or "drive" in url:
                    path = r'C:\Users\iirok\OneDrive\Desktop\HomePage\main\home\static\img'
                    output = os.path.join(path, "google_default.png")
                    image = Image.open(output)
                    output = os.path.join(path, str(form3.instance.name) + ".png")
                    image.save(fp=output)
                    return redirect('home')

                # Download icon from site

                path = r'C:\Users\iirok\OneDrive\Desktop\HomePage\main\home\static\img'
                output = os.path.join(path, str(form3.instance.name) + ".png")

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
                output = os.path.join(path, str(form3.instance.name) + ".png")
                image.save(fp=output)
              
            return redirect('home')
 
    return render(request, "home/base.html", context)

def delete_shortcut(request, item_id):
    item = shortcut.objects.get(pk=item_id)
    item.delete()

    try:
        to_delete = os.path.join(r'C:\Users\iirok\OneDrive\Desktop\HomePage\main\home\static\img', str(item) + str(".png"))
        os.remove(to_delete)
    except:
        pass

    return redirect('home')

def update_stock_database():

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
    

    x = stock.objects.all()

    index = 0
    for i in x.iterator():

        # Update current price
        i.current_price = round(stock_info.get_live_price(stocks[index]),3)
        
        # Update historical prices
        i.stock_prices = data[index]

        # Update dates
        i.dates = labels[0]

        # Update colors
        i.chart_colors = colors[index]

        # Update last-update time
        i.last_update = dt.today()

        i.save()
        index += 1

def update_weather_database():

    cities = weather.objects.all()

    for i in cities.iterator():
   
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        CITY = i.city
        API_KEY = "80a0b6e9e8019ea97ceb2137ba302c7b"

        URL = BASE_URL + "q=" + CITY + "&units=metric&appid=" + API_KEY

        # HTTP request
        response = requests.get(URL)
        # checking the status code of the request
        if response.status_code == 200:
            # getting data in the json format
            data = response.json()
            # getting the main dict block
            main = data['main']
            wind = data['wind']
            # weather report
            report = data['weather']
            sun = data['sys']

            # Get local timezone

            seconds = data['timezone']
            local_timezone = datetime.timedelta(seconds=seconds)

            # Get local time

            utc_time = dt.utcnow()
            local_time = utc_time + local_timezone

            # Calculate user timezone
            my_timezone = dt.now() - utc_time

            # Calculate sunrise and sunrise times, substract local + user timezone
            sunrise = dt.fromtimestamp(sun['sunrise']) + (local_timezone - my_timezone)
            sunset = dt.fromtimestamp(sun['sunset']) + (local_timezone - my_timezone)

            if sunrise < local_time < sunset:
                    local_time = "day"
            else:
                    local_time = "night"

            i.temperature = round(int(main['temp']),1)
            i.condition = report[0]['description']
            i.humidity = main['humidity']
            i.wind_speed = wind['speed']
            i.time = local_time
            i.last_update = dt.today()
            i.save()

def change_background(request, background_id):

    backgrounds = background.objects.all()

    # Set current background as inactive

    for i in backgrounds.iterator():
        if i.status == "active":
            i.status = "inactive"
        i.save()

    # Set new backgrounds as active

    new_background = background.objects.get(id = background_id)
    new_background.status = "active"
    new_background.save()
    
    return redirect('home')

    
# To do
# Fix weather icons
# Rework shortcut form
# Add login with google
# Add google apps
# Add background from files (optional)

# Done 26.4
# Added time variable to weather widgets, now displays day or night icons
# Added default shortcut icon for google
# Added background menu

# Done 25.4
# Added weather widget
# Reworked shortcut buttons
# Added delete button to widgets

# Done 24.4
# Added stock chart widgets
# Set stock widgets data to database and update it every 5 mins
# Added widget menu





    

    
    




