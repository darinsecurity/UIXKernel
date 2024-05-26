##add_dependencies=threading
# Windows / UNIX multithreading
import threading
class Interrupts:
   Timer = threading.Timer
   interrupts_table = {}

   class RepeatTimer(Timer):
       def run(self):
           while not self.finished.wait(self.interval):
               self.function(*self.args, **self.kwargs)
           del self

   @classmethod
   def retrieve_interrupt(self, id):
      return self.interrupts_table.get(id, None)
   
   @classmethod
   def assign_interrupt(self, func, id, run_every=-1, is_periodic=True):
      timer = None
      if run_every != -1: 
         timer = threading.Thread(target=func)
      else:
         timer = self.RepeatTimer(run_every, func)
      self.interrupts_table[id] = timer
      timer.start()

      return id

   @classmethod
   def destroy_interrupt(self, id):
      timer = self.interrupts_table.get(id)
      if timer:
         timer.cancel()
         del timer
         return True
      else:
         return False
   