import builtins # one of the only dependencies of UIX OS
from basesystem import BaseSystem
from util import util
from simpledec import SimpleDEC
if COMPILATION.get_headers('hardware'):
   from hardware import Hardware

if COMPILATION.get_headers('interrupts'):
   from interrupts import Interrupts
   
from libassembly import LibraryAssembly
from progassembly import ProgramAssembly
from sysflags import Flags
from systemlib import SystemLib
from kernel import Kernel

if COMPILATION.get_headers('hardware'):
   Hardware.init()

# configure importlib
SystemLib._original_import_method = builtins.__import__
builtins.__import__ = SystemLib._import_lib_h
if COMPILATION.match_headers('nspire', 'rp2'):
   from overridesys import OverrideSys
   sys_lib = None
   success, error = SystemLib.import_host_lib('sys')
   if success:
      sys_lib = SystemLib._import_lib_h('sys')
   sys_module = OverrideSys(sys_lib, [])
   SystemLib.override_imports['sys'] = sys_module
   
if COMPILATION.get_headers('filesystem'):
   if COMPILATION.get_headers('simulatedfs'):
      from simulatedfs import simulatedfs
      SystemLib.supported_libraries['os'] = True
   from fsdriver import FSDriver
   if COMPILATION.get_headers('simulatedfs'):
      os = VirtualOSModule(vfs=FSDriver.vfs)
      SystemLib.override_imports['os'] = os
      if globals().get("__builtins__", None) is None:
         globals()['__builtins__'] = builtins
      __builtins__.open = os.open
      __builtins__.__import__ = SystemLib._import_lib_h
   
   from journalfs import FileSystem
   
   
from info import Info
from unixlog import log
from compatunits import CompatibilityUnits
from compatflags import CompatFlags
from basesysint import BaseSystemInterface
from vposix import POSIX
if COMPILATION.get_headers('taskscheduler'):
   from taskscheduler import TaskScheduler
import COMPILATION
### END // AUTOREPLACE ###
### LIBRARY // AUTOREPLACE ###
import base64
### END ###
### PACKAGE-BIN // AUTOINSERT ###
def call_exit():
   Kernel.exit()

def test_exec(code):
   try:
      exec(code)
      return True
   except Exception:
      return False

insignia = "###########\n###### ####\n###### ####\n#####  ####\n#      ####\n###     ###\n####      #\n####  #####\n#### ######\n#### ######\n###########"
def print_insignia():
   for line in insignia.split("\n"):
      lookup = {"#": "#="}
      msg = ""
      for char in line:
         char = lookup.get(char, char*2)
         msg += char 
      print(msg)
print_insignia()
   
log("\n"+Info.get_header())
log("Checking if this system has `exec` capabilities..")
if test_exec('') == False:
   log("`exec` required for system! Fail!")
   call_exit()
   
log("Decoding libraries.. ")
for library_name, library in LibraryAssembly.libraries.items():
   custom_globals = {}
   library_code = library #+ "{} = {}\n".format(library_name, library_name)
   # the class is now defined in custom globals
   exec(library_code, custom_globals)
   if custom_globals.get(library_name, False):
      LibraryAssembly.library_namespace[library_name] = custom_globals[library_name]
      LibraryAssembly.libraries[library_name] = True
      SystemLib.supported_libraries[library_name] = True
   else:
      del LibraryAssembly.libraries[library_name]
      
log("Decoding programs..")
for program_name, program in ProgramAssembly.programs.items():
   ProgramAssembly.programs[program_name] = program

def run_lib_check():
   check_lib = ['os', 'sys', 'math', 'time', 'random', 'signal', 'threading', 'cmath', 'ast', 'zlib', 'traceback', 'gc']
   for lib in check_lib:
      log("Checking if `" + lib + '` is available.. ', end="")
      success, error = SystemLib.import_host_lib(lib)
      if success:
         log("OK")
      else:
         log("FALSE")
   log("Supported libraries: " + ", ".join(SystemLib.get_supported()))
run_lib_check()

