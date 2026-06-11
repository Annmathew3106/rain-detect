import requests
import os
import sys
sys.stdout.reconfigure(encoding="utf-8")

city = "Thiruvanathapuram"
API_KEY = os.environ["OPENWEATHER_API_KEY"]

EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]



def get_weather():
     url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
     try:
          response=requests.get(url,timeout=20)
          response.raise_for_status()
          return response.text.strip()
     except Exception as e:
          return f"error in getting weather: {e}"


     
    
