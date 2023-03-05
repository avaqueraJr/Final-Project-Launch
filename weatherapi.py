from fastapi import FastAPI
import requests
import json

app = FastAPI()

@app.get("/weather/{city}")
def get_weather(city: str):
    # Replace the spaces in the city name with %20 to make it URL safe
    city = city.replace(" ", "%20")

    # Get the API key from the OpenWeatherMap website
    api_key = "8b9d4011d9dbf283bab6b60609ca631c"

    # Send the request to the OpenWeatherMap API and get the response
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    # Parse the JSON response and get the relevant weather information
    weather_info = json.loads(response.text)
    temp_celsius = weather_info["main"]["temp"]
    temp_fahrenheit = (temp_celsius * 1.8) + 32
    feels_like_celsius = weather_info["main"]["feels_like"]
    feels_like_fahrenheit = (feels_like_celsius * 1.8) + 32
    humidity = weather_info["main"]["humidity"]
    description = weather_info["weather"][0]["description"]

    # Create a dictionary with the weather information
    weather_dict = {
        "city": city,
        "temperature_celsius": temp_celsius,
        "temperature_fahrenheit": temp_fahrenheit,
        "feels_like_celsius": feels_like_celsius,
        "feels_like_fahrenheit": feels_like_fahrenheit,
        "humidity": humidity,
        "description": description
    }

    return weather_dict
 #hello