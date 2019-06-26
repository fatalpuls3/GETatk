# Automated Test Tool Notification Script
# Author: Jason Miller
# 6/17/2019
# Version 1.0

import smtplib
import os
import sys
from time import strftime

login = 'GetronicsAutomation@gmail.com'
password = 'QAtest123'
emailfile = '.\\emails.txt'  # email file with one address per line for script to send notification to
defaddr = 'jason.miller@getronics.com'  # Default email for TO if emails.txt doesnt exist
toaddrs = []


def createmessage():
    global current_case
    global msg
    current_case_file = 'C:\\REGRESSN\\CASES\\CURRENT.CSE'
    if not os.path.exists(current_case_file):
        sys.exit('Unable to find current case file')
    else:
        with open(current_case_file) as csfile:
            for line in csfile:
                current_case = line
    rundatetime = strftime("%Y-%m-%d - %H:%M:%S")
    msg = 'Subject: {}\n\n{}'.format(current_case + ' - Automated Test Run Completed!',
                                     'Test Case: ' + current_case +
                                     '\nRun Date/Time: ' + rundatetime +
                                     '\n\n***Pull all automated run logs back to your system for triage.***')


def emailfilecheck():  # check if email.txt file exists
    global emailfilexists
    emailfilexists = -1
    if not os.path.exists(emailfile):
        emailfilexists = 0
    elif os.path.exists(emailfile):
        emailfilexists = 1
        with open(emailfile, 'r') as emails:
            for line in emails:
                toaddrs.append(line)
    else:
        sys.exit('***Unable to send email***')


def sendemail():  # Send email file based on emailfileexists value
    global toaddrs
    global defaddr
    if emailfilexists == 1:
        for a in toaddrs:
            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login(login, password)
                server.sendmail(login, toaddrs, msg)
                server.quit()
                print('Sent notification to ' + str(toaddrs))
            except smtplib.SMTPException:
                sys.exit("***Unable to send emails to email.txt list!***")
    else:
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(login, password)
            server.sendmail(login, defaddr, msg)
            server.quit()
            print('Sent notification to ' + defaddr)
        except smtplib.SMTPException:
            sys.exit("***Unable to send emails to default email address!***")


createmessage()
emailfilecheck()
sendemail()
