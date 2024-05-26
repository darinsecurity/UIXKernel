import COMPILATION
if COMPILATION.get_headers('hardware', 'rp2'):
   pass##add_dependencies=machine
   
class Hardware:
   cpu_count=1
   cpu_freq=0

   if COMPILATION.get_headers('clockmod', 'hardware', 'rp2'):
      pico_default_clock = 250_000_000
      pico_overclock = 433_000_000
      pico_recv_usb_clock = 133_000_000
      cpu_clock = machine.freq()

   if COMPILATION.get_headers('clockmod'):
      def update_freq(freq):
         if COMPILATION.get_headers('clockmod', 'hardware', 'rp2'):
            machine.freq(freq)
         cpu_freq = freq

