from basesystem import BaseSystem

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