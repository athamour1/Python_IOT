import time
import requests
import math
import random
import Adafruit_DHT
import smtplib, ssl
from getpass import getpass
TOKEN = "..."  # Put your TOKEN here
DEVICE_LABEL = "Raspberry_pi_4"  # Put your device label here
VARIABLE_LABEL_1 = "temperature:"  # Put your first variable label here
VARIABLE_LABEL_2 = "humidity:"  # Put your second variable label here
#-------------------------------------------------------------
sensor = Adafruit_DHT.DHT11
DHT11_pin = 22
#-------------------------------------------------------------
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "..."  # Enter your address
receiver_email = "..."  # Enter receiver address
password = " "
def build_payload(variable_1, variable_2):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT11_pin)
    if humidity is not None and temperature is not None:
      print('Temperature={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
      print('Failed to get reading from the sensor. Try again!')
    if temperature>21.0 and humidity>59.0:
        sendemail(temperature, humidity)
    payload = {variable_1: temperature,
                variable_2: humidity}
    return payload
def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)
    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check your token credentials and internet connection")
        return False
    print("[INFO] request made properly, your device is updated")
    return True
 #-------------------------------------------------------------
# smtp model
 #              +----------+                +----------+
 #  +------+    |          |                |          |
 #  | User |<-->|          |      SMTP      |          |
 #  +------+    |  Sender- |Commands/Replies| Receiver-|
 #  +------+    |   SMTP   |<-------------->|    SMTP  |    +------+
 #  | File |<-->|          |    and Mail    |          |<-->| File |
 #  |System|    |          |                |          |    |System|
 #  +------+    +----------+                +----------+    +------+
 #               Sender-SMTP                Receiver-SMTP
 #                          Model for SMTP Use
 #                               Figure 1
 #    -------------------------------------------------------------
def sendemail(temp1, hum1):
    message = """\
    Subject: Warning: Temperature and humidity are rising!
    This email is sent because the temperature and humidity doesn't seem normal..
    Current status: Temperature:""" +str(temp1)+"  Humidity:"+str(hum1)
    """Please check if everything is ok."""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
def main():
    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2)
    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")
if _name_ == '_main_':
    password=getpass()
    while (True):
        main()
        time.sleep(1)