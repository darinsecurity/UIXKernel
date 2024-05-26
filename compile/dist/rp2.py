class Args:
   target_dist = "rp2",
   base_libs = {'base64': 'base64_micropython.py'}
   dist_specific_module = {
       "interrupts": "interrupts/interrupts_rp2.py",
       "fsdriver": "fsdriver/fsdriver_rp2.py"
   }
   libs = ['lwdatetime.py']

   headers = {
       "hardware", "rp2", "clockmod", "freemem", "filesystem", "createhostfs",
   }
