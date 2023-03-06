import tkinter as tk
import requests
import json

def get_weather(city):
    # Replace the spaces in the city name with %20 to make it URL safe
    city = city.replace(" ", "%20")

    # Get the API key from the OpenWeatherMap website
    api_key = "8b9d4011d9dbf283bab6b60609ca631c"

    # Send the request to the OpenWeatherMap API and get the response
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    response = requests.get(url)

    # Parse the JSON response and get the relevant weather information
    weather_info = json.loads(response.text)
    temp = weather_info["main"]["temp"]
    feels_like = weather_info["main"]["feels_like"]
    humidity = weather_info["main"]["humidity"]
    description = weather_info["weather"][0]["description"]

    # Create a dictionary with the weather information
    weather_dict = {
        "city": city,
        "temperature": temp,
        "feels_like": feels_like,
        "humidity": humidity,
        "description": description
    }

    return weather_dict

def show_weather():
    city = city_entry.get()
    weather_dict = get_weather(city)

    # Clear any previous weather data from the output label
    output_label.config(text="")

    # Set the text of the output label with the weather data
    output_label.config(text=f"City: {weather_dict['city']}\nTemperature: {weather_dict['temperature']}°F\nFeels Like: {weather_dict['feels_like']}°F\nHumidity: {weather_dict['humidity']}%\nDescription: {weather_dict['description']}")

# Create the GUI window
window = tk.Tk()

# Create the GUI widgets
title_label = tk.Label(window, text="Weather App", font=("Arial", 24))
city_label = tk.Label(window, text="Enter a city name:")
city_entry = tk.Entry(window)
submit_button = tk.Button(window, text="Get Weather", command=show_weather)
output_label = tk.Label(window, font=("Arial", 16))

# Add the widgets to the window
title_label.pack()
city_label.pack()
city_entry.pack()
submit_button.pack()
output_label.pack()

# Run the GUI event loop
window.mainloop()


