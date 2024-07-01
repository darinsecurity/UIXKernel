class BaseSystem:
   version = 1
   subversion = 0
   name = "UIXKernel"
   prefix = "uix"
   default_program = "bsi"
   vposix = "VPOSIX/1.0"
   subsystem = "Python"
   author = "Darin Tanner"
class CompatibilityUnits:
   checks_code = {}
   checks_patches = {}

   @classmethod
   def get_code_patch(self, check):
      return base64.b64decode(self.checks_patches[check])
   
   @classmethod
   def get_code_check(self, check):
      return base64.b64decode(self.checks_code[check])
      
   @classmethod
   def get_all_checks(self):
      l = []
      for k, v in self.checks_code.items():
         l.append(k)
      return l

   @classmethod
   def get_all_patches(self):
      l = []
      for k, v in self.checks_patches.items():
         l.append(k)
      return l
class CompatFlags:
   system_type="linux/unix"
class LibraryAssembly:
   libraries = {}
   included = {}

   # to not be touched by computer generated code
   library_namespace = {}
## INCLUDE // BASE-HEADER ##
class ProgramAssembly:
   programs = {}
   program_count = 0
   use_base64 = True
   
   @classmethod
   def get_all_programs(self):
      l = []
      for k, v in self.programs.items():
         l.append(k)
      return l
class Flags:
   show_dmesg_output = True
# Computer generated comments, do not modify
## AUTOINSERT // START ##
class SystemLib:
   supported_libraries = {}
   def get_supported():
      l = []
      for k, v in SystemLib.supported_libraries.items():
         if v == True:
            l.append(k)
      return l
   def resolve_lib(name):
      if LibraryAssembly.library_namespace[name]:
         return LibraryAssembly.library_namespace[name]
      custom_globals = {}
      exec("import " + name, custom_globals)
      return custom_globals[name]
   def supports_lib(name):
      return name in SystemLib.supported_libraries
   def import_lib(name, add_supported=True):
      try:
         exec("import " + str(name))
         if add_supported:
            SystemLib.supported_libraries[name] = True
         return True, None
      except ImportError as e:
         return False, e
      except Exception as e:
         return False, e
class BaseSystemInterface:
   msg = "Base System Interface"
   prefix = "$:"

   class BlankTermInput(Exception):
      pass
      
   class Commands:
      commands = ['author', 'echo', 'posix_exit', 'help', 'exit_system', 'dmesg', 'uptime', 'clear', 'debug_prog']

      def debug_prog(self, input):
         print(ProgramAssembly.programs)
         
      def clear(self, input):
         POSIX.clear_term()
      
      def uptime(self, input):
         if not SystemLib.supports_lib('time'):
            print("This system does not include the `time` library, no time support.")
            return
         if not SystemLib.supports_lib('lwdatetime'):
            print("Please compile UIXKernel with the included `lwdatetime` library for datetime support.")
            return
         import time
         if hasattr(time, 'time') == False:
            print("Time function lacks .time() property, can not capture time.")
            return
         lwdatetime = SystemLib.resolve_lib('lwdatetime')
         cur_time = time.time()
         print(lwdatetime.get_time_difference(cur_time, Kernel.timestamp_started, ['days','hours', 'minutes','seconds']))
      
      def dmesg(self, input):
         for log in Kernel.logs:
            print(log[0], end=log[1])
      def exit_system(self, input):
         POSIX.exit_system()
      def author(self, input):
         print(BaseSystem.author)
      def echo(self, input):
         print(input[5:])
      def posix_exit(self, input):
         POSIX.exit_program()
      def help(self, input):
         print("{}: Available commands".format(BaseSystem.name))
         print(", ".join(self.commands))
         print()
         print("Available programs")
         print(", ".join(ProgramAssembly.get_all_programs()))

   @classmethod
   def get_command(self, name):
      if name in self.Commands.commands:
         func = getattr(self.Commands, name, None)
         if func == None:
            return False
         return func
      else:
         return False
      
   @classmethod
   def run(self):
      print(self.msg + " on " + str(CompatFlags.system_type))

      suffix_word = ""
      if ProgramAssembly.program_count != 1:
         suffix_word = "s"
      print("{} program{} on system.".format(ProgramAssembly.program_count, suffix_word))
      print("Type `help` for help.")
      while True:
         try:
            user_input = input(self.prefix + " ")
   
            args = user_input.split(" ")
            if args == ['']:
               raise self.BlankTermInput
            command = args[0]
            command_method = self.get_command(command)
            
            is_packaged_program = command in ProgramAssembly.programs
            
            if command_method:
               command_method(self.Commands, user_input)
               # determine_args = 2
               # try:
               #    determine_args = command_method.__code__.co_argcount
               # except Exception as e:
               #    pass
               # if determine_args == 1:
               #    command_method(self.Commands)
               # else:
               #    command_method(self.Commands, user_input)
            elif is_packaged_program:
               return command, command
            else:
               print("{}: unknown command or program `{}`".format(BaseSystem.prefix, command))
         except self.BlankTermInput:
            # pass
            pass
