from django.shortcuts import render
import datetime
import requests
from django.contrib import messages

# Create your views here.
def climate(request):
    API_KEY="d8614ff24d40e059c1e52f8c1cc1b3d1"
    current_weather_url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url="https://api.openweathermap.org/data/2.5/onecall?lat={}&exclude=current,minutely,hourly,alerts&appid={}"
    if request.method == "POST":
        city1 = request.POST["city1"]
        city2 = request.POST.get("city", None)

        try:
            weather_data1, daily_forecasts1 = fetch_weather_and_forecast(
                city1, API_KEY, current_weather_url, forecast_url
            )
        except KeyError:
            messages.error(request, " Please enter a valid city name.")
            weather_data1 = None
            daily_forecasts1 = None

        try:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(
                city2, API_KEY, current_weather_url, forecast_url
            )
        except KeyError:
            messages.error(request, "Invalid city name entered for City 2. Please enter a valid city name.")
            weather_data2 = None
            daily_forecasts2 = None
    # if request.method=="POST":
    #     city1=request.POST['city1']
    #     city2=request.POST.get('city',None)
    #     weather_data1,daily_forecasts1=fetch_weather_and_forecast(city1,API_KEY,current_weather_url,forecast_url)
        
    #     if city2:
    #         weather_data2,daily_forecasts2=fetch_weather_and_forecast(city2,API_KEY,current_weather_url,forecast_url)

    #     else:
    #         weather_data2,daily_forecasts2=None,None

        context={
            "weather_data1":weather_data1,
            "daily_forecasts1":daily_forecasts1,
            "weather_data2":weather_data2,
            "daily_forecasts2":daily_forecasts2
        } 
        return render(request,"weather.html",context)    
    else:
        return render(request,"weather.html")
    

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Get current weather data for the specified city
    response = requests.get(current_weather_url.format(city, api_key)).json()
    
    # Extract latitude and longitude from the current weather response
    lat, lon = response['coord']['lat'], response['coord']['lon']
    
    # Get the weather forecast data for the next 5 days (excluding current day, hourly, minutely, and alerts)
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    # Extract relevant information from the current weather response
    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    # Extract daily forecasts for the next 5 days
    daily_forecasts = []
    if 'daily' in forecast_response:
        for daily_data in forecast_response['daily'][:5]:
            daily_forecasts.append({
                "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
                "min_temp": round(daily_data['temp']['min'] - 273.15, 2),
                "max_temp": round(daily_data['temp']['max'] - 273.15, 2),
                "description": daily_data['weather'][0]['description'],
                "icon": daily_data['weather'][0]['icon']
            })
    else:
        print("Daily forecast data not available")

    return weather_data, daily_forecasts
