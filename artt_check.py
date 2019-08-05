# Automated Test Tool Check Script
# Author: Jason Miller
# 7/25/2019
# Version 5.0
# Removed ability to run on windows, only for use with AFTER.bat with arguments to python scripts

# !/usr/bin/env python2
# checkartt.py
import os
import sys
import fileinput
import filecmp
import re
import shutil

dateformat = re.compile('..\/..\/.....:....')


def get_test_case():
    argcount = len(sys.argv)
    version = str(sys.version[:1])

    # This function enables the script to loop through test cases or perform check on one test case
    global current_case
    global tcloop
    global arttrun_path
    global customer
    global zipfile
    global current_case_dir
    global current_case

    if os.path.exists("f:/rtm"):
        if not os.path.exists("f:/arttchecks"):
            os.makedirs("f:/arttchecks")
            arttrun_path = "f:/arttchecks/"
        else:
            arttrun_path = "f:/arttchecks/"
    elif not os.path.exists("f:/rtm"):
        os.makedirs(".\\arttchecks")

    if argcount != 3:
        tcloop = 0
        # THIS IS COMMENTED OUT SO THIS WILL NOT WORK ON WINDOWS AT THIS TIME
        # FOR USE WITH 4690 SYSTEM ONLY IN AFTER.BAT
        # if version == '2':
        #     current_case = raw_input("Please type in test case name: ")
        #     current_case = current_case.lower()
        # elif version == '3':
        #     current_case = input("Please type in test case name: ")
        #     current_case = current_case.lower()
        # else:
        #     current_case = input("Please type in test case name: ")
        #     current_case = current_case.lower()
        # print(current_case)
        #
        # if current_case.lower() == 'all':
        #     tcloop = 1
        #     tclist = []
        #     test_case_dirs = os.listdir("C:\\regressn\\cases\\")
        #     for d in test_case_dirs:
        #         d = d.upper()
        #         if d.endswith(".DIR"):
        #             d = d.rstrip(".DIR")
        #             tclist.append(d)
        #         else:
        #             pass
        #     print("Test cases being inspected:")
        #     print(tclist)
        #     for t in tclist:
        #         if not os.path.exists(".\\arttchecks\\" + t):
        #             os.mkdir('.\\arttchecks\\' + t)
        #         current_case = t
        #         checks()
        #         if run_2x20_checks is False:
        #             pass
        #         elif run_cr_valuechecks is False:
        #             pass
        #         elif run_ledger_valuechecks() is False:
        #             pass
        #         elif run_regreport_valuechecks() is False:
        #             pass
        # else:
        #     if not os.path.exists('.\\arttchecks\\' + current_case):
        #         os.mkdir('.\\arttchecks\\' + current_case)
        #     checks()
    elif argcount == 3:  # This is for use with 4690 after.bat
        current_case = sys.argv[2]
        if not os.path.exists(arttrun_path + current_case):
            os.mkdir(arttrun_path + current_case)
            checks()
            run_copy_runlog()

        else:
            checks()
            run_copy_runlog()

    else:
        print("Process ended, nothing processed")

# OLD GET_TEST_CASE FUNCTION
# def get_test_case():
#     version = str(sys.version[:1])
#
#     # This function enables the script to loop through test cases or perform check on one test case
#     global current_case
#     global tcloop
#     tcloop = 0
#     if version == '2':
#         current_case = raw_input("Please type in test case name: ")
#         current_case = current_case.lower()
#     elif version == '3':
#         current_case = input("Please type in test case name: ")
#         current_case = current_case.lower()
#     else:
#         current_case = input("Please type in test case name: ")
#         current_case = current_case.lower()
#     print(current_case)
#
#     if current_case.lower() == 'all':
#         tcloop = 1
#         tclist = []
#         test_case_dirs = os.listdir("C:\\regressn\\cases\\")
#         for d in test_case_dirs:
#             d = d.upper()
#             if d.endswith(".DIR"):
#                 d = d.rstrip(".DIR")
#                 tclist.append(d)
#             else:
#                 pass
#         print("Test cases being inspected:")
#         print(tclist)
#         for t in tclist:
#             if not os.path.exists(".\\arttchecks\\" + t):
#                 os.mkdir('.\\arttchecks\\' + t)
#             current_case = t
#             checks()
#             if run_2x20_checks is False:
#                 pass
#             elif run_cr_valuechecks is False:
#                 pass
#             elif run_ledger_valuechecks() is False:
#                 pass
#             elif run_regreport_valuechecks() is False:
#                 pass
#     else:
#         if not os.path.exists('.\\arttchecks\\' + current_case):
#             os.mkdir('.\\arttchecks\\' + current_case)
#         checks()


