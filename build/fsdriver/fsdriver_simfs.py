# default filesystem driver
from kernel import Kernel
from simulatedfs import simulatedfs

class FSDriver:
   default_file_system = "VfsLfs2"
   progsize=256
   vfs = VirtualFileSystem()

   class FormattingError(Exception):
      pass

   @classmethod   
   def open_handler(self, file_path, mode='r'):
      return VirtualFileHandler(vfs=self.vfs, file_path=file_path, mode=mode)


   @classmethod
   def connect_fsi(self):
      return True

   @classmethod
   def format_system(self, format=None):
      # delete all (bye bye)
      self.vfs.reset_fs()


   @classmethod
   def umount(self, value):
      pass

   @classmethod
   def mount(self, value):
      pass

   @classmethod
   def host_supports_open(self):
      return True


