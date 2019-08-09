# Automated Test Tool Results Sifter Script
# Author: Jason Miller
# 8/09/2019
# Version 1.0

import os
import sys
import fileinput

results_file = '_results.txt'
results_list = []
results_to_check = []

argcount = len(sys.argv)


def validate_args():
    global results_location
    if argcount == 2:
        print("=======================================================")
        print("Base directory being reviewed " + sys.argv[1])
        print("=======================================================")
        results_location = sys.argv[1]
        validate_runs()
    elif argcount > 2:
        print("You have entered to many arguments.")
        print("Please only pass 1 argument with the directory you wish to be reviewed")
        sys.exit("Script will now exit")
    else:
        print("You did not pass enough or no arguments.")
        print("Please only pass 1 argument with the directory you wish to be reviewed")
        sys.exit("Script will now exit")


def validate_runs():
    global results_location
    if not os.path.exists(results_location):
        sys.exit("Directory does not exist, exiting script")
    else:
        for (dirpath, subdirs, filenames) in os.walk(results_location):
            for f in filenames:
                if f.endswith(results_file):
                    results_list.append(os.path.join(dirpath, f))

    for r in results_list:
        if 'Check Key Seq Errors             |  *Yes*' in open(r).read():
            testcase = r.replace(results_file, "")
            testcase = testcase[-8:]
            results_to_check.append(testcase)
        elif '2x20 Values Differ               |  *Yes*' in open(r).read():
            testcase = r.replace(results_file, "")
            testcase = testcase[-8:]
            results_to_check.append(testcase)
        elif 'Customer Receipt Values Differ   |  *Yes*' in open(r).read():
            testcase = r.replace(results_file, "")
            testcase = testcase[-8:]
            results_to_check.append(testcase)
        else:
            pass


def review_runs():
    print("             ARTT Runs Require Attention!!!          ")
    print("=========================================================")
    print("It is highly suggested you review the following runs!")
    print("And perform manual comparisons of the files marked *Yes*!")
    print("=========================================================")
    for tc in results_to_check:
        print(tc)


validate_args()
review_runs()