def run_2x20_checks():
    # This looks into the 2x20 file for change due values to see if you got change and shouldnt have
    # also looks for check key sequence which means the test case did not run as expected
    if not (os.path.isfile(two_by_twenty_file)):
        return False

    global checkkey
    global changedue
    global itemnotfound
    global negativetrans
    global cfg_nof
    global cfg_negative
    global cfg_changedue

    if "CHECK KEY" in open(two_by_twenty_file).read() or "B003" in open(two_by_twenty_file).read():
        checkkey = 1
    else:
        checkkey = 0

    if "CHANGEDUE" not in open(case_readme).read().upper():
        with open(two_by_twenty_file) as twoby20:
            for line in twoby20:
                if "CHANGE" in line:
                    string = line.split()
                    chngamt = float(string[1])
                    if chngamt > 0.00:
                        changedue = 1
                        break
                    else:
                        changedue = 0
                else:
                    changedue = 0
    elif "CHANGEDUE=0" in open(case_readme).read().upper():
        with open(two_by_twenty_file) as twoby20:
            for line in twoby20:
                if "CHANGE" in line:
                    string = line.split()
                    chngamt = float(string[1])
                    if chngamt > 0.00:
                        changedue = 1
                        break
                    else:
                        changedue = 0
                else:
                    changedue = 0
    elif "CHANGEDUE=1" in open(case_readme).read().upper():
        cfg_changedue = 1
    else:
        changedue = 0

    if "NEGATIVE" not in open(case_readme).read().upper():
        with open(two_by_twenty_file) as twoby20:
            for line in twoby20:
                if "NEGATIVE" in line or "B172" in line:
                    negativetrans = 1
                    break
                else:
                    negativetrans = 0
    elif "NEGATIVE=0" in open(case_readme).read().upper():
        with open(two_by_twenty_file) as twoby20:
            for line in twoby20:
                if "NEGATIVE" in line or "B172" in line:
                    negativetrans = 1
                    break
                else:
                    negativetrans = 0
    elif "NEGATIVE=1" in open(case_readme).read().upper():
        cfg_negative = 1
    else:
        negativetrans = 0

    if "ITEMNOTFOUND" not in open(case_readme).read().upper():
        if "ITEM NOT FOUND" in open(two_by_twenty_file).read() or "B026" in open(two_by_twenty_file).read():
            itemnotfound = 1
        else:
            itemnotfound = 0
    elif "ITEMNOTFOUND=0" in open(case_readme).read().upper():
        if "ITEM NOT FOUND" in open(two_by_twenty_file).read() or "B026" in open(two_by_twenty_file).read():
            itemnotfound = 1
        else:
            itemnotfound = 0
    elif "ITEMNOTFOUND=1" in open(case_readme).read().upper():
        cfg_nof = 1
    elif "ITEMNOTFOUND" not in open(case_readme).read().upper():
        cfg_nof = 3
    else:
        itemnotfound = 0


def run_cr_valuechecks():
    global crvalueerror
    # counter1 = 0  # Counter for Original Line Number from Original File
    # counter2 = 0
    trunvalues = (arttrun_path + test_case + '\\' + test_case + '_cr_this.txt')
    grunvalues = (arttrun_path + test_case + '\\' + test_case + '_cr_gold.txt')

    if not (os.path.isfile(cr_file_this)):
        return False

    # if os.path.isfile(trunvalues):
    #     os.remove(trunvalues)
    # elif os.path.isfile(grunvalues):
    #     os.remove(grunvalues)
    # else:
    open(trunvalues, 'w').close()  # making sure file exists by opening with W and closing
    open(grunvalues, 'w').close()

    # This looks for specific values in customer reciept and outputs to files for comparisons
    for line in fileinput.input(cr_file_this):
        # counter1+= 1  # Incrementing line number from original file
        if "PrintLine: '        TAX" in line:
            with open(trunvalues, 'a') as f:
                # f.write('OriginalLineNo: ' + str(counter1) + ' - ' + line)
                f.write(line)
        elif "PrintLine: '   **** BALANCE" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "PrintLine: '        CASH" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "PrintLine: '        CHANGE" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)

    for line in fileinput.input(cr_file_golden):
        # counter2 += 1  # Incrementing line number from original file
        if "PrintLine: '        TAX" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "PrintLine: '   **** BALANCE" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "PrintLine: '        CASH" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "PrintLine: '        CHANGE" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)

    if filecmp.cmp(grunvalues, trunvalues, shallow=False):
        crvalueerror = 0
    else:
        crvalueerror = 1


