# default filesystem driver
##add_dependencies=os,rp2
# default filesystem driver
from kernel import Kernel

class FSDriver:
   default_file_system = "VfsLfs2"
   progsize=256
   bdev = rp2.Flash()
   vfs = None

   class FormattingError(Exception):
      pass

   @classmethod
   def connect_fsi(self):
      self.bdev = rp2.Flash()
      func = getattr(os, self.default_file_system, None)
      if func == None:
         Kernel.log("Unknown fs {}".format(self.default_file_system))
      try:
         self.vfs = func(self.bdev, progsize=self.progsize)
         return True
      except Exception as e:
         return False
      

   @classmethod
   def format_system(self, format="VfsLfs2"):
      self.umount('/')
      retrieve_class = getattr(os, format, None)
      if not retrieve_class:
         raise self.FormattingError("unknown fs format")
      retrieve_class.mkfs(self.bdev, progsize=self.progsize)
      Kernel.log("Formatting file system..")
      self.mount('/')


   @classmethod
   def umount(self, value):
      os.umount(value)

   @classmethod
   def mount(self, value):
      os.mount(self.vfs, value)

   @classmethod
   def host_supports_open(self):
      try:
         exec("open()")
         return True
      except NameError: # doesn't exist
         return False
      except Exception as e: # still works
         return True


