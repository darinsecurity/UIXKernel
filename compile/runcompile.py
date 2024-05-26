import logging
import os
import compilelib
from extension import ext, strip_extension
import cleancode

class CompileError(Exception):
   pass

def log(x):
   logging.info(msg=x)
logging.getLogger().setLevel(logging.INFO)

def compile(Args, Output):
   # configre output file
   global_dependencies = []
   
   Output.output_file = strip_extension(Output.output_file, ".py")+".py"
   
   logging.info(f"Compiling target `{Output.output_file}`..")

   logging.info(f"Using provided compilation headers and dist..")
   logging.info(f"headers={', '.join(Args.headers)}")
   logging.info(f"dist={', '.join(Args.target_dist)}")

   
   kernel_lines = []
   with open(os.path.join("build", Args.target_kernel)) as f:
      kernel_lines = f.read().splitlines()

   def prefilter_compilation(kernel_lines):
      return compilelib.prefilter_compilation(kernel_lines, Args.headers, Args.target_dist)


   kernel_lines = prefilter_compilation(kernel_lines)
   
   logging.info(f"Line count: {len(kernel_lines)}")
   logging.info(f"Locating autoinsert header `{Args.autoinsert_header}`")
   autoinsert_header = -1
   libar_header = -1
   endar_header = -1

   for count, line in enumerate(kernel_lines):
      if line.strip() == Args.autoinsert_header:
         logging.info(f"Found autoinsert at line {count}")
         autoinsert_header = count
         continue
      if line.strip() == Args.libar_header:
         logging.info(f"Found libar header at line {count}")
         libar_header = count
         continue
      if line.strip() == Args.endar_header:
         logging.info(f"Found endar header at line {count}")
         endar_header = count
         continue
      if -1 not in [autoinsert_header, libar_header, endar_header]:
         break
         
   if -1 in [autoinsert_header, libar_header, endar_header]:
      raise CompileError("One or more of the headers are missing in the target kernel.")

   logging.info(msg=f"1: Doing kernel lib compilation down to endar_header")

   for line_num in range(0,endar_header+1):
      if kernel_lines[line_num].strip() == Args.endar_header:
         break
      line = kernel_lines[line_num].strip().split(" ")
      if len(line) <= 3:
         continue
      if line[0] != "from" and line[2] != "import":
         continue
      target = line[1]
      target_path = None
      if getattr(Args, "dist_specific_module", None) and Args.dist_specific_module.get(target):
         target = Args.dist_specific_module[target]
         target_path = os.path.join('build', target)
         print(f"Found dist-specific kernel module `{target_path}` override `{line[1]}`")
         if os.path.exists(target_path):
            print(f"Using dist-specific kernel module `{target_path}` override `{line[1]}`")
      else:
         target_path = os.path.join("build", target+".py")

      if os.path.exists(target_path) == False:
         folder_import_path = os.path.join("build", strip_extension(target,".py"), ext(target, ".py"))
         if os.path.exists(folder_import_path):
            target_path = folder_import_path
         
      if os.path.exists(target_path):
         lib_code = ""
         with open(target_path, "r") as f:
            lib_code = f.read()
         if lib_code.strip() == "":
            continue
         kernel_lines[line_num], dependencies = compilelib.strip_imports(prefilter_compilation(lib_code))
         global_dependencies += dependencies
         logging.info(f"Found target for {target} at {target_path}")
      else:
         logging.warning(f"Unknown target {target} at {target_path}.")

   logging.info("2: Specifying base libs")
   index = libar_header-1
   while index < len(kernel_lines):
      index += 1
      line = kernel_lines[index]
      if line.strip() == "### END ###":
         break
      line = kernel_lines[index].strip().split(" ")
      
      if len(line) <= 1:
         continue
      if line[0] != "import":
         continue
      target = line[1]
      base_target = Args.base_libs.get(target)
      if base_target:
         target_path = os.path.join("libs", strip_extension(base_target, ".py")+".py")
         logging.info(f"Specified base target {target_path} for {target}")
         if os.path.exists(target_path):
            lib_code = ""
            with open(target_path, "r") as f:
               lib_code = f.read()
            if lib_code.strip() == "":
               continue
            kernel_lines[index], dependencies = compilelib.strip_imports(prefilter_compilation(lib_code))
            global_dependencies += dependencies
            logging.info(f"Found target for {target} to {base_target} at {target_path}")
      else:
         logging.info(f"Registering global dependency for {target}, since no base target exists in base_libs.")
         global_dependencies.append(target)
         kernel_lines[index] = ""
   global_dependencies_line = ""
   if len(global_dependencies) > 0:
      logging.info(f"Registering global dependencies.. ({len(global_dependencies)})")
      logging.info(f'- {", ".join(global_dependencies)}')
      for dependency in global_dependencies:
         global_dependencies_line += f"import {dependency}\n"

   
   

   result = global_dependencies_line+"\n".join(kernel_lines)

   if getattr(Args, "clean_code_space", None):
      logging.info("Cleaning code space (refactor with ast)..")
      result = cleancode.clean_code(result)

   logging.info(f"Saving result to result/{Output.output_file}")
   path = os.path.join("result", Output.output_file)
   
   with open(path, "w+") as f:
      f.write(result)

   