def run_2x20_valuechecks():
    global twobyvalueerror
    # counter1 = 0  # Counter for Original Line Number from Original File
    # counter2 = 0
    trunvalues = (arttrun_path + test_case + '\\' + test_case + '_2x20_this.txt')
    grunvalues = (arttrun_path + test_case + '\\' + test_case + '_2x20_gold.txt')

    if not (os.path.isfile(two_by_twenty_file)):
        return False

    # if os.path.isfile(trunvalues):
    #     os.remove(trunvalues)
    # elif os.path.isfile(grunvalues):
    #     os.remove(grunvalues)
    # else:
    open(trunvalues, 'w').close()  # making sure file exists by opening with W and closing
    open(grunvalues, 'w').close()

    # This looks for specific values in 2x20 file and outputs to files for comparisons
    for line in fileinput.input(twoby_file_this):
        # counter1 += 1  # Incrementing line number from original file
        if "==================================================" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "<<<<<< *" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "		TAX DUE" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "		TOTAL" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "		CASH" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "		CHANGE" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)

    for line in fileinput.input(twoby_file_golden):
        # counter2 += 1  # Incrementing line number from original file
        if "==================================================" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "<<<<<< *" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "		TAX DUE" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "		TOTAL" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "		CASH" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "		CHANGE" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)

    if filecmp.cmp(grunvalues, trunvalues, shallow=False):
        twobyvalueerror = 0
    else:
        twobyvalueerror = 1


def run_ledger_valuechecks():
    global ldgrvalueerror
    # counter1 = 0  # Counter for Original Line Number from Original File
    # counter2 = 0
    trunvalues = (arttrun_path + test_case + '\\' + test_case + '_ldgr_this.txt')
    grunvalues = (arttrun_path + test_case + '\\' + test_case + '_ldgr_gold.txt')

    if not (os.path.isfile(ldgr_file_this)):
        return False

    # if os.path.isfile(trunvalues):
    #     os.remove(trunvalues)
    # elif os.path.isfile(grunvalues):
    #     os.remove(grunvalues)
    # else:
    open(trunvalues, 'w').close()  # making sure file exists by opening with W and closing
    open(grunvalues, 'w').close()

    for line in fileinput.input(ldgr_file_this):
        # counter1 += 1  # Incrementing line number from original file
        if "AMT" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "SALES" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "TENDER" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "TOTAL" in line:
            with open(trunvalues, 'a') as f:
                f.write(line)

    for line in fileinput.input(ldgr_file_golden):
        # counter2 += 1  # Incrementing line number from original file
        if "AMT" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "SALES" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "TENDER" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "TOTAL" in line:
            with open(grunvalues, 'a') as f:
                f.write(line)

    if filecmp.cmp(grunvalues, trunvalues, shallow=False):
        ldgrvalueerror = 0
    else:
        ldgrvalueerror = 1


