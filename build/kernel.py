import COMPILATION
from systemlib import SystemLib

class Kernel:
   logs = []
   compilation_headers = []
   timestamp_started = -1.0

   persistent_state = {"updated":None}
   if COMPILATION.get_headers('filesystem'):
      persistent_state["usefs"] = True
      persistent_state["fsformat"] = None
      persistent_state["loc"] = "/kernel/kernel.cfg"

   @classmethod
   def log(self, x, end="\n", store=True):
      print(x, end=end)
      if store:
         self.logs.append([x,end])

   @classmethod
   def reboot(self):
      if COMPILATION.get_headers('rp2', 'hardware'):
         machine.reset()
      self.log("Reboot is not implemented on this system! Exiting..")
   
   @classmethod
   def exit(self):
      if SystemLib.supports_lib('sys'):
         import sys
         sys.exit()
      exit()