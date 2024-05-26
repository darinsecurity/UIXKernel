from fsdriver import FSDriver
from kernel import Kernel
from systemlib import SystemLib
from simpledec import SimpleDEC
import COMPILATION

class FileSystem:
   filesystem_available = False


   if COMPILATION.get_headers('createhostfs'):
      @classmethod
      def init_fs(self):
         supports_open = FSDriver.host_supports_open()
         if not supports_open:
            Kernel.log("This system does not have an open() function. ")
            return
         if SystemLib.supports_lib('os') == False:
            Kernel.log("No `os` module -- required for journalfs.")
            return
   
         if Kernel.persistent_state['usefs'] == True:
            Kernel.log("Filesystem enabled on kernel.")

         def dump_pstate():
            with open(Kernel.persistent_state["loc"], 'w+') as f:
               f.write(SimpleDEC.dumps(Kernel.persistent_state))
         def read_pstate():
            persistent_state = {}
            with open(Kernel.persistent_state["loc"], 'r') as f:
               persistent_state = SimpleDEC.loads(f.read())
            return persistent_state

         def reset_fs(do_format=False):
            if do_format:
               FSDriver.format_system()
               FSDriver.mount('/')
            os.chdir('/')
            os.mkdir('kernel')
            dump_pstate()
         
         import os
         
         status = FSDriver.connect_fsi()
      
         if status:
            try:
               persistent_state = read_pstate()
            except Exception as e:
               reset_fs(False)
         else:
            reset_fs(True)
         os.chdir('/')
         persistent_state = read_pstate()
            
         self.filesystem_available = True
   @classmethod
   def init(self):
      if COMPILATION.get_headers('createhostfs'):
         self.init_fs()
      Kernel.log("Finished os initialization!")
      pass