# default initialization file
# is not compiled or included in the actual program
headers = {}
dist = "unix"


def is_dist(x):
   return x == dist
   
def get_headers(x):
   return x in headers