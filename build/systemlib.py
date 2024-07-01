from libassembly import LibraryAssembly

class SystemLib:
   supported_libraries = {}
   override_imports = {} # name: module to override import
   _original_import_method = None

   @classmethod
   def _import_lib_h(self, name, *args, **kwargs):
      # Import lib handler to override __import__
      if self.override_imports.get(name, None):
         return self.override_imports[name]
      return self._original_import_method(name, *args, **kwargs)

   
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
   def import_host_lib(self, name, add_supported=True):
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