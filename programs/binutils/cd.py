import os
import sys
args = sys.argv
if len(args) == 1:
    args.append("/")
os.chdir(args[1])