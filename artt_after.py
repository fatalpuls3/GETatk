#  This script generates the after.bat for every test case
#  that does not currently have the after.bat on every reboot
#  to ensure its not forgotten

import os
import shutil
import sys

after_seq = 'python2 f:/tools/artt_run.py '
after_batch = '/after.bat'
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
    with open(default_after, 'rw+') as a:
        a.truncate(0)
        a.writelines('REM File has been edited by artt_after.py\n')
        a.writelines('REM for use with customer ' + customer + '\n')
        a.writelines(after_seq + customer)
    for dirName, subdirList, fileList in os.walk(tc_base_dir):
        if 'setup' in dirName:
            dirs.append(dirName)
            for f in dirs:
                if '/setup/' in f:
                    dirs.remove(f)
    for d in dirs:
        try:
            os.remove(d + '/AFTER.BAT')
        except:
            pass
        shutil.copy(default_after, d + after_batch)

    print("All test cases updated with After.bat")
    print("For the following test case directories")
    print(dirs)


getargs()
createfile()
