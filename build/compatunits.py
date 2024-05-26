class CompatibilityUnits:
   checks_code = {}
   checks_patches = {}

   @classmethod
   def get_code_patch(self, check):
      return base64.b64decode(self.checks_patches[check])

   @classmethod
   def get_code_check(self, check):
      return base64.b64decode(self.checks_code[check])

   @classmethod
   def get_all_checks(self):
      l = []
      for k, v in self.checks_code.items():
         l.append(k)
      return l

   @classmethod
   def get_all_patches(self):
      l = []
      for k, v in self.checks_patches.items():
         l.append(k)
      return l