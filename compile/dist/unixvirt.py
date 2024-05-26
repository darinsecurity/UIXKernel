class Args:
   target_dist = "nspire",
   base_libs = {}
   dist_specific_module = {
       #"interrupts": "interrupts/interrupts_rp2.py",
       "fsdriver": "fsdriver/fsdriver_simfs.py"
   }
   libs = ['lwdatetime.py']

   headers = {'freemem', 'filesystem', 'simulatedfs', 'createhostfs'}