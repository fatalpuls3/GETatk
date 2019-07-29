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
arttrun_dir = 'f:/arttchecks'
customer = sys.argv[1]
current_case = (sys.argv[2].upper())
fullpath = (arttrun_dir + '/' + current_case)

# for root, dirs, files in os.walk(arttrun_dir, topdown=True):
#     fullpath = (arttrun_dir + '/' + current_case)
#     relative = root[len(arttrun_dir):].lstrip(os.sep)
#     for d in dirs:
#         try:
#             ftp.mkd(os.path.join(relative, customer + '\\' + uploaddate + '_' + d))
#         except:
#             pass
try:
    ftp.mkd(os.path.join(customer + '\\' + uploaddate + '_' + current_case))
except:
    pass

try:
    for filename in os.listdir(fullpath):
        if filename.endswith(".txt"):
            ftp.cwd(customer + "\\" + uploaddate + '_' + current_case)
            ftp.storbinary('STOR ' + filename, open(os.path.join(fullpath, filename), 'rb'))
            ftp.cwd('/')
        else:
            continue
except:
    pass

ftp.quit()
