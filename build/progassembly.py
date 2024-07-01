class ProgramAssembly:
   programs = {}
   program_count = 0

   @classmethod
   def get_all_programs(self):
      l = []
      for k, v in self.programs.items():
         l.append(k)
      return l