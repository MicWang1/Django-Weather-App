from django.shortcuts import render
import os
from dotenv import load_dotenv
import requests
from .models import City
from .forms import CityForm

# API Endpoint and Key
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?q={{}}&units=imperial&appid={API_KEY}"


# Create your views here.
def index(request):
    cities = City.objects.all()  # Returns all cities in database
    if request.method == "POST":  # only true if form is submitted
        form = CityForm(request.POST)  # add actual request data to form for processing
        form.save()  # will validate and save if validate

    form = CityForm()
    weather_data = []

    for city in cities:
        city_weather = requests.get(API_ENDPOINT.format(city)).json()

        weather = {
            "city": city,
            "temperature": int((city_weather["main"]["temp"] - 32) * 5 / 9),
            "description": city_weather["weather"][0]["description"],
            "icon": city_weather["weather"][0]["icon"],
        }

        weather_data.append(weather)

    context = {"weather_data": weather_data, "form": form}

    return render(request, "weather/index.html", context)
