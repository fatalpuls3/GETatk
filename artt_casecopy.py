# Automated Test Tool Case Copy Script
# Author: Jason Miller
# 7/30/2019
# Version 1.0

import os, shutil, sys

root_dst_dir = 'c:/REGRESSN/CASES/'
argcount = len(sys.argv)

if argcount != 2:
    print('Source directory for ARTT test cases not specified')
    print('Example: e:/000/rtmzips/ahold')
    print('Re-run script passing source directory of test cases')
    sys.exit(2)
else:
    root_src_dir = sys.argv[1]
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        print(dst_dir)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)

