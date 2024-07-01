class Args:
   target_dist = "nspire",
   base_libs = {'base64':'base64_compat.py'}
   dist_specific_module = {
       "fsdriver": "fsdriver/fsdriver_simfs.py"
   }
   libs = ['lwdatetime.py']

   headers = {'freemem', 'filesystem', 'createhostfs', 'simulatedfs', 'nspire', "g_use_builtin_import"}