def run_regreport_valuechecks():
    global rgrrptvalueerror
    # counter1 = 0  # Counter for Original Line Number from Original File
    # counter2 = 0
    trunvalues = (arttrun_path + test_case + '\\' + test_case + '_rgrrpt_this.txt')
    grunvalues = (arttrun_path + test_case + '\\' + test_case + '_rgrrpt_gold.txt')

    if not (os.path.isfile(rgr_file_this)):
        return False

    # if os.path.isfile(trunvalues):
    #     os.remove(trunvalues)
    # elif os.path.isfile(grunvalues):
    #     os.remove(grunvalues)
    # else:
    open(trunvalues, 'w').close()  # making sure file exists by opening with W and closing
    open(grunvalues, 'w').close()

    for line in fileinput.input(rgr_file_this):
        # counter1 += 1  # Incrementing line number from original file
        if dateformat.search(line) is not None:
            pass
        elif "RING TIME" in line:
            line = line[:38] + '\n'
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "TENDER TIME" in line:
            line = line[:38] + '\n'
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "OTHER TIME" in line:
            line = line[:38] + '\n'
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "TOTAL TIME" in line:
            line = line[:38] + '\n'
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "POINTS" in line:
            line = line[:40] + '\n'
            with open(trunvalues, 'a') as f:
                f.write(line)
        elif "BONUS" in line:
            line = line[:40] + '\n'
            with open(trunvalues, 'a') as f:
                f.write(line)
        else:
            with open(trunvalues, 'a') as f:
                f.write(line)

    for line in fileinput.input(rgr_file_golden):
        # counter2 += 1  # Incrementing line number from original file
        if dateformat.search(line)is not None:
            pass
        elif "RING TIME" in line:
            line = line[:38] + '\n'
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "TENDER TIME" in line:
            line = line[:38] + '\n'
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "OTHER TIME" in line:
            line = line[:38] + '\n'
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "TOTAL TIME" in line:
            line = line[:38] + '\n'
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "POINTS" in line:
            line = line[:40] + '\n'
            with open(grunvalues, 'a') as f:
                f.write(line)
        elif "BONUS" in line:
            line = line[:40] + '\n'
            with open(grunvalues, 'a') as f:
                f.write(line)
        else:
            with open(grunvalues, 'a') as f:
                f.write(line)

    if filecmp.cmp(trunvalues, grunvalues, shallow=False):
        rgrrptvalueerror = 0
    else:
        rgrrptvalueerror = 1


def run_cop_checks():
    # This checks the copient log file for errors or if it exists
    global coperror
    global cfg_copient
    # print("Processing Copient Log for test case " + test_case.upper())
    if os.path.exists(cop_log_file):
        if "ERROR" in open(cop_log_file) or "Error" in open(cop_log_file) or "error" in open(cop_log_file):
            coperror = 1
        else:
            coperror = 0
    else:
        cfg_copient = 0


def run_copy_runlog():
    # Looking for run.log in the current case logs directory
    if os.path.exists(case_runlog):
        shutil.copyfile(case_runlog, results_base_dir + '\\run.txt')


def arttcheckreport():
    # We print the on screen report here for user to get a preliminary results screen
    # stdout is printed to _result.txt file
    print("       ARTT Check Report                  ")
    print("              " + test_case.upper())
    print("====================================================")
    print("| Data Being Checked               |     Result    |")
    print("| ---------------------------------|-------------- |")

    if cfg_changedue == 1:
        print("| Change Due                       |   Configured  |")
    elif cfg_changedue == 3:
        print("| Change Due                       |   *No Cfg*    |")
    elif changedue == 0:
        print("| Change Due                       |   No          |")
    elif changedue == 1:
        print("| Change Due                       |  *Yes*        |")
    else:
        print("| Change Due                       |   Unknown     |")

    if cfg_negative == 1:
        print("| Negative Trans                   |   Configured  |")
    elif cfg_negative == 3:
        print("| Negative Trans                   |   *No Cfg*    |")
    elif negativetrans == 0:
        print("| Negative Trans                   |   No          |")
    elif negativetrans == 1:
        print("| Negative Trans                   |  *Yes*        |")
    else:
        print("| Negative Trans                   |   Unknown     |")

    if checkkey == 1:
        print("| Check Key Seq Errors             |  *Yes*        |")
    elif checkkey == 0:
        print("| Check Key Seq Errors             |   No          |")
    else:
        print("| Check Key Seq Errors             |   Unknown     |")

    if cfg_nof == 1:
        print("| Items Not Found                  |   Configured  |")
    elif cfg_nof == 3:
        print("| Items Not Found                  |   *No Cfg*    |")
    elif itemnotfound == 0:
        print("| Items Not Found                  |   No          |")
    elif itemnotfound == 1:
        print("| Items Not Found                  |  *Yes*        |")
    else:
        print("| Items Not Found                  |   Unknown     |")

    if coperror == 1:
        print("| Copient Errors                   |  *Yes*        |")
    elif coperror == 0:
        print("| Copient Errors                   |   No          |")
    elif cfg_copient == 0:
        print("| Copient Errors                   |   No Log      |")
    else:
        print("| Copient Errors                   |   Unknown     |")

    if crvalueerror == 0:
        print("| Customer Receipt Values Differ   |   No          |")
    elif crvalueerror == 1:
        print("| Customer Receipt Values Differ   |  *Yes*        |")
    else:
        print("| Customer Receipt Vales Differ    |   Unknown     |")

    if twobyvalueerror == 0:
        print("| 2x20 Values Differ               |   No          |")
    elif twobyvalueerror == 1:
        print("| 2x20 Values Differ               |  *Yes*        |")
    else:
        print("| 2x20 Values Differ               |   Unknown     |")

    if ldgrvalueerror == 0:
        print("| Ledger Report Values Differ      |   No          |")
    elif ldgrvalueerror == 1:
        print("| Ledger Report Values Differ      |  *Yes*        |")
    else:
        print("| Ledger Report Values Differ      |   Unknown     |")

    if rgrrptvalueerror == 0:
        print("| Register Report Values Differ    |   No          |")
    elif rgrrptvalueerror == 1:
        print("| Register Report  Values Differ   |  *Yes*        |")
    else:
        print("| Register Report  Values Differ   |   Unknown     |")

    print("----------------------------------------------------")
    print("")
    

