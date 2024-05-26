##add_dependencies=ubinascii

class base64:
   def b64decode(x):
      return ubinascii.a2b_base64(x)
   def b64encode(x):
      return ubinascii.b2a_base64(x)