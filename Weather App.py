import datetime
import tkinter as tk
import requests




API_KEY = '426a46830840bd955c882113c09f7215'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather():
    """Fetch weather data for the specified city and update the result label"""
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city name.")
        return 
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units':'metric' 
    
  
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()

        # Extract relevant weather data 
        sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')

        weather_description = data['weather'][0]['description'].capitalize()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Prepare output string 
        output = (f"Weather in {city.capitalize()}:\n"
          f"Description: {weather_description}\n"
          f"Temperature: {temperature}°C\n"
          f"Humidity: {humidity}%\n"
          f"Pressure: {data['main']['pressure']} hPa\n"
          f"Wind Speed: {wind_speed} m/s\n"
          f"Visibility: {data.get('visibility', 'N/A')} m\n"
          f"Sunrise: {sunrise_time}\n"
          f"Sunset: {sunset_time}")
    except requests.exceptions.HTTPError:
        output = "City not found or error occurred. Please check the city name and try again."
    except Exception as e:
        output = f"An error occurred: {e}"

    result_label.config(text=output)
# Create the main window 
root = tk.Tk()
root.title("Weather App")

# Create and pack widgets 
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

city_label = tk.Label(frame, text="Enter City:")
city_label.grid(row=0, column=0, pady=5)

city_entry = tk.Entry(frame, width=25)
city_entry.grid(row=0, column=1, pady=5)

get_weather_button = tk.Button(frame, text="Get Weather", command=get_weather)
get_weather_button.grid(row=1, column=0, columnspan=2, pady=10)

result_label = tk.Label(frame, text="", justify=tk.LEFT, font=("Helvetica", 10))
result_label.grid(row=2, column=0, columnspan=2, pady=10)

root.configure(bg='#e0f7fa') # Set a background color for the main window

# Customize the frame 
frame = tk.Frame(root, padx=20, pady=20, bg='#e0f7fa')
frame.pack()

# Customize labels with fonts and colors 
city_label = tk.Label(frame, font=("Helvetica", 12, "bold"), bg='#e0f7fa')
city_label.grid(row=0, column=0, pady=5, sticky="w")

result_label = tk.Label(frame, text="", justify=tk.LEFT, font=("Helvetica", 11), bg='#e0f7fa')
result_label.grid(row=2, column=0, columnspan=2, pady=10)



# Run the Tkinter event loop
root.mainloop()



