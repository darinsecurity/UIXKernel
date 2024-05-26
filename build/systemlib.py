from libassembly import LibraryAssembly

class SystemLib:
   supported_libraries = {}
   def get_supported():
      l = []
      for k, v in SystemLib.supported_libraries.items():
         if v == True:
            l.append(k)
      return l
   def resolve_lib(name):
      if LibraryAssembly.library_namespace[name]:
         return LibraryAssembly.library_namespace[name]
      custom_globals = {}
      exec("import " + name, custom_globals)
      return custom_globals[name]
   def supports_lib(name):
      return name in SystemLib.supported_libraries

   @classmethod
   def import_lib(self, name, add_supported=True):
      if self.supports_lib(name):
         return True, None
      try:
         __import__(name)
         if add_supported:
            SystemLib.supported_libraries[name] = True
         return True, None
      except ImportError as e:
         return False, e
      except Exception as e:
         return False, e