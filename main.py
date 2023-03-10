import tkinter as tk
import requests
import json
from PIL import Image, ImageTk
import datetime

class Weather:
    def __init__(self, city):
        # Replace the spaces in the city name with %20 to make it URL safe
        self.city = city.replace(" ", "%20")

        # Get the API key from the OpenWeatherMap website
        self.api_key = "8b9d4011d9dbf283bab6b60609ca631c"

        # Send the request to the OpenWeatherMap API and get the response
        self.url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=imperial"
        self.response = requests.get(self.url)

        if self.response.status_code != 200:
            raise ValueError(f"Error for {self.city}.Please check the spelling.")

        # Parse the JSON response and get the relevant weather information
        self.weather_info = json.loads(self.response.text)
        self.temp_f = self.weather_info["main"]["temp"]
        self.feels_like_f = self.weather_info["main"]["feels_like"]
        self.humidity = self.weather_info["main"]["humidity"]
        self.description = self.weather_info["weather"][0]["description"]
        
        # Convert Fahrenheit to Celsius
        self.temp_c = round((self.temp_f - 32) * 5/9, 2)
        self.feels_like_c = round((self.feels_like_f - 32) * 5/9, 2)

    def get_clothing_suggestion(self):
        """
        Suggest what type of clothing is needed based on the weather forecast.
        """
        if "cloud" in self.description.lower() or "wind" in self.description.lower():
            return "Wear a light jacket or sweater."
        elif "rain" in self.description.lower():
            return "Wear a raincoat or bring an umbrella."
        elif "snow" in self.description.lower():
            return "Wear a heavy coat and boots."
        else:
            return "Wear appropriate clothing for the temperature."


class GUI:
    def __init__(self, root, weather):
        self.root = root
        self.root.title('Weather')
        self.root.geometry('700x700')
        self.weather = weather

        # Get the current time
        now = datetime.datetime.now()

        # Determine if it's day or night based on the current time
        if now.hour >= 18 or now.hour < 6:
            bg_color = "#333333" #Nighttime color
            fg_color = "#ffffff"
        else:
            bg_color = "#f5f5f5"
            fg_color = "#000000"

        # Set the root window colors
        self.root.configure(bg=bg_color)

        # Create the GUI window
        self.window = tk.Frame(self.root, bg=bg_color)
        self.window.place(relwidth=1, relheight=1)

        # Create the GUI widgets
        self.title_label = tk.Label(self.window, text="Weather App", font=("Arial Bold", 36), bg='#3E3E3E', fg='#f5f5f5')
        self.title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.city_label = tk.Label(self.window, text="Enter a city name:", font=("Arial Bold", 24), bg='#00D37F', fg='#f5f5f5')
        self.city_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.city_entry = tk.Entry(self.window, font=("Arial", 24), bg='#AFF8C8', insertbackground='black')
        self.city_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.submit_button = tk.Button(self.window, text="Get Weather", command=self.show_weather, font=("Arial", 24),  bg='#3e3e3e', fg='#f5f5f5')
        self.submit_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.output_label = tk.Label(self.window, font=("Arial", 24), bg='#f5f5f5')
        self.output_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.icon_label = tk.Label(self.window)

        #Add the widgets to the window
        self.title_label.pack(pady=10)
        self.city_label.pack(pady=10)
        self.city_entry.pack(pady=10)
        self.submit_button.pack(pady=10)
        self.output_label.pack(pady=10)
        self.icon_label.pack(pady=10)

    def show_weather(self):
        city = self.city_entry.get()
        
        try:
            self.weather = Weather(city)
        except ValueError as e:
            self.output_label.config(text=str(e))
            self.icon_label.config(image=None)
            return
        except requests.exceptions.RequestException as e:
            self.output_label.config(text="Error (check spelling or connection)")
            self.icon_label.config(image=None)
            return
        

        # Clear any previous weather data from the output label
        self.output_label.config(text="")
        self.icon_label.config(image=None) 

        # Set the text of the output label with the weather data
        self.output_label.config(text=f"City: {self.weather.city}\nTemperature: {self.weather.temp_f}°F ({self.weather.temp_c}°C)\nFeels Like: {self.weather.feels_like_f}°F ({self.weather.feels_like_c}°C)\nHumidity: {self.weather.humidity}%\nDescription: {self.weather.description}")

        # Show an icon based on the weather description
        if "cloud" in self.weather.description.lower():
            icon_path = "cloud.png"
        elif "rain" in self.weather.description.lower():
            icon_path = "rain.png"
        elif "snow" in self.weather.description.lower():
            icon_path = "snow.png"
        else:
            icon_path = "sun.png"

        icon = Image.open(icon_path)
        icon = icon.resize((100, 100), resample=Image.LANCZOS)
        icon = ImageTk.PhotoImage(icon)
        self.icon_label.config(image=icon)
        self.icon_label.image = icon

        # Change the background color of the window based on the temperature
    def update_temp(self, temp):
        self.temp_value_label.config(text=str(temp))
        if temp < 40:
            self.root.configure(bg="#2C3539")
        elif temp < 70:
            self.root.configure(bg="#FFA07A")
        else:
            self.root.configure(bg="#FF6347")

# Create the root window
root = tk.Tk()

# Create an instance of the Weather class with default values
default_weather = Weather("New York")

# Create an instance of the GUI class
app = GUI(root, default_weather)

# Run the GUI event loop
root.mainloop()

