class Args:
   target_dist = "unix",
   base_libs = {}
   dist_specific_module = {"interrupts": "interrupts/interrupts_general.py"}
   libs = ['lwdatetime.py']

   headers = {"hardware", "interrupts"}