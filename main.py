
    

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

    tempC: float = (5 / 9) * (temp - 32)

    # Create a dictionary with the weather information
    weather_dict = {
        "city": city,
        "temperature": temp,
        "temperatureC": tempC,
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
    output_label.config(text=f"City: {weather_dict['city']}\nTemperature: {weather_dict['temperature']}°F\nTemperature: {weather_dict['temperatureC']}°C\nFeels Like: {weather_dict['feels_like']}°F\nHumidity: {weather_dict['humidity']}%\nDescription: {weather_dict['description']}")

#root window
root= tk.Tk()
root.title('Weather')
root.configure(bg='#0F2830')
root.geometry('700x700')

# Create the GUI window
window = tk.Frame(root, bg="#014751")
window.place(relwidth=0.95, relheight=0.95, relx=0.025, rely=0.025)

# Create the GUI widgets
title_label = tk.Label(window, text="Weather App", font=("Arial", 30), bg='#FFEEB4')
city_label = tk.Label(window, text="Enter a city name:", font=("Arial", 24), bg='#00D37F',)
city_entry = tk.Entry(window, font=("Arial", 24), bg='#AFF8C8')
submit_button = tk.Button(window, text="Get Weather", command=show_weather, font=("Arial", 24),  bg='#D2C4FB')
output_label = tk.Label(window, font=("Arial", 24), bg='#AFF8C8')

# Add the widgets to the window
title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
city_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
city_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
submit_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
output_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Run the GUI event loop
window.mainloop()
