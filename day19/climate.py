import requests

API_KEY = "c95e44e90355840cd84ee88654d8df97"
city = "London"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"


response = requests.get(url=url)
weather_data = response.json()

if response.status_code == 200:
    weather_condition = weather_data["weather"][0]["main"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    print(f"Weather Condition: {weather_condition}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
else:
    print(f"Error: Unable to fetch weather data, Status Code: {response.status_code}")