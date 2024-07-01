import os
import sys
import COMPILATION

specify_arg = ""
if len(sys.argv) == 2:
   specify_arg = sys.argv[1]

use_dir_func = False
if COMPILATION.match_headers("rp2"):
   use_dir_func = True
if use_dir_func == False:
   print("  ".join(os.listdir(os.path.join(os.getcwd(), specify_arg))))
else:
   print("  ".join(os.listdir(os.getcwd()+ specify_arg)))