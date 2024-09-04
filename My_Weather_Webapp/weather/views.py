import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from django.contrib import messages
from django.urls import reverse

def get_coordinates(city_name):
    geo_url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid=a4314ffdaae2590bf19f7b845b0fe11f'
    try:
        response = requests.get(geo_url.format(city_name)).json()
        if response:
            lat = response[0]['lat']
            lon = response[0]['lon']
            return lat, lon
        else:
            return None, None
    except requests.exceptions.RequestException:
        return None, None

def index(request):
    weather_url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=a4314ffdaae2590bf19f7b845b0fe11f&units=metric'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            
            if not new_city.strip():  # Check if the city name is empty or contains only whitespace
                messages.error(request, 'City name cannot be empty!')
                return redirect(reverse('home'))
            
            lat, lon = get_coordinates(new_city)
            if not City.objects.filter(name=new_city).exists():
                if lat and lon:
                    try:
                        weather_response = requests.get(weather_url.format(lat, lon)).json()
                        print(weather_response)
                        if 'weather' in weather_response:
                            form.save()
                            messages.success(request, 'City added successfully!')
                            return redirect(reverse('home'))
                        else:
                            messages.error(request, 'Unable to retrieve weather data!')
                    except requests.exceptions.RequestException:
                        messages.error(request, 'Error connecting to the weather service!')
                else:
                    messages.error(request, 'City not found!')
            else:
                messages.error(request, 'City already exists!')
        else:
            messages.error(request, 'Invalid form submission!')
    
    # Handle GET request
    form = CityForm()
    cities = City.objects.all()
    
    weather_data = []
    for city in cities:
        lat, lon = get_coordinates(city.name)
        print(lat, lon)
        if lat and lon:
            try:
                weather_response = requests.get(weather_url.format(lat, lon)).json()
                if 'weather' in weather_response:
                    city_weather = {
                        'city': city.name,
                        'temperature': weather_response['main'].get('temp', 'N/A'),
                        'description': weather_response['weather'][0].get('description', 'N/A'),
                        'icon': weather_response['weather'][0].get('icon', 'N/A'),
                    }
                    weather_data.append(city_weather)
            except requests.exceptions.RequestException:
                continue
    
    context = {
        'weather_data': weather_data,
        'form': form,
    }
    print(weather_data)
    
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.filter(name=city_name).delete()
    return redirect('home')
