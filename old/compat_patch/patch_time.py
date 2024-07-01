def patch_method():
   return 0
if not hasattr(time, 'time'):
   setattr(time, 'existing_method', patch_method)