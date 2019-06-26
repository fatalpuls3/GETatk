# Automated Test Tool FTP Script
# Author: Jason Miller
# 6/17/2019
# Version 1.0

import ftplib
import os
import sys
from time import strftime


server = '172.22.28.141'
username = 'Automation'
password = '4690ftp'
ftp = ftplib.FTP(server, username, password)
uploaddate = strftime("%Y-%m-%d-%H-%M")
arttrun_dir = 'f:/arttruns'

for root, dirs, files in os.walk(arttrun_dir, topdown=True):
    relative = root[len(arttrun_dir):].lstrip(os.sep)
    for d in dirs:
        try:
            ftp.mkd(os.path.join(relative, d))
        except:
            pass

    for f in files:
        try:
            ftp.cwd(relative)
            ftp.storbinary('STOR ' + uploaddate + '_' + f, open(os.path.join(arttrun_dir, relative, f), 'rb'))
            ftp.cwd('/')
        except:
            sys.exit("***Unable to send automation run via FTP!***")

ftp.quit()
