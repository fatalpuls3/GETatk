# ARTT RTM Case Trigger File Generator
# Author: Jason Miller
# Date: 7/27/2019
# Version 1.0
# Description: This script will read in the cases.log file and generate 
# trigger files for RTM to be able to run the test cases

cfile = '.\cases.log'

with open(cfile, 'r') as f:
	for line in f:
		line = line.rstrip()
		with open(line, 'w') as a:
			a.write(line + "\n")
