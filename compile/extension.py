
def strip_extension(path: str,ext: str):
   if len(ext) > len(path):
      return path
   if path.endswith(ext):
      return path[:-len(ext)]
   return path

def ext(path,n):
   return strip_extension(path,n)+n