class Args:
   target_dist="default",
   package_programs = ['tictactoe.py', 'guessthenumber.py', 'lineq.py', 'ls.py', 'pycoremark.py', "binutils/cd.py", "binutils/ls.py", "binutils/cat.py"]
   libs = ['lwdatetime.py']
   version="1.1.1",
   target_kernel = 'uixkernel-1.1.py'
   autoinsert_header = "### PACKAGE-BIN // AUTOINSERT ###"
   libar_header = "### LIBRARY // AUTOREPLACE ###"
   endar_header = "### END // AUTOREPLACE ###"

   use_code_compilation=True,
   clean_code_space=True,
   clean_code_dependencies=True, # clean the code of programs and libraries? 
class Output:
   output_file = "" #auto generated