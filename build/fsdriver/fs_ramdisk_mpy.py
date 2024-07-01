# MicroPython ramdisk filesystem driver
##add_dependencies=os
from kernel import Kernel
# allocate 64 kb of memory

class FSDriver:
   class RAMBlockDev:
       def __init__(self, block_size, num_blocks):
           self.block_size = block_size
           self.data = bytearray(block_size * num_blocks)

       def readblocks(self, block_num, buf):
           for i in range(len(buf)):
               buf[i] = self.data[block_num * self.block_size + i]

       def writeblocks(self, block_num, buf):
           for i in range(len(buf)):
               self.data[block_num * self.block_size + i] = buf[i]

       def ioctl(self, op, arg):
           if op == 4: # get number of blocks
               return len(self.data) // self.block_size
           if op == 5: # get block size
               return self.block_size
              
   default_file_system = "VfsLfs2"
   progsize=256
   bdev = RAMBlockDev(512, 128) 

   class FormattingError(Exception):
      pass

   @classmethod
   def connect_fsi(self):
      os.VfsFat.mkfs(self.bdev)
      self.mount('/')

   @classmethod
   def format_system(self, format=None):
      # delete all (bye bye)
      del self.bdev
      self.bdev = self.RAMBlockDev(512, 128) 
      self.connect_fsi()


   @classmethod
   def umount(self, value):
      os.umount(value)

   @classmethod
   def mount(self, value):
      os.mount(self.bdev, value)

   @classmethod
   def host_supports_open(self):
      return True


