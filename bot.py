import requests
import smtplib
import os
from email.mime.text import MIMEText

CITY = "Thiruvananthapuram"

API_KEY = os.environ["OPENWEATHER_API_KEY"]
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    data = response.json()

    current_temp = data["list"][0]["main"]["temp"]

    temp_alert = current_temp > 35
    rain_alert = False

    for item in data["list"]:
        if item["weather"][0]["main"] == "Rain":
            rain_alert = True
            break

    if temp_alert or rain_alert:

        message = f"Weather Alert for {CITY}\nTemperature: {current_temp}°C\n"

        if temp_alert:
            message += "Temperature is above 35°C\n"
        if rain_alert:
            message += "Rain is predicted\n"

        msg = MIMEText(message)
        msg["Subject"] = "Weather Alert"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            print("Email sent successfully!")

        except Exception as e:
            print("Error:", e)

    else:
        print("No alert needed.")

except Exception as e:
    print("Error:", e)