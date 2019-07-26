#  This script generates the after.bat for every test case
#  that does not currently have the after.bat on every reboot
#  to ensure its not forgotten

import os
import shutil
import sys

after_check = 'python2 f:/tools/artt_check.py '
after_run = 'python2 f:/tools/artt_run.py '
after_batch = '/AFTER.BAT'
default_after = 'f:/tools/after.bat'
tc_base_dir = 'c:/REGRESSN/CASES'


def getargs():
    global customer
    if len(sys.argv) < 2:
        sys.exit('You did not provide enough arguments, please specify customer name')
    elif len(sys.argv) == 2:
        customer = sys.argv[1]
        print('Customer: ' + customer)


def createfile():
    dirs = []
    for dirName, subdirList, fileList in os.walk(tc_base_dir):
        if 'setup' in dirName:
            dirs.append(dirName)
            for f in dirs:
                if '/setup/' in f:
                    dirs.remove(f)


    # for dirName, subdirList, fileList in os.walk(tc_base_dir):
    #     if 'setup' in dirName:
    #         dirs.append(dirName)
    #         for f in dirs:
    #             if '/setup/' in f:
    #                 dirs.remove(f)

    for d in dirs:
        if '.DIR' in d.upper():
            open(d + after_batch, 'w').close()
            with open(d + after_batch, 'rw+') as a:
                a.truncate(0)

        try:
            if '.DIR' in d.upper():
                testcase = d.upper()
                testcase = testcase.rstrip('./DIR/SETUP')
                testcase = testcase.lstrip('C:/REGRESSN/CASES')
                with open(d + after_batch, 'rw+') as a:
                    a.writelines('REM File has been edited by artt_after.py\n')
                    a.writelines('REM for use with customer ' + customer + ' test case ' + testcase + '\n')
                    a.writelines(after_check + customer + ' ' + testcase + '\n')
                    a.writelines(after_run + customer + ' ' + testcase + '\n')
                    # shutil.copy(default_after, d + after_batch)
        except:
            pass

    print("All test cases updated with After.bat")
    print("For the following test case directories")
    print(dirs)


getargs()
createfile()
