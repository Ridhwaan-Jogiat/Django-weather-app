import random
from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):
    if 'city' in request.POST and request.POST['city'].strip():
        typed_city = request.POST['city'].strip()
    else:
        typed_city = 'Pretoria'

   
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={typed_city}&appid=149d7cf518a0d434d4cbb7bd33c66128"
    PARAMS = {'units': 'metric'}

  
    API_KEY = 'AIzaSyB10DXaUVEweu465U_3GDfn3xVWMgLTdTI'
    SEARCH_ENGINE_ID = 'd5c4e052eeb974599'
    query = typed_city + ' 1920x1080'
    start = 1
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType=image&imgSize=xlarge"


    try:
        image_data = requests.get(city_url).json()
        search_items = image_data.get("items", [])

        if search_items:
           
            image_url = random.choice(search_items)['link']
        else:
            image_url = "https://via.placeholder.com/1920x1080?text=No+Image"


    except:
        image_url = "https://via.placeholder.com/1920x1080?text=Image+Unavailable"

 
    try:
        weather_data = requests.get(weather_url, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        return render(request, 'index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': typed_city.capitalize(),
            'typed_city': typed_city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except:
        messages.error(
            request, 'Entered city not found. Showing default weather for Wakanda.')
        day = datetime.date.today()
        return render(request, 'index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': '25',
            'day': day,
            'city': 'Wakanda',
            'typed_city': typed_city,
            'exception_occurred': True,
            'image_url': "https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600"
        })
