#!/usr/bin/env python3
"""
    Author: Pek, Jonetta
    Date: 5 October 2023
    Purpose: Send email at a specified date and time
"""


import smtplib
import ssl
from email.message import EmailMessage
import credentials


password = input('Enter a password') or credentials.gmail_password
sender_email = credentials.my_email
receiver_email = credentials.my_email
subject = 'Email From Python'
body = 'This is a test email from Python!'

message = EmailMessage()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject
message.set_content(body)

context = ssl.create_default_context()

print('Sending Email!')

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string)

print('Success')

def main():
    pass


if __name__ == '__main__':
    main()