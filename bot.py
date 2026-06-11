import requests
import smtplib
import os
import sys
from email.mime.text import MIMEText

sys.stdout.reconfigure(encoding="utf-8")

CITY = "Thiruvananthapuram"

# Secrets (GitHub or local env)
API_KEY = os.environ["OPENWEATHER_API_KEY"]
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

# OpenWeather API
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

        message = f"Weather Alert for {CITY}\n\nTemperature: {current_temp}°C\n\n"

        if temp_alert:
            message += "⚠ Temperature is above 35°C\n"
        if rain_alert:
            message += "🌧 Rain is predicted\n"

        msg = MIMEText(message)
        msg["Subject"] = "Weather Alert"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            print("✅ Email sent successfully!")

        except smtplib.SMTPAuthenticationError as e:
            print("❌ Authentication failed")
            print("Error code:", e.smtp_code)
            print("Error message:", e.smtp_error)

        except smtplib.SMTPException as e:
            print("❌ SMTP error:", str(e))

        except Exception as e:
            print("❌ Unknown error:", str(e))

    else:
        print("No alert needed.")

except Exception as e:
    print("❌ Error fetching weather:", str(e))