log("Starting VPOSIX runtime..")
checks = CompatibilityUnits.get_all_checks()
if len(checks) > 0:
   log("Using compatibility checks compiled for: " + ', '.join(checks))
   for check in checks:
      code = CompatibilityUnits.get_code_check(check)
      custom_locals = {"modified":False}
      if not code:
         continue
      exec(code, globals(), custom_locals)
      if custom_locals["modified"]:
         print("Modification occured.")
      print("Attempted check `{}` (stat: {})".format(check, custom_locals['modified']))
del checks
patches = CompatibilityUnits.get_all_patches()
if len(patches) > 0:
   log("Applying compatibility patches in sequential order: " + ', '.join(patches))
   for patch in patches:
      code = CompatibilityUnits.get_code_patch(patch)
      custom_locals = {}
      exec(code, globals(), custom_locals)
del patches
# mark system started
if SystemLib.supports_lib("time"):
   import time
   if hasattr(time, 'time'):
      Kernel.timestamp_started = time.time()

if COMPILATION.get_headers("networking"):
   log("Networking enabled! ")

if COMPILATION.get_headers("freemem"):
   if SystemLib.supports_lib('gc'):
      import gc
      log("Freeing memory: ")
      CompatibilityUnits.checks_code.clear()
      CompatibilityUnits.checks_patches.clear()
      del insignia, run_lib_check, print_insignia
      gc.collect()
      if COMPILATION.get_headers("rp2"):
         log(f"  Bytes free: {gc.mem_free()}") #micropython only
   else:
      log("No garbage collector library, can not free memory")
   
if COMPILATION.get_headers("filesystem"):
   log("Filesystem enabled!")
   FileSystem.init()

if COMPILATION.get_headers("taskscheduler"):
   Kernel.log("Using single threaded task scheduler.")
   task_scheduler = TaskScheduler()

log("Capturing state..")
clear_terminal = False
POSIX.Interpreter.capture_variable()
log("Starting loop..\n")

BaseSystemInterface.display_init_msg()
while True:
   try:
      POSIX.ProgramState.set_default_interface()
      # if clear_terminal:
      #    POSIX.clear_term()

      exec_name, exec_program, exec_args = BaseSystemInterface.run()
      # when exit out of BSI, execute corresponding program.

      # execute program
      # set program state
      POSIX.ProgramState.alter_interface(exec_name)

      sys = __import__('sys')
  
      # if COMPILATION.get_headers('nspire'):
      #    use_setattr = False
      # if use_setattr:
      try:
         setattr(sys, "argv", exec_args)
      except AttributeError:
         sys.argv = exec_args
      # else:
      #    sys.argv = exec_args # quite crude but works on the calculator
      # program_locals = {}
      #program_globals = {'os':os, 'sys': sys}
      
      exec(ProgramAssembly.programs[exec_name])#, program_locals, program_globals)

   except KeyboardInterrupt:
      active_program = POSIX.ProgramState.active_program
      if active_program == "bsi":
         print("\nExiting system..")
         call_exit()
      else:
         print("\nExiting program..")
         POSIX.Interpreter.restore_variable()

   except POSIX.Interrupts.ProgramExit:
      active_program = POSIX.ProgramState.active_program
      if active_program == "bsi":
         print("Received POSIX exit program signal from Base System Interface. This is not supported. Restarting interpreter..")
      POSIX.Interpreter.restore_variable()
   except POSIX.SystemInterrupts.ExitSystem:
      # exit the system
      call_exit()
   except Exception as e:
      active_program = POSIX.ProgramState.active_program
      is_running_program = True

      if active_program == "bsi":
         is_running_program = False

      if is_running_program or True: # show all errors
         print("\n" + "-"*20)
         print("{}: Error. Program `{}` encountered an exception while running, and must exit. ".format(BaseSystem.prefix,active_program))
         print("Exception: {}".format(type(e).__name__))
         if SystemLib.supports_lib('traceback'):
            import traceback
            traceback.print_exc()
         else:
            if str(Flags.raise_exception_traceback) == "1":
               raise e
            else:
               print("No traceback available on this system.")
         clear_terminal = False
         print("-"*20)
         POSIX.Interpreter.restore_variable()
         continue

   clear_terminal = True
