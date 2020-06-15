import smtplib, ssl
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "iot.mourtzoukos@gmail.com"  # Enter your address
receiver_email = "vaggelisgeo23@gmail.com"  # Enter receiver address
password = "fbRalwC4@a9J0L3K"
message = """/
Subject: Hi there
This message is sent from Python."""
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)