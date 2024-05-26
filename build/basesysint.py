from progassembly import ProgramAssembly
from vposix import POSIX
from systemlib import SystemLib
from kernel import Kernel
from info import Info
from compatflags import CompatFlags
from basesystem import BaseSystem
if COMPILATION.get_headers('hardware'):
   from hardware import Hardware
from sysflags import Flags
import util

class BaseSystemInterface:
   msg = Info.get_header()
   prefix = "$:"

   class BlankTermInput(Exception):
      pass

   class Commands:
      commands = {'author', 'echo', 'posix_exit', 'help', 'exit_system', 'exit', 'dmesg', 'uptime', 'clear', 'debug_prog', 'setflag', 'enabletraceback'}

      
      if COMPILATION.get_headers('hardware'):
         commands.add("hwservice")
         commands.add("reboot")
         
         class HWService:
            hw_service_list = {"info", "help"}
            if COMPILATION.get_headers('clockmod'):
               hw_service_list.add("freq")

         def reboot(self, input):
            Kernel.reboot()
         def hwservice(self, input):
            input = input.split()[1:]
            cmd = ""
            if len(input) == 0:
               cmd = "help"
            else:
               cmd = input[0]
            if cmd not in self.HWService.hw_service_list:
               cmd = "help"
            if cmd == "help":
               print("Usage: hwservice\n Hardware service for UIX.")
            elif cmd == "info":
               print("Hardware service info:\nCPU Count:{} \nCPU Frequency :{}\n".format(Hardware.cpu_count, Hardware.cpu_freq))
               print("Commands: {}".format(", ".join(self.HWService.hw_service_list)))
            if COMPILATION.get_headers('clockmod'):
               elif cmd == "freq":
                  if len(input) != 2 or not util.isnumeric(input[1]):
                     print("You must specify an integer to set `freq`")
                     return
   
                  print("Requesting update freq to {}".format(input[1]))
                  Hardware.update_freq(int(input[1]))

      def enabletraceback(self, input):
         self.setflag(self=self, input="setflag raise_exception_traceback=1")
   
      def setflag(self, input):
         msg = "setflag: Set a sysflag\nUsage:\n setflag {flag}={value}"
         input = input.split(" ")[1:]
         if len(input) != 1:
            print(msg)
            return
         split_input = input[0].split("=", 1)
         if len(split_input) != 2:
            print(msg)
            return
         if getattr(Flags, split_input[0], None) == None:
            print("The flag `{}` does not exist.".format(split_input[0]))
         setattr(Flags, split_input[0], split_input[1])

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
      def exit(self, input=None):
         self.exit_system(input)
      def exit_system(self, input=None):
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