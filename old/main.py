      class BaseSystem:
         version = 1
         subversion = 0
         name = "UIXKernel"
         prefix = "uix"
         default_program = "bsi"
         vposix = "VPOSIX/1.0"
         subsystem = "Python"
         author = "Darin Tanner"
      ## INCLUDE // BASE-HEADER ##
      class ProgramAssembly:
         programs = {}
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
            commands = ['author', 'echo', 'posix_exit', 'help', 'exit_system']
            def exit_system(self):
               POSIX.exit_system()
            def author(self):
               print(BaseSystem.author)
            def echo(self, input):
               print(input[5:])
            def posix_exit(self):
               POSIX.exit_program()
            def help(self, input):
               print(f"{BaseSystem.name}: Available commands")
               print(", ".join(self.commands))
               print()

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
            POSIX.clear_term()
            print(self.msg)
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
                     determine_args = 2
                     try:
                        determine_args = command_method.__code__.co_argcount
                     except Exception as e:
                        pass
                     if determine_args == 1:
                        command_method(self.Commands)
                     else:
                        command_method(self.Commands, user_input)
                  elif is_packaged_program:
                     return command, command
                  else:
                     print(f"{BaseSystem.prefix}: unknown command `{command}`")
               except self.BlankTermInput:
                  # pass
                  pass

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

      def print_header():
         print(f"Running {BaseSystem.name} {BaseSystem.version}.{BaseSystem.subversion} {BaseSystem.vposix} in {BaseSystem.subsystem} Subsystem")

      print_header()
      print("Checking if this system has `exec` capabilities..")
      if test_exec('') == False:
         print("`exec` required for system! Fail!")
         call_exit()
      check_lib = ['os', 'sys', 'math', 'time', 'random', 'signal', 'threading', 'cmath', 'ast', 'zlib']
      for lib in check_lib:
         print("Checking if `" + lib + '` is available.. ', end="")
         success, error = SystemLib.import_lib(lib)
         if success:
            print("OK")
         else:
            print("FALSE")
      print("Supported libraries: " + ", ".join(SystemLib.get_supported()))
      print("Starting VPOSIX runtime..")
      print("Capturing state..")
      POSIX.Interpreter.capture_variable()
      print("Starting loop..\n")
      while True:
         try:
            POSIX.ProgramState.set_default_interface()
            exec_name, exec_program = BaseSystemInterface.run()
            # execute program
            exec(ProgramAssembly.programs[exec_name])

         except KeyboardInterrupt:
            print("\nExiting system..")
            call_exit()
         except POSIX.Interrupts.ProgramExit:
            active_program = POSIX.ProgramState.active_program
            if active_program == "bsi":
               print("Received POSIX exit program signal from Base System Interface. This is not supported. Restarting interpreter..")
            POSIX.Interpreter.restore_variable()
         except POSIX.SystemInterrupts.ExitSystem:
            # exit the system
            call_exit()