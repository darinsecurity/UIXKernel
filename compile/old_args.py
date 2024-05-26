class Args:
   target_dist = "rp2",
   package_programs = ['tictactoe.py', 'guessthenumber.py', 'bugged_program.py', 'lineq.py']
   base_libs = {}#{'base64':'base64_micropython.py'}
   libs = ['lwdatetime.py']

   headers = {}#{"hardware", "rp2", "clockmod"}

   target_kernel = 'uixkernel-1.1.py'
   autoinsert_header = "### PACKAGE-BIN // AUTOINSERT ###"
   libar_header = "### LIBRARY // AUTOREPLACE ###"
   endar_header = "### END // AUTOREPLACE ###"

   use_code_compilation=True,
   clean_code_space=True, # Remove comments and spaces
class Output:
   output_file = "uixos-1.1-dev-"+Args.target_dist[0]