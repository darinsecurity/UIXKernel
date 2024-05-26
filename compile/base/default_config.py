class Args:
   target_dist="default",
   package_programs = ['tictactoe.py', 'guessthenumber.py', 'bugged_program.py', 'lineq.py']
   libs = ['lwdatetime.py']
   version="1.1",
   target_kernel = 'uixkernel-1.1.py'
   autoinsert_header = "### PACKAGE-BIN // AUTOINSERT ###"
   libar_header = "### LIBRARY // AUTOREPLACE ###"
   endar_header = "### END // AUTOREPLACE ###"

   use_code_compilation=True,
   clean_code_space=True,
class Output:
   output_file = "" #auto generated