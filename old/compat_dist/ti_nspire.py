# compat flags
# class CompatibilityFlags:
#    system_type="linux/unix"

modules = {}
def is_installed(name):
   try:
      try:
         exec("import " + str(name))
         return True
      except ModuleNotFoundError or ImportError:
         return False
   except NameError:
      return False
   

if is_installed('ti_system'):
   print("Registered ti_system")
   CompatFlags.system_type = "ti_nspire"
   # import ti_system
   # def perf_counter():
   #    return ti_system.get_time_ms()
   # setattr(modules['time'], 'perf_counter', perf_counter)
   modified = True