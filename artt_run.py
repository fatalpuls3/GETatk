import os4690
import os
import sys


def getargs():
    global arttrun_path
    global customer
    global zipfile
    global current_case
    argcount = len(sys.argv)

    if argcount != 3:
        sys.exit('You did not provide enough arguments, please specify customer name and test case')
    elif argcount == 3:
        arttrun_path = 'f:/arttchecks/'
        current_case = sys.argv[2]
        print('Current Case: ' + current_case)
        customer = sys.argv[1]
    else:
        print("Process ended, nothing was processed")


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


# def backuprun():
#     print('=================================')
#     print('Backing up ARTT Runs')
#     print('=================================')
#     os.chdir(arttrun_path + customer)
#     print('Current Case: ' + current_case)
#     os4690.system('adxnszzl -c -AD -r ' + zipfile + arttrun_path + customer + "/" + current_case)


def ftpnotify():
    print('============================================')
    print('ARTT Run backed up!')
    print('Location: f:/arttcheck')
    os4690.system('python2 f:/tools/artt_ftp.py ' + customer + ' ' + current_case)
    print('ARTT Run FTP complete!')
    os4690.system('python2 f:/tools/artt_notify.py ' + customer + ' ' + current_case)
    print('Notification sent for ARTT Run!')
    print('============================================')


getargs()
# makedirs()
# backuprun()
ftpnotify()
