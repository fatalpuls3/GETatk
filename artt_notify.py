# Automated Test Tool Notification Script
# Author: Jason Miller
# 7/27/2019
# Version 1.0

import smtplib
import os
import sys
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formatdate
from time import strftime


customer = sys.argv[1]
current_case = (sys.argv[2].upper())
arttrun_dir = 'f:/arttchecks'
fullpath = (arttrun_dir + '/' + current_case)
files = []
login = 'GetronicsAutomation@gmail.com'
password = 'QAtest123'
emailfile = '.\\emails.txt'  # email file with one address per line for script to send notification to
defaddr = 'jason.miller@getronics.com'  # Default email for TO if emails.txt doesnt exist
rundatetime = strftime("%Y-%m-%d - %H:%M:%S")

message = (customer + ' - ' + current_case + ' - Automated Test Run Completed!',
           '\nCustomer: ' + customer +
           '\nTest Case: ' + current_case +
           '\nRun Date/Time: ' + rundatetime)


def emailfilecheck():  # check if email.txt file exists
    global emailfilexists
    global toaddrs
    emailfilexists = -1
    if not os.path.exists(emailfile):
        emailfilexists = 0
        toaddrs = defaddr
    elif os.path.exists(emailfile):
        emailfilexists = 1
        with open(emailfile, 'r') as emails:
            for line in emails:
                toaddrs = line
    else:
        sys.exit('***Unable to send email***')


def gather_run_results():
    global files
    os.chdir(fullpath)
    try:
        for filename in os.listdir(fullpath):
            if filename.endswith(".txt"):
                files.append(filename)
            else:
                continue
    except:
        pass


def send_mail(send_from, send_to, subject, text, files=None,
              server="smtp.gmail.com:587"):
    # assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files:
        print(f)
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.starttls()
    smtp.login(login, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


emailfilecheck()
gather_run_results()
send_mail(login, toaddrs, customer + ' - ' + current_case + ' - Automated Test Run Completed!',
          '\nCustomer: ' + customer +
          '\nTest Case: ' + current_case +
          '\nRun Date/Time: ' + rundatetime, files)
