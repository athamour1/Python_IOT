import time
import requests
import math
import random
from sense_emu import SenseHat
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sense = SenseHat()

# Ubidots ---------------------------------------------------- 
TOKEN = "BBFF-DZKKbJ247xVNIVm1xexbf0FtPneoWk"  # Put your TOKEN here
DEVICE_LABEL = "Sense_Hat"  # Put your device label here 
VARIABLE_LABEL_1 = "temperature"  # Put your first variable label here
VARIABLE_LABEL_2 = "humidity"  # Put your second variable label here
# Email ------------------------------------------------------ 
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "iot.mourtzoukos@gmail.com"  # Enter your address
receiver_email = "thanosmour.tk@gmail.com"  # Enter receiver address
password = "fbRalwC4@a9J0L3K"

message = MIMEMultipart("alternative")
message["Subject"] = "Fire in the Lab"
message["From"] = sender_email
message["To"] = receiver_email
#------------------------------------------------------------- 

def build_payload(variable_1, variable_2):
    # Creates two random values for sending data
    value_1 = sense.temp
    value_2 = sense.humidity
    if value_1 > 21.0 and value_2 > 59.0:
        print("[INFO] Attemping send email")
        sendemail(value_1, value_2)
        print("[INFO] Sended email")
        time.sleep(5)
    payload = {variable_1: value_1,
               variable_2: value_2}
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
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def sendemail(temp1, hum1):
    html = """\
    <html>
        <body>
            <p> <b>Fire !</b> Temperature: """ + str(temp1) + """ Humidity: """ + str(hum1) + """</p>
        </body>
    </html>
    """
    # Temperature: """ + str(temp1) + """
    # Humidity: """ + str(hum1) + """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
    message.attach(MIMEText(html, "html"))
    server.sendmail(sender_email, receiver_email, message.as_string())

def main():
    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2)
    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")

if __name__ == '__main__':
    # password = input()
    while (True):
        main()
        time.sleep(1)