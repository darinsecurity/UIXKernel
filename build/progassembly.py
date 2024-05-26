class ProgramAssembly:
   programs = {}
   program_count = 0
   use_base64 = True

   @classmethod
   def get_all_programs(self):
      l = []
      for k, v in self.programs.items():
         l.append(k)
      return l