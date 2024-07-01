from basesystem import BaseSystem


class Info:
   def get_header():
      return "Running " + BaseSystem.name + " " + str(BaseSystem.version) + " " + BaseSystem.vposix + " in " + BaseSystem.subsystem + " Subsystem"
      