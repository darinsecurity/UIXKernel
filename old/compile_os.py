import os
import pinliner
import base64


# pi pico
class Args:
   programs = ['tictactoe.py', 'guessthenumber.py', 'bugged_program.py', 'lineq.py']
   init_libraries = [{'base64.py':'base64_micropython.py'}]
   libraries = [{'base64.py':'base64_compat.py'}, 'lwdatetime.py']
   use_kernel = 'uixkernel1.py'
   kernel_header = "## AUTOINSERT // START ##"
   library_header = "## INCLUDE // BASE-HEADER ##"
   embed_base64 = True,
   compatibility_dist=[]
   compatibility_patches=[]
   output = 'uixos1-pico.py'
   
# the ti-inspire
# class Args:
#    programs = ['tictactoe.py', 'guessthenumber.py', 'bugged_program.py', 'lineq.py']
#    init_libraries = [{'base64.py':'base64_compat.py'}]
#    libraries = [{'base64.py':'base64_compat.py'}, 'lwdatetime.py']
#    use_kernel = 'uixkernel1.py'
#    kernel_header = "## AUTOINSERT // START ##"
#    library_header = "## INCLUDE // BASE-HEADER ##"
#    embed_base64 = True,
#    compatibility_dist=['ti_nspire']
#    compatibility_patches=[]
#    output = 'uixos1-nspire.py'

print("Compiling UIXKernel with programs..")

kernel = ""
with open(Args.use_kernel, 'r') as f:
   kernel = f.read()
kernel = kernel.splitlines()

kernel_header_line = 0
library_header_line = 0

for line_num, line in enumerate(kernel):
   if line.strip() == Args.kernel_header:
      kernel_header_line = line_num
      print("Found kernel header line at " + str(line_num))
   elif line.strip() == Args.library_header:
      library_header_line = line_num
      print("Found library header line at " + str(line_num))
      
def get_name(filepath):
   return filepath.split(".py")[0]

## INCLUDE // BASE-HEADER ##
base_h_lines = []
## AUTOINSERT // START ##
alter_lines = []

print("Packaging libraries..")

print("Packaging initial libraries first.. (no base64 encoding)")
for library_obj in Args.init_libraries:
   library_path = ""
   library = ""
   if isinstance(library_obj, dict):
      library = list(library_obj)[0]
      library_path = library_obj[library]
   else:
      library = library_obj
      library_path = library_obj  
   
   print(f"Packaging initial library `{library}`")
   library_code = ""
   with open(os.path.join('libs',library_path), 'r') as f:
      library_code = f.read()
   # do not employ encoding
   base_h_lines.append(library_code)
   alter_lines.append(f'LibraryAssembly.included["{get_name(library)}"] = True')
print("Packaging libraries with base64 encoding..")
for library_obj in Args.libraries:
   library_path = ""
   library = ""
   if isinstance(library_obj, dict):
      library = list(library_obj)[0]
      library_path = library_obj[library]
   else:
      library = library_obj
      library_path = library_obj   
      
   if library in Args.init_libraries:
      continue
   print(f"Packaging library `{library}`")
   library_code = ""
   with open(os.path.join('libs',library), 'r') as f:
      library_code = f.read()
   # now use encoding
   base_h_lines.append(f'LibraryAssembly.libraries["{get_name(library)}"] = """{base64.b64encode(library_code.encode()).decode()}"""')
   alter_lines.append(f'LibraryAssembly.included["{get_name(library)}"] = True')

# for library in Args.libraries:
#    library_code = ""
#    with open(os.path.join('libs',library), 'r') as f:
#       library_code = f.read()
#    library_code = library_code

print("Packaging programs..")
for program in Args.programs:
   print(f"Packaging program `{program}` with base64 encoding")
   program_code = ""
   with open(os.path.join('programs',program), 'r') as f:
      program_code = f.read()
   alter_lines.append(f'ProgramAssembly.programs["{get_name(program)}"] = """{base64.b64encode(program_code.encode()).decode()}"""')

program_count = len(Args.programs)
print(f"Program count: {program_count}")
alter_lines.append(f'ProgramAssembly.program_count = {program_count}')


if len(Args.compatibility_dist) > 0:
   print("Implementing compatibility checks:")
   print(f"+ {', '.join(Args.compatibility_dist)}")
   for check in Args.compatibility_dist:
      check_code = ""
      with open(os.path.join('compat_dist',get_name(check)+".py"), 'r') as f:
         check_code = f.read()
      alter_lines.append(f'CompatibilityUnits.checks_code["{get_name(check)}"] = """{base64.b64encode(check_code.encode()).decode()}"""')

if len(Args.compatibility_patches) > 0:
   print("Implementing compatibility patches:")
   print(f"+ {', '.join(Args.compatibility_patches)}")
   for patch in Args.compatibility_patches:
      patch_code = ""
      with open(os.path.join('compat_patch',get_name(patch)+".py"), 'r') as f:
         patch_code = f.read()
      alter_lines.append(f'CompatibilityUnits.checks_patches["{get_name(patch)}"] = """{base64.b64encode(patch_code.encode()).decode()}"""')



print("Inserting into ProgramAssembly..")

kernel[kernel_header_line] = "\n".join(alter_lines)

print("Inserting into Base Header..")
kernel[library_header_line] = "\n".join(base_h_lines)

print(f"Writing into {Args.output}...")
with open(Args.output, 'w+') as f:
   f.write("\n".join(kernel))
