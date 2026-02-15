import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 51.507351  # Your latitude
MY_LONG = -1.127758  # Your longitude
my_email = "your@email.com"
password = "yourpassword"


def write_error(message):
    """Will write  message to error file"""
    with open("./log/error.txt", 'a') as error_file:
        error_file.write(f"{message}\n")


# Your position is within +5 or -5 degrees of the ISS position.
def iss_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    else:
        return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def is_dark():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False


while True:
    time.sleep(60)
    if iss_near() and is_dark():
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as connection:
                connection.starttls()
                connection.login(my_email, password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=my_email,
                    msg=f"Subject: Look up\n\n ISS overhead"
                )
        except smtplib.SMTPAuthenticationError:
            write_error("Authentication Error Check Username and Password\n")
