class util:
   def isnumeric(x):
      allowed = {"0","1","2","3","4","5","6","7","8","9"}
      for i in x: 
         if i not in allowed:
            return False
      return True