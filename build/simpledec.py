# SIMPLEDEC:
# A json alternative for key value storage
# Purely string based
# Newline seperated by "="

class SimpleDEC:
   def loads(string):
      result = {}
      for line in string.split("\n"):
         split_line = line.split("=",1)
         if len(split_line) != 2:
            continue
         result[split_line[0]] = split_line[1]
   def dumps(table):
      result = ""
      for key, value in table.items():
         result += "{}={}\n".format(key,value)
      return result