def checks():
    global test_case_dir
    global test_case_golden
    global test_case_root
    global case_readme
    global case_errortxt
    global case_saverun
    global two_by_twenty_file
    global cop_log_file
    global cr_file_this
    global cr_file_golden
    global twoby_file_this
    global twoby_file_golden
    global ldgr_file_this
    global ldgr_file_golden
    global rgr_file_this
    global rgr_file_golden
    global changedue
    global checkkey
    global coperror
    global casesuccess
    global itemnotfound
    global negativetrans
    global cfg_nof
    global cfg_negative
    global cfg_changedue
    global cfg_copient
    global twobyvalueerror
    global crvalueerror
    global ldgrvalueerror
    global rgrrptvalueerror
    global tlogvalueerror
    global test_case
    global cr_file_this
    global ldgr_file_this
    global rgr_file_this
    global case_runlog
    global results_base_dir

    # Directory variables and File variables
    test_case_dir = ("C:\\regressn\\cases\\" + current_case + ".DIR" + "\\THIS.RUN\\")
    test_case_golden = ("C:\\regressn\\cases\\" + current_case + ".DIR" + "\\GOLDEN.RUN\\")
    test_case_root = ("C:\\regressn\\cases\\" + current_case + ".DIR")
    test_case = current_case

    # Extra case files for results
    case_readme = (test_case_root + "\\" + current_case + ".RME")
    case_errortxt = (test_case_root + "\\LOGS\\ERROR.TXT")
    case_saverun = (test_case_root + "\\LOGS\\SAVE.RUN")
    case_runlog = (test_case_root + "\\LOGS\\RUN.LOG")

    # Files for use with negative, change due, key sequence checks
    two_by_twenty_file = (test_case_dir + "2x20.001")
    cop_log_file = (test_case_dir + "CP2.001")

    # Files for use with value comparisons
    cr_file_this = (test_case_dir + "CR.001")
    cr_file_golden = (test_case_golden + "CR.001")
    twoby_file_this = (test_case_dir + "2x20.001")
    twoby_file_golden = (test_case_golden + "2x20.001")
    ldgr_file_this = (test_case_dir + "LEDGER.OUT")
    ldgr_file_golden = (test_case_golden + "LEDGER.OUT")
    rgr_file_this = (test_case_dir + "RGRRPRT.RPT")
    rgr_file_golden = (test_case_golden + "RGRRPRT.RPT")

    # Initializing Variables
    changedue = -1
    checkkey = -1
    coperror = -1
    casesuccess = -1
    itemnotfound = -1
    negativetrans = -1
    cfg_nof = -1
    cfg_negative = -1
    cfg_changedue = -1
    cfg_copient = -1
    twobyvalueerror = -1
    crvalueerror = -1
    ldgrvalueerror = -1
    rgrrptvalueerror = -1
    tlogvalueerror = -1

    # test_case_check()

    results_file = (arttrun_path + current_case + '\\' + current_case + '_results.txt')
    results_base_dir = (arttrun_path + current_case)
    sys.stdout = open(arttrun_path + current_case + '\\' + current_case + '_results.txt', "w")

    # Peform checks on data
    run_2x20_checks()
    run_cop_checks()
    run_cr_valuechecks()
    run_2x20_valuechecks()
    run_ledger_valuechecks()
    run_regreport_valuechecks()
    run_copy_runlog()
    arttcheckreport()


get_test_case()