class Kernel:
   logs = []
   timestamp_started = -1.0

   @classmethod
   def log(self, x, end="\n", store=True):
      print(x, end=end)
      if store:
         self.logs.append([x,end])
class POSIX:
   class Interpreter:
      variable = []
      @classmethod
      def get_variable(self):
         return set(globals().keys())

      @classmethod
      def capture_variable(self):
         self.variable = self.get_variable()

      @classmethod
      def restore_variable(self):
         new_vars = self.get_variable()
         added_vars = new_vars - self.variable
         for var in added_vars:
             del globals()[var]
   class RunState:
      pass
   class ProgramState:
      active_program = BaseSystem.default_program

      @classmethod
      def set_default_interface(self):
         self.active_program = BaseSystem.default_program

      @classmethod
      def alter_interface(self, name):
         self.active_program = name
   class Interrupts:
      class ProgramExit(Exception):
         pass
      class PrivilegeRequired(Exception):
         pass
   class SystemInterrupts:
      class ExitSystem(Exception):
         pass
      
   def clear_term():
      print("\033c", end="")

   @classmethod
   def exit_system(self):
      if self.ProgramState.active_program == 'bsi':
         raise self.SystemInterrupts.ExitSystem
      else:
         raise self.Interrupts.PrivilegeRequired('Require permissions for exit_system')
   
   @classmethod
   def exit_program(self):
      raise self.Interrupts.ProgramExit
def call_exit():
   exit()

def test_exec(code):
   try:
      exec(code)
      return True
   except Exception:
      return False

def log(x, end="\n", store=True):
   Kernel.log(x, end, store)
   
def print_header():
   log("Running " + BaseSystem.name + " " + str(BaseSystem.version) + "." + str(BaseSystem.subversion) + " " + BaseSystem.vposix + " in " + BaseSystem.subsystem + " Subsystem")

print_header()
log("Decoding libraries..")
for library_name, library in LibraryAssembly.libraries.items():
   custom_globals = {}
   library_code = base64.b64decode(library) + "\n{} = {}".format(library_name, library_name).encode()
   # the class is now defined in custom globals
   exec(library_code, custom_globals)
   if custom_globals[library_name]:
      LibraryAssembly.library_namespace[library_name] = custom_globals[library_name]
      LibraryAssembly.libraries[library_name] = True
      SystemLib.supported_libraries[library_name] = True
   else:
      del LibraryAssembly.libraries[library_name]
      
log("Decoding programs..")
for program_name, program in ProgramAssembly.programs.items():
   ProgramAssembly.programs[program_name] = base64.b64decode(program)

log("Checking if this system has `exec` capabilities..")
if test_exec('') == False:
   log("`exec` required for system! Fail!")
   call_exit()
check_lib = ['os', 'sys', 'math', 'time', 'random', 'signal', 'threading', 'cmath', 'ast', 'zlib', 'traceback']
for lib in check_lib:
   log("Checking if `" + lib + '` is available.. ', end="")
   success, error = SystemLib.import_lib(lib)
   if success:
      log("OK")
   else:
      log("FALSE")
log("Supported libraries: " + ", ".join(SystemLib.get_supported()))

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

# mark system started
if SystemLib.supports_lib("time"):
   import time
   if hasattr(time, 'time'):
      Kernel.timestamp_started = time.time()

log("Capturing state..")
clear_terminal = False
POSIX.Interpreter.capture_variable()
log("Starting loop..\n")
while True:
   try:
      POSIX.ProgramState.set_default_interface()
      if clear_terminal:
         POSIX.clear_term()
      
      exec_name, exec_program = BaseSystemInterface.run()
      # when exit out of BSI, execute corresponding program.
      
      # execute program
      # set program state
      POSIX.ProgramState.alter_interface(exec_name)
      exec(ProgramAssembly.programs[exec_name])
      
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
            print("No traceback available on this system.")
         clear_terminal = False
         print("-"*20)
         POSIX.Interpreter.restore_variable()
         continue

   clear_terminal = True
