from basesystem import BaseSystem


class Info:
   def get_header():
      return "Running " + BaseSystem.name + " " + str(BaseSystem.version) + "." + str(BaseSystem.subversion) + " " + BaseSystem.vposix + " in " + BaseSystem.subsystem + " Subsystem"
      