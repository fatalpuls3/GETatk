import os4690
import os
import sys


def getargs():
    global arttrun_path
    global customer
    global zipfile
    global current_case_dir
    global current_case
    if len(sys.argv) < 2:
        sys.exit('You did not provide enough arguments, please specify customer name')
    elif len(sys.argv) == 2:
        arttrun_path = 'f:/arttruns/'
        current_case_file = 'c:/regressn/cases/current.cse'
        with open(current_case_file, 'r') as f:
            current_case = f.readline()
        print('Current Case: ' + current_case)
        customer = sys.argv[1]
        zipfile = current_case + '.zip'
        current_case_dir = str(current_case + '.DIR')


def makedirs():
    print('===============================')
    print('Beginning ARTT Run Backup')
    print('===============================')
    if not os.path.exists(arttrun_path):
        os.mkdir(arttrun_path)
    elif not os.path.exists(arttrun_path + customer):
        os.mkdir(arttrun_path + customer)
    else:
        print("Expected directories exist")


def backuprun():
    print('=================================')
    print('Backing up ARTT Runs')
    print('=================================')
    os.chdir(arttrun_path + customer)
    print('Current Case: ' + current_case)
    os4690.system('adxnszzl -c -AD -r ' + zipfile + ' c:/REGRESSN/CASES/' + current_case_dir + "/*.*")


def ftpnotify():
    print('============================================')
    print('ARTT Run backed up!')
    print('Location: f:/arttruns')
    os4690.system('python2 f:/tools/artt_ftp.py')
    print('ARTT Run FTP complete!')
    os4690.system('python2 f:/tools/artt_notify.py')
    print('Notification sent for ARTT Run!')
    print('============================================')


getargs()
makedirs()
backuprun()
ftpnotify()
