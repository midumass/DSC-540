"""
# DSC-540-T301 Assignment 9.2
# Zach Hill
# 03AUG2019
"""

import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import email.encoders
import os
import smtplib

# Request input from user
print("This is Zach Hill's Assignment 9.2 script")
userInputCompany = input('Enter your company name: ')
userInputFeet = input('Enter number of feet for installation: ')

# Define logging function
def start_logger():
    logging.basicConfig(filename='./daily_report_%s.log' %
                    datetime.strftime(datetime.now(), '%m%d%Y_%H%M%S'),
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

def mail(to, subject, text, attach=None, config=None):
    msg = MIMEMultipart()
    msg['From'] = ('<email address>')
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    if attach:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        email.encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login('<email address>',
                     '')
    # password removed for obvious reasons
    mailServer.sendmail('<email address>', to, msg.as_string())
    mailServer.close()

# Calculate cost per foot based on user input
def priceFunction(numberOfFeet):
	costOfCable = 0.87
	if numberOfFeet > 100:
		costOfCable = 0.80
		if numberOfFeet > 250:
			costOfCable = 0.70
			if numberOfFeet > 500:
				costOfCable = 0.50
	return costOfCable;

# Take calculated cost and multiply by requested number of feet
# Write Company name and calculations to screen
def costFunction(feet,price):
	totalCost = feet * price
	print(userInputCompany + "'s cost of installation for " + str(feet) + ' feet of optical cable is: $' + f'{(totalCost):.2f}');

# Validate requested input. Rerequest if improper literal is entered.
# Complete calculations if successful
# added simple logging to find when users enter bad input. 
def userInput(receivedInputFeet):
    start_logger()
    logging.debug("SRIPT: I'm starting to do things")
    
    try:
        userInputFeet = float(receivedInputFeet)
        priceCalc = priceFunction(userInputFeet)
        costFunction(userInputFeet,priceCalc)

    except:
        logging.exception("SCRIPT: There was a problem!")
        logging.error("SCRIPT: non-numeric value found")
        print(receivedInputFeet + ' is not a number. Please enter a number')
        userInputFeet = input('Enter number of feet for installation: ')
        userInput(userInputFeet);
        # Removed to hide email address
        # mail('<email address>', 'FAILURE',
        #     'Unsuccessful user data entry')
        
    logging.debug("SCRIPT: I'm done doing things")
    # Removed to hide email address
    # mail('<email address>', 'SUCCESS', 'Successful user data entry')
    
userInput(userInputFeet);