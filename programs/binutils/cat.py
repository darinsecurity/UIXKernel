import os
import sys

if len(sys.argv) == 1:
   while True:
      try:
         print(input())
      except Exception as e:
         break
else:
   with open(sys.argv[1], 'r') as f:
      print(f.read())