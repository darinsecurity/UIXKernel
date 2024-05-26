# Virtual interrupt class
# For interface purposes only

class Interrupts:
   interrupts_table = {}

   @classmethod
   def retrieve_interrupt(self, id):
      pass
      
   @classmethod
   def assign_interrupt(self, func, run_every, is_periodic, id):
      pass

   @classmethod
   def destroy_interrupt(self, id):
      pass