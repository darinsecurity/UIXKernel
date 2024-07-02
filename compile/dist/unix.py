class Args:
   target_dist = "unix",
   base_libs = {}
   dist_specific_module = {"interrupts": "interrupts/interrupts_general.py"}
   dist_specific_module = {
       "fsdriver": "fsdriver/fsdriver_hostos.py"
   }
   libs = ['lwdatetime.py']

   headers = {'freemem', 'filesystem', "hardware", "interrupts"}