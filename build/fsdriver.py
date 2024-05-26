# default filesystem driver

class FSDriver:
   default_file_system = "fat"

   @classmethod
   def connect_fsi(self):
      # Reconnect file system interface
      pass
   
   @classmethod
   def return_fs_object(self):
      pass
   
   @classmethod
   def format_system(self, format):
      pass

   @classmethod
   def umount(self, **args):
      pass

   @classmethod
   def mount(self, args):
      pass

   @classmethod
   def host_supports_open(self):
      try:
         exec("open()")
         return True
      except NameError: # doesn't exist
         return False
      except Exception as e: # still works
         return True

