class BaseSystem:
   version = 1
   subversion = 0
   name = "UIXKernel"
   prefix = "uix"
   default_program = "bsi"
   vposix = "VPOSIX/1.0"
   subsystem = "Python"
   author = "Darin Tanner"
class CompatibilityUnits:
   checks_code = {}
   checks_patches = {}

   @classmethod
   def get_code_patch(self, check):
      return base64.b64decode(self.checks_patches[check])
   
   @classmethod
   def get_code_check(self, check):
      return base64.b64decode(self.checks_code[check])
      
   @classmethod
   def get_all_checks(self):
      l = []
      for k, v in self.checks_code.items():
         l.append(k)
      return l

   @classmethod
   def get_all_patches(self):
      l = []
      for k, v in self.checks_patches.items():
         l.append(k)
      return l
class CompatFlags:
   system_type="linux/unix"
class LibraryAssembly:
   libraries = {}
   included = {}

   # to not be touched by computer generated code
   library_namespace = {}
import ubinascii

class base64:
   def b64decode(x):
      return ubinascii.a2b_base64(x)
   def b64encode(x):
      return ubinascii.b2a_base64(x)
LibraryAssembly.libraries["base64"] = """Y2xhc3MgYmFzZTY0OgogICAgQ0hBUlMgPSAiQUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVphYmNkZWZnaGlqa2xtbm9wcXJzdHV2d3h5ejAxMjM0NTY3ODkrLyIKCiAgICBAY2xhc3NtZXRob2QKICAgIGRlZiBjaHVuayhjbHMsIGRhdGEsIGxlbmd0aCk6CiAgICAgICAgcmV0dXJuIFtkYXRhW2k6aStsZW5ndGhdIGZvciBpIGluIHJhbmdlKDAsIGxlbihkYXRhKSwgbGVuZ3RoKV0KCiAgICBAY2xhc3NtZXRob2QKICAgIGRlZiBiNjRlbmNvZGUoY2xzLCBkYXRhKToKICAgICAgICBvdmVycmlkZSA9IDAKICAgICAgICBpZiBsZW4oZGF0YSkgJSAzICE9IDA6CiAgICAgICAgICAgIG92ZXJyaWRlID0gKGxlbihkYXRhKSArIDMgLSBsZW4oZGF0YSkgJSAzKSAtIGxlbihkYXRhKQogICAgICAgIGRhdGEgKz0gYiJceDAwIiAqIG92ZXJyaWRlCgogICAgICAgIHRocmVlY2h1bmtzID0gY2xzLmNodW5rKGRhdGEsIDMpCgogICAgICAgIGJpbnN0cmluZyA9ICIiCiAgICAgICAgZm9yIGNodW5rIGluIHRocmVlY2h1bmtzOgogICAgICAgICAgICBmb3IgeCBpbiBjaHVuazoKICAgICAgICAgICAgICAgIGJpbnN0cmluZyArPSBmb3JtYXQoeCwgJzA4YicpCgogICAgICAgIHNpeGNodW5rcyA9IGNscy5jaHVuayhiaW5zdHJpbmcsIDYpCgogICAgICAgIG91dHN0cmluZyA9ICIiCiAgICAgICAgZm9yIGVsZW1lbnQgaW4gc2l4Y2h1bmtzOgogICAgICAgICAgICBvdXRzdHJpbmcgKz0gY2xzLkNIQVJTW2ludChlbGVtZW50LCAyKV0KCiAgICAgICAgb3V0c3RyaW5nID0gb3V0c3RyaW5nWzotb3ZlcnJpZGVdICsgIj0iICogb3ZlcnJpZGUKICAgICAgICByZXR1cm4gb3V0c3RyaW5nCgogICAgQGNsYXNzbWV0aG9kCiAgICBkZWYgYjY0ZGVjb2RlKGNscywgYjY0X3N0cmluZyk6CiAgICAgICAgIyBCYXNlNjQgY2hhcmFjdGVyIHNldAogICAgICAgIGJhc2U2NF9jaGFycyA9IGNscy5DSEFSUwogICAgICAgIGJhc2U2NF9tYXAgPSB7Y2hhcjogaW5kZXggZm9yIGluZGV4LCBjaGFyIGluIGVudW1lcmF0ZShiYXNlNjRfY2hhcnMpfQoKICAgICAgICAjIFJlbW92ZSBwYWRkaW5nIGNoYXJhY3RlcnMgYW5kIGNvbXB1dGUgdGhlIHBhZGRpbmcgbGVuZ3RoCiAgICAgICAgcGFkZGluZ19sZW5ndGggPSBiNjRfc3RyaW5nLmNvdW50KCc9JykKICAgICAgICBiNjRfc3RyaW5nID0gYjY0X3N0cmluZy5yc3RyaXAoJz0nKQoKICAgICAgICAjIENvbnZlcnQgYmFzZTY0IGNoYXJhY3RlcnMgdG8gdGhlaXIgY29ycmVzcG9uZGluZyB2YWx1ZXMKICAgICAgICBkZWNvZGVkX2JpdHMgPSAiIgogICAgICAgIGZvciBjaGFyIGluIGI2NF9zdHJpbmc6CiAgICAgICAgICAgIGlmIGNoYXIgaW4gYmFzZTY0X21hcDoKICAgICAgICAgICAgICAgIHZhbHVlID0gYmFzZTY0X21hcFtjaGFyXQogICAgICAgICAgICAgICAgIyBDb252ZXJ0IHRoZSB2YWx1ZSB0byBhIDYtYml0IGJpbmFyeSBzdHJpbmcgYW5kIGFwcGVuZCB0byB0aGUgcmVzdWx0CiAgICAgICAgICAgICAgICBkZWNvZGVkX2JpdHMgKz0gZm9ybWF0KHZhbHVlLCAnMDZiJykKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIkludmFsaWQgY2hhcmFjdGVyIGZvdW5kIGluIGJhc2U2NCBzdHJpbmciKQoKICAgICAgICAjIFJlbW92ZSB0aGUgcGFkZGluZyBiaXRzIGZyb20gdGhlIGJpbmFyeSBzdHJpbmcKICAgICAgICBpZiBwYWRkaW5nX2xlbmd0aDoKICAgICAgICAgICAgZGVjb2RlZF9iaXRzID0gZGVjb2RlZF9iaXRzWzotKHBhZGRpbmdfbGVuZ3RoICogMildCgogICAgICAgICMgU3BsaXQgdGhlIGJpbmFyeSBzdHJpbmcgaW50byBieXRlcyAoOCBiaXRzIGVhY2gpCiAgICAgICAgYnl0ZV9hcnJheSA9IGJ5dGVhcnJheSgpCiAgICAgICAgZm9yIGkgaW4gcmFuZ2UoMCwgbGVuKGRlY29kZWRfYml0cyksIDgpOgogICAgICAgICAgICBieXRlX2NodW5rID0gZGVjb2RlZF9iaXRzW2k6aSs4XQogICAgICAgICAgICBpZiBsZW4oYnl0ZV9jaHVuaykgPT0gODoKICAgICAgICAgICAgICAgIGJ5dGVfYXJyYXkuYXBwZW5kKGludChieXRlX2NodW5rLCAyKSkKCiAgICAgICAgcmV0dXJuIGJ5dGVzKGJ5dGVfYXJyYXkpCg=="""
LibraryAssembly.libraries["lwdatetime"] = """IyBMaWdodHdlaWdodCBkYXRldGltZSBsaWJyYXJ5IGluIFB5dGhvbgojIE5vdCBhcyBsYXJnZSBhcyB0aGUgYWN0dWFsIG9uZSAoNzUgS0IpCmNsYXNzIGx3ZGF0ZXRpbWU6CiAgICBkZWYgZ2V0X3RpbWVfZGlmZmVyZW5jZSh0aW1lc3RhbXAxLCB0aW1lc3RhbXAyLCB1bml0cyk6CiAgICAgICAgIyBFbnN1cmUgdGltZXN0YW1wMSBpcyB0aGUgc21hbGxlciBvbmUKICAgICAgICBpZiB0aW1lc3RhbXAxID4gdGltZXN0YW1wMjoKICAgICAgICAgICAgdGltZXN0YW1wMSwgdGltZXN0YW1wMiA9IHRpbWVzdGFtcDIsIHRpbWVzdGFtcDEKICAgIAogICAgICAgICMgQ2FsY3VsYXRlIHRoZSBkaWZmZXJlbmNlIGluIHNlY29uZHMKICAgICAgICB0b3RhbF9zZWNvbmRzID0gdGltZXN0YW1wMiAtIHRpbWVzdGFtcDEKICAgIAogICAgICAgICMgRGljdGlvbmFyeSB0byBob2xkIHRpbWUgdW5pdCB2YWx1ZXMgaW4gc2Vjb25kcwogICAgICAgIHRpbWVfdW5pdHMgPSB7CiAgICAgICAgICAgICd5ZWFycyc6IDMxNTM2MDAwLCAgIyBBcHByb3hpbWF0aW9uOiAzNjUgZGF5cwogICAgICAgICAgICAnZGF5cyc6IDg2NDAwLAogICAgICAgICAgICAnaG91cnMnOiAzNjAwLAogICAgICAgICAgICAnbWludXRlcyc6IDYwLAogICAgICAgICAgICAnc2Vjb25kcyc6IDEKICAgICAgICB9CiAgICAKICAgICAgICAjIFByZXBhcmUgdGhlIHJlc3VsdCBkaWN0aW9uYXJ5CiAgICAgICAgcmVzdWx0ID0ge30KICAgIAogICAgICAgIGZvciB1bml0IGluIHVuaXRzOgogICAgICAgICAgICBpZiB1bml0IGluIHRpbWVfdW5pdHM6CiAgICAgICAgICAgICAgICB1bml0X3ZhbHVlID0gdGltZV91bml0c1t1bml0XQogICAgICAgICAgICAgICAgcmVzdWx0W3VuaXRdID0gdG90YWxfc2Vjb25kcyAvLyB1bml0X3ZhbHVlCiAgICAgICAgICAgICAgICB0b3RhbF9zZWNvbmRzICU9IHVuaXRfdmFsdWUKICAgIAogICAgICAgICMgUHJpbnQgdGhlIHJlc3VsdCBpbiB0aGUgcmVxdWVzdGVkIG9yZGVyCiAgICAgICAgcmV0dXJuICJUaGUgc3lzdGVtIGhhcyBiZWVuIHVwIGZvciAiICsgIiwgIi5qb2luKFt1bml0ICsgIjogIiArIHN0cihpbnQocmVzdWx0W3VuaXRdKSkgZm9yIHVuaXQgaW4gdW5pdHNdKQ=="""
class ProgramAssembly:
   programs = {}
   program_count = 0
   use_base64 = True
   
   @classmethod
   def get_all_programs(self):
      l = []
      for k, v in self.programs.items():
         l.append(k)
      return l
class Flags:
   show_dmesg_output = True
# Computer generated comments, do not modify
LibraryAssembly.included["base64"] = True
LibraryAssembly.included["base64"] = True
LibraryAssembly.included["lwdatetime"] = True
ProgramAssembly.programs["tictactoe"] = """I0xldCdzIHN0YXJ0IGJ5IGluaXRpYWxpemluZyBvdXIgZ2FtZSBib2FyZApib2FyZCA9IFsiLSIsIi0iLCItIiwKICAgICAgICAgIi0iLCItIiwiLSIsCiAgICAgICAgICItIiwiLSIsIi0iXQoKI0tub3cgaWYgZ2FtZSBpcyBzdGlsbCBnb2luZyBvbiBieSBzZXR0aW5nIGl0IHRvIFRydWUKZ2FtZV9vbiA9IFRydWUKCiMgSW5pdGlhbGl6ZSBvdXIgY3VycmVudCBwbGF5ZXIgdG8gYmUgWApjdXJyZW50X3BsYXllciA9ICJYIgoKI0Z1bmN0aW9uIHRvIGRpc3BsYXkgb3VyIGdhbWUgYm9hcmQKZGVmIGRpc3BsYXlfYm9hcmQoKToKICAgIHByaW50KGJvYXJkWzBdICsgIiB8ICIgKyBib2FyZFsxXSArICIgfCAiICsgYm9hcmRbMl0gKyAiICAgICAgIiArICIxfDJ8MyIpCiAgICBwcmludChib2FyZFszXSArICIgfCAiICsgYm9hcmRbNF0gKyAiIHwgIiArIGJvYXJkWzVdICsgIiAgICAgICIgKyAiNHw1fDYiKQogICAgcHJpbnQoYm9hcmRbNl0gKyAiIHwgIiArIGJvYXJkWzddICsgIiB8ICIgKyBib2FyZFs4XSArICIgICAgICAiICsgIjd8OHw5IikKCiMgRnVudGlvbiB0byBkZWZpbmUgcGxheWVycwpkZWYgcGxheWVycygpOgogICAgcHJpbnQoIlNlbGVjdCBQbGF5ZXIgLSBYIG9yIE8iKQogICAgcDEgPSBpbnB1dCgiUGxheWVyMTogIikKICAgIHAyID0gIiIKICAgIGlmIHAxID09ICJYIjoKICAgICAgICBwMiA9ICJPIgogICAgICAgIHByaW50KCJQbGF5ZXIyOiAiICsgcDIpCiAgICBlbGlmIHAxID09ICJPIjoKICAgICAgICBwMiA9ICJYIgogICAgICAgIHByaW50KCJQbGF5ZXIyOiAiICsgcDIpCiAgICBlbGlmIHAxICE9ICJPIiBvciBwMSAhPSAiWCI6CiAgICAgICAgcHJpbnQoIlNvcnJ5LGludmFsaWQgaW5wdXQuIFR5cGUgWCBvciBPIikKICAgICAgICBwbGF5X2dhbWUoKQoKI0RlZmluZSB0aGUgcGxheWVyIHBvc2l0aW9uCmRlZiBwbGF5ZXJfcG9zaXRpb24oKToKICAgIGdsb2JhbCBjdXJyZW50X3BsYXllcgogICAgcHJpbnQoIkN1cnJlbnQgUGxheWVyOiAiICsgY3VycmVudF9wbGF5ZXIpCiAgICBwb3NpdGlvbiA9IGlucHV0KCJDaG9vc2UgcG9zaXRpb24gZnJvbSAxIC0gOTogIikKCiAgICAjIExvb3AgdGhyb3VnaCB0aGUgcHJvZ3JhbSB1bnRpbGwgdGhlcmUgaXMgYSB3aW4gb3IgdGllCiAgICB2YWxpZCA9IEZhbHNlCiAgICB3aGlsZSBub3QgdmFsaWQ6CiAgICAgICAgd2hpbGUgcG9zaXRpb24gbm90IGluIFsiMSIsICIyIiwgIjMiLCAiNCIsICI1IiwgIjYiLCAiNyIsICI4IiwgIjkiXToKICAgICAgICAgIHBvc2l0aW9uID0gaW5wdXQoIkNob29zZSBwb3NpdGlvbiBmcm9tIDEgLSA5OiAiKQogICAgICAgIHBvc2l0aW9uID0gaW50KHBvc2l0aW9uKSAtIDEKCiAgICAgICAgaWYgYm9hcmRbcG9zaXRpb25dID09ICItIjoKICAgICAgICAgICAgdmFsaWQgPSBUcnVlCiAgICAgICAgZWxzZToKICAgICAgICAgICAgcHJpbnQoIlBvc2l0aW9uIGFscmVhZHkgc2VsZWN0ZWQsIGNob29zZSBhbm90aGVyIHBvc2l0aW9uISIpCiAgICBib2FyZFtwb3NpdGlvbl0gPSBjdXJyZW50X3BsYXllcgogICAgZGlzcGxheV9ib2FyZCgpCgojRnVuY3Rpb24gdG8gcGxheSBvdXIgdGljIHRhYyBnYW1lIApkZWYgcGxheV9nYW1lKCk6CiAgICBwcmludCgiTXkgVGljIFRhYyBUb2UgR2FtZSIpCiAgICBkaXNwbGF5X2JvYXJkKCkKICAgIHBsYXllcnMoKQoKICAjbG9vcCAgdG8gZmxpcCBwbGF5ZXJzIHVudGlsbCB0aGVyZSBpcyBhIHdpbgogICAgd2hpbGUgZ2FtZV9vbjoKICAgICAgICBwbGF5ZXJfcG9zaXRpb24oKQoKICAgICAgICAjQ2hlY2sgd2lubmVyCiAgICAgICAgZGVmIGNoZWNrX3dpbm5lcigpOgogICAgICAgICAgICBnbG9iYWwgZ2FtZV9vbgogICAgICAgICAgICAjQ2hlY2sgcm93cyBpZiB0aGVyZSBpcyBhIHdpbiAKICAgICAgICAgICAgaWYgYm9hcmRbMF0gPT0gYm9hcmRbMV0gPT0gYm9hcmRbMl0gIT0gIi0iOgogICAgICAgICAgICAgICAgZ2FtZV9vbiA9IEZhbHNlCiAgICAgICAgICAgICAgICBwcmludCgiQ29uZ3JhdHVsYXRpb25zICIgKyBib2FyZFswXSsiIHlvdSBXT04hIikKICAgICAgICAgICAgZWxpZiBib2FyZFszXSA9PSBib2FyZFs0XSA9PSBib2FyZFs1XSAhPSAiLSI6CiAgICAgICAgICAgICAgICBnYW1lX29uID0gRmFsc2UKICAgICAgICAgICAgICAgIHByaW50KCJDb25ncmF0dWxhdGlvbnMgIiArIGJvYXJkWzNdKyIgeW91IFdPTiEiKQogICAgICAgICAgICBlbGlmIGJvYXJkWzZdID09IGJvYXJkWzddID09IGJvYXJkWzhdICE9ICItIjoKICAgICAgICAgICAgICAgIGdhbWVfb24gPSBGYWxzZQogICAgICAgICAgICAgICAgcHJpbnQoIkNvbmdyYXR1bGF0aW9ucyAiICsgYm9hcmRbNl0rIiB5b3UgV09OISIpCiAgICAgICAgICAgICAjQ2hlY2sgY29sdW1ucyBpZiB0aGVyZSBpcyBhIHdpbgogICAgICAgICAgICBlbGlmIGJvYXJkWzBdID09IGJvYXJkWzNdID09IGJvYXJkWzZdICE9ICItIjoKICAgICAgICAgICAgICAgIGdhbWVfb24gPSBGYWxzZQogICAgICAgICAgICAgICAgcHJpbnQoIkNvbmdyYXR1bGF0aW9ucyAiICsgYm9hcmRbMF0rIiB5b3UgV09OISIpCiAgICAgICAgICAgIGVsaWYgYm9hcmRbMV0gPT0gYm9hcmRbNF0gPT0gYm9hcmRbN10gIT0gIi0iOgogICAgICAgICAgICAgICAgZ2FtZV9vbiA9IEZhbHNlCiAgICAgICAgICAgICAgICBwcmludCgiQ29uZ3JhdHVsYXRpb25zICIgKyBib2FyZFsxXSsiIHlvdSBXT04hIikKICAgICAgICAgICAgZWxpZiBib2FyZFsyXSA9PSBib2FyZFs1XSA9PSBib2FyZFs4XSAhPSAiLSI6CiAgICAgICAgICAgICAgICBnYW1lX29uID0gRmFsc2UKICAgICAgICAgICAgICAgIHByaW50KCJDb25ncmF0dWxhdGlvbnMgIiArIGJvYXJkWzJdKyIgeW91IFdPTiEiKQogICAgICAgICAgICAgI0NoZWNrIGRpYWdvbmFscyBpZiB0aGVyZSBpcyBhIHdpbgogICAgICAgICAgICBlbGlmIGJvYXJkWzBdID09IGJvYXJkWzRdID09IGJvYXJkWzhdICE9ICItIjoKICAgICAgICAgICAgICAgIGdhbWVfb24gPSBGYWxzZQogICAgICAgICAgICAgICAgcHJpbnQoIkNvbmdyYXR1bGF0aW9ucyAiICsgYm9hcmRbMF0rIiB5b3UgV09OISIpCiAgICAgICAgICAgIGVsaWYgYm9hcmRbMl0gPT0gYm9hcmRbNF0gPT0gYm9hcmRbNl0gIT0gIi0iOgogICAgICAgICAgICAgICAgZ2FtZV9vbiA9IEZhbHNlCiAgICAgICAgICAgICAgICBwcmludCgiQ29uZ3JhdHVsYXRpb25zICIrIGJvYXJkWzZdKyIgeW91IFdPTiEiKQogICAgICAgICAgICAgI0lmIG5vbmUgb2YgdGhlIGFib3ZlLCB0aGVuLCBpdCdzIGEgdGllCiAgICAgICAgICAgIGVsaWYgIi0iIG5vdCBpbiBib2FyZDoKICAgICAgICAgICAgICAgIGdhbWVfb24gPSBGYWxzZQogICAgICAgICAgICAgICAgcHJpbnQoIkl0J3MgYSBUaWUiKQogICAgICAgICAgICAgICAgZXhpdCgpCgogICAgICAgICNGdW5jdGlvbiB0byBmbGlwIHBsYXllcgogICAgICAgIGRlZiBmbGlwX3BsYXllcigpOgogICAgICAgICAgICBnbG9iYWwgY3VycmVudF9wbGF5ZXIKICAgICAgICAgICAgaWYgY3VycmVudF9wbGF5ZXIgPT0gIlgiOgogICAgICAgICAgICAgICAgY3VycmVudF9wbGF5ZXIgPSAiTyIKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIGN1cnJlbnRfcGxheWVyID0gIlgiCiAgICAgICAgZmxpcF9wbGF5ZXIoKQogICAgICAgIGNoZWNrX3dpbm5lcigpCiNQbGF5IG91ciB0aWMgdGFjIGdhbWUKcGxheV9nYW1lKCk="""
ProgramAssembly.programs["guessthenumber"] = """aW1wb3J0IHJhbmRvbQp3aGlsZSBUcnVlOgogICBwcmludCgiQ2FuIHlvdSBndWVzcyB0aGUgbnVtYmVyPyBUaGUgbnVtYmVyIGlzIGJldHdlZW4gMSBhbmQgMTAwLiIpCiAgIGd1ZXNzX2NvdW50ID0gMAogICBhY3R1YWxfbnVtYmVyID0gcmFuZG9tLnJhbmRpbnQoMSwxMDApCiAgIHVzZXJfbnVtYmVyID0gMAogICB3aGlsZSB1c2VyX251bWJlciAhPSBhY3R1YWxfbnVtYmVyOgogICAgICB1c2VyX2lucHV0ID0gaW5wdXQoIj4gIikKICAgICAgaWYgbm90IHVzZXJfaW5wdXQuaXNudW1lcmljKCk6CiAgICAgICAgIHByaW50KCJQbGVhc2UgcHJvdmlkZSBhIHZhbGlkIG51bWJlci4gIikKICAgICAgICAgY29udGludWUKICAgICAgdXNlcl9udW1iZXIgPSBpbnQodXNlcl9pbnB1dCkKICAgICAgaWYgdXNlcl9udW1iZXIgPT0gYWN0dWFsX251bWJlcjoKICAgICAgICAgcHJpbnQoZiJZb3UgZ3Vlc3NlZCB0aGUgbnVtYmVyISBJdCB3YXMge30uIi5mb3JtYXQodXNlcl9udW1iZXIpKQogICAgICAgICBicmVhawogICAgICBlbHNlOgogICAgICAgICBwcmludChmIlRyeSBhZ2FpbiEgVGhlIG51bWJlciBpcyAiLCBlbmQ9IiIpCiAgICAgICAgIGlmIHVzZXJfbnVtYmVyID4gYWN0dWFsX251bWJlcjoKICAgICAgICAgICAgcHJpbnQoInNtYWxsZXIuIikKICAgICAgICAgZWxzZToKICAgICAgICAgICAgcHJpbnQoImJpZ2dlci4iKQogICBwbGF5X2FnYWluID0gaW5wdXQoIlBsYXkgYWdhaW4/IChZL04pIikKICAgaWYgcGxheV9hZ2FpbiAhPSAiWSI6CiAgICAgIGJyZWFr"""
ProgramAssembly.programs["bugged_program"] = """aW1wb3J0IF9majJvZzM0CjEzaWBqMzBg"""
ProgramAssembly.programs["lineq"] = """ZGVmIGdldF9jb29yZGluYXRlcygpOgogICAgIiIiRnVuY3Rpb24gdG8gZ2V0IGNvb3JkaW5hdGVzIGZyb20gdGhlIHVzZXIuIiIiCiAgICB4MSwgeTEgPSBtYXAoZmxvYXQsIGlucHV0KCJFbnRlciB0aGUgZmlyc3QgcG9pbnQgKHgxIHkxKTogIikuc3BsaXQoKSkKICAgIHgyLCB5MiA9IG1hcChmbG9hdCwgaW5wdXQoIkVudGVyIHRoZSBzZWNvbmQgcG9pbnQgKHgyIHkyKTogIikuc3BsaXQoKSkKICAgIHJldHVybiAoeDEsIHkxKSwgKHgyLCB5MikKCmRlZiBjYWxjdWxhdGVfc2xvcGVfaW50ZXJjZXB0KHBvaW50MSwgcG9pbnQyKToKICAgICIiIkZ1bmN0aW9uIHRvIGNhbGN1bGF0ZSB0aGUgc2xvcGUgKG0pIGFuZCB5LWludGVyY2VwdCAoYikgb2YgdGhlIGxpbmUuIiIiCiAgICB4MSwgeTEgPSBwb2ludDEKICAgIHgyLCB5MiA9IHBvaW50MgoKICAgIGlmIHgxID09IHgyOgogICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIlRoZSB0d28gcG9pbnRzIG11c3QgaGF2ZSBkaWZmZXJlbnQgeC1jb29yZGluYXRlcyBmb3IgYSBub24tdmVydGljYWwgbGluZS4iKQoKICAgICMgQ2FsY3VsYXRlIHRoZSBzbG9wZSAobSkKICAgIG0gPSAoeTIgLSB5MSkgLyAoeDIgLSB4MSkKICAgICMgQ2FsY3VsYXRlIHRoZSB5LWludGVyY2VwdCAoYikKICAgIGIgPSB5MSAtIG0gKiB4MQoKICAgIHJldHVybiBtLCBiCgpkZWYgbWFpbigpOgogICAgIyBHZXQgY29vcmRpbmF0ZXMgZnJvbSB0aGUgdXNlcgoKICAgIHdoaWxlIFRydWU6CiAgICAgICAgcG9pbnQxLCBwb2ludDIgPSBnZXRfY29vcmRpbmF0ZXMoKQogICAgCiAgICAgICAgdHJ5OgogICAgICAgICAgICAjIENhbGN1bGF0ZSBzbG9wZSBhbmQgaW50ZXJjZXB0CiAgICAgICAgICAgIG0sIGIgPSBjYWxjdWxhdGVfc2xvcGVfaW50ZXJjZXB0KHBvaW50MSwgcG9pbnQyKQogICAgCiAgICAgICAgICAgICMgRm9ybWF0IGFuZCBwcmludCB0aGUgbGluZSBlcXVhdGlvbgogICAgICAgICAgICBpZiBiID49IDA6CiAgICAgICAgICAgICAgICBwcmludCgiVGhlIGVxdWF0aW9uIG9mIHRoZSBsaW5lIGlzOiB5ID0gezouMmZ9eCArIHs6LjJmfSIuZm9ybWF0KG0sIGIpKQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgcHJpbnQoIlRoZSBlcXVhdGlvbiBvZiB0aGUgbGluZSBpczogeSA9IHs6LjJmfXggLSB7Oi4yZn0iLmZvcm1hdChtLCBhYnMoYikpKQogICAgCiAgICAgICAgZXhjZXB0IFZhbHVlRXJyb3IgYXMgZToKICAgICAgICAgICAgcHJpbnQoZSkKCiAgICAgICAgaWYgaW5wdXQoIlRyeSBhZ2Fpbj8gKFkvTik6ICIpLnVwcGVyKCkgIT0gIlkiOgogICAgICAgICAgICBicmVhawoKbWFpbigpCg=="""
ProgramAssembly.program_count = 4
class SystemLib:
   supported_libraries = {}
   def get_supported():
      l = []
      for k, v in SystemLib.supported_libraries.items():
         if v == True:
            l.append(k)
      return l
   def resolve_lib(name):
      if LibraryAssembly.library_namespace[name]:
         return LibraryAssembly.library_namespace[name]
      custom_globals = {}
      exec("import " + name, custom_globals)
      return custom_globals[name]
   def supports_lib(name):
      return name in SystemLib.supported_libraries
   def import_lib(name, add_supported=True):
      try:
         exec("import " + str(name))
         if add_supported:
            SystemLib.supported_libraries[name] = True
         return True, None
      except ImportError as e:
         return False, e
      except Exception as e:
         return False, e
class BaseSystemInterface:
   msg = "Base System Interface"
   prefix = "$:"

   class BlankTermInput(Exception):
      pass
      
   class Commands:
      commands = ['author', 'echo', 'posix_exit', 'help', 'exit_system', 'dmesg', 'uptime', 'clear', 'debug_prog']

      def debug_prog(self, input):
         print(ProgramAssembly.programs)
         
      def clear(self, input):
         POSIX.clear_term()
      
      def uptime(self, input):
         if not SystemLib.supports_lib('time'):
            print("This system does not include the `time` library, no time support.")
            return
         if not SystemLib.supports_lib('lwdatetime'):
            print("Please compile UIXKernel with the included `lwdatetime` library for datetime support.")
            return
         import time
         if hasattr(time, 'time') == False:
            print("Time function lacks .time() property, can not capture time.")
            return
         lwdatetime = SystemLib.resolve_lib('lwdatetime')
         cur_time = time.time()
         print(lwdatetime.get_time_difference(cur_time, Kernel.timestamp_started, ['days','hours', 'minutes','seconds']))
      
      def dmesg(self, input):
         for log in Kernel.logs:
            print(log[0], end=log[1])
      def exit_system(self, input):
         POSIX.exit_system()
      def author(self, input):
         print(BaseSystem.author)
      def echo(self, input):
         print(input[5:])
      def posix_exit(self, input):
         POSIX.exit_program()
      def help(self, input):
         print("{}: Available commands".format(BaseSystem.name))
         print(", ".join(self.commands))
         print()
         print("Available programs")
         print(", ".join(ProgramAssembly.get_all_programs()))

   @classmethod
   def get_command(self, name):
      if name in self.Commands.commands:
         func = getattr(self.Commands, name, None)
         if func == None:
            return False
         return func
      else:
         return False
      
   @classmethod
   def run(self):
      print(self.msg + " on " + str(CompatFlags.system_type))

      suffix_word = ""
      if ProgramAssembly.program_count != 1:
         suffix_word = "s"
      print("{} program{} on system.".format(ProgramAssembly.program_count, suffix_word))
      print("Type `help` for help.")
      while True:
         try:
            user_input = input(self.prefix + " ")
   
            args = user_input.split(" ")
            if args == ['']:
               raise self.BlankTermInput
            command = args[0]
            command_method = self.get_command(command)
            
            is_packaged_program = command in ProgramAssembly.programs
            
            if command_method:
               command_method(self.Commands, user_input)
               # determine_args = 2
               # try:
               #    determine_args = command_method.__code__.co_argcount
               # except Exception as e:
               #    pass
               # if determine_args == 1:
               #    command_method(self.Commands)
               # else:
               #    command_method(self.Commands, user_input)
            elif is_packaged_program:
               return command, command
            else:
               print("{}: unknown command or program `{}`".format(BaseSystem.prefix, command))
         except self.BlankTermInput:
            # pass
            pass
class Kernel:
   logs = []
   timestamp_started = -1.0

   @classmethod
   def log(self, x, end="\n", store=True):
      print(x, end=end)
      if store:
         self.logs.append([x,end])
class POSIX:
   class Interpreter:
      variable = []
      @classmethod
      def get_variable(self):
         return set(globals().keys())

      @classmethod
      def capture_variable(self):
         self.variable = self.get_variable()

      @classmethod
      def restore_variable(self):
         new_vars = self.get_variable()
         added_vars = new_vars - self.variable
         for var in added_vars:
             del globals()[var]
   class RunState:
      pass
   class ProgramState:
      active_program = BaseSystem.default_program

      @classmethod
      def set_default_interface(self):
         self.active_program = BaseSystem.default_program

      @classmethod
      def alter_interface(self, name):
         self.active_program = name
   class Interrupts:
      class ProgramExit(Exception):
         pass
      class PrivilegeRequired(Exception):
         pass
   class SystemInterrupts:
      class ExitSystem(Exception):
         pass
      
   def clear_term():
      print("\033c", end="")

   @classmethod
   def exit_system(self):
      if self.ProgramState.active_program == 'bsi':
         raise self.SystemInterrupts.ExitSystem
      else:
         raise self.Interrupts.PrivilegeRequired('Require permissions for exit_system')
   
   @classmethod
   def exit_program(self):
      raise self.Interrupts.ProgramExit
def call_exit():
   exit()

def test_exec(code):
   try:
      exec(code)
      return True
   except Exception:
      return False

def log(x, end="\n", store=True):
   Kernel.log(x, end, store)
   
def print_header():
   log("Running " + BaseSystem.name + " " + str(BaseSystem.version) + "." + str(BaseSystem.subversion) + " " + BaseSystem.vposix + " in " + BaseSystem.subsystem + " Subsystem")

print_header()
log("Decoding libraries..")
for library_name, library in LibraryAssembly.libraries.items():
   custom_globals = {}
   library_code = base64.b64decode(library) + "\n{} = {}".format(library_name, library_name).encode()
   # the class is now defined in custom globals
   exec(library_code, custom_globals)
   if custom_globals[library_name]:
      LibraryAssembly.library_namespace[library_name] = custom_globals[library_name]
      LibraryAssembly.libraries[library_name] = True
      SystemLib.supported_libraries[library_name] = True
   else:
      del LibraryAssembly.libraries[library_name]
      
log("Decoding programs..")
for program_name, program in ProgramAssembly.programs.items():
   ProgramAssembly.programs[program_name] = base64.b64decode(program)

log("Checking if this system has `exec` capabilities..")
if test_exec('') == False:
   log("`exec` required for system! Fail!")
   call_exit()
check_lib = ['os', 'sys', 'math', 'time', 'random', 'signal', 'threading', 'cmath', 'ast', 'zlib', 'traceback']
for lib in check_lib:
   log("Checking if `" + lib + '` is available.. ', end="")
   success, error = SystemLib.import_lib(lib)
   if success:
      log("OK")
   else:
      log("FALSE")
log("Supported libraries: " + ", ".join(SystemLib.get_supported()))

log("Starting VPOSIX runtime..")
checks = CompatibilityUnits.get_all_checks()
if len(checks) > 0:
   log("Using compatibility checks compiled for: " + ', '.join(checks))
   for check in checks:
      code = CompatibilityUnits.get_code_check(check)
      custom_locals = {"modified":False}
      if not code:
         continue
      exec(code, globals(), custom_locals)
      if custom_locals["modified"]:
         print("Modification occured.")
      print("Attempted check `{}` (stat: {})".format(check, custom_locals['modified']))
del checks
patches = CompatibilityUnits.get_all_patches()
if len(patches) > 0:
   log("Applying compatibility patches in sequential order: " + ', '.join(patches))
   for patch in patches:
      code = CompatibilityUnits.get_code_patch(patch)
      custom_locals = {}
      exec(code, globals(), custom_locals)

# mark system started
if SystemLib.supports_lib("time"):
   import time
   if hasattr(time, 'time'):
      Kernel.timestamp_started = time.time()

log("Capturing state..")
clear_terminal = False
POSIX.Interpreter.capture_variable()
log("Starting loop..\n")
while True:
   try:
      POSIX.ProgramState.set_default_interface()
      if clear_terminal:
         POSIX.clear_term()
      
      exec_name, exec_program = BaseSystemInterface.run()
      # when exit out of BSI, execute corresponding program.
      
      # execute program
      # set program state
      POSIX.ProgramState.alter_interface(exec_name)
      exec(ProgramAssembly.programs[exec_name])
      
   except KeyboardInterrupt:
      active_program = POSIX.ProgramState.active_program
      if active_program == "bsi":
         print("\nExiting system..")
         call_exit()
      else:
         print("\nExiting program..")
         POSIX.Interpreter.restore_variable()
         
   except POSIX.Interrupts.ProgramExit:
      active_program = POSIX.ProgramState.active_program
      if active_program == "bsi":
         print("Received POSIX exit program signal from Base System Interface. This is not supported. Restarting interpreter..")
      POSIX.Interpreter.restore_variable()
   except POSIX.SystemInterrupts.ExitSystem:
      # exit the system
      call_exit()
   except Exception as e:
      active_program = POSIX.ProgramState.active_program
      is_running_program = True

      if active_program == "bsi":
         is_running_program = False

      if is_running_program or True: # show all errors
         print("\n" + "-"*20)
         print("{}: Error. Program `{}` encountered an exception while running, and must exit. ".format(BaseSystem.prefix,active_program))
         print("Exception: {}".format(type(e).__name__))
         if SystemLib.supports_lib('traceback'):
            import traceback
            traceback.print_exc()
         else:
            print("No traceback available on this system.")
         clear_terminal = False
         print("-"*20)
         POSIX.Interpreter.restore_variable()
         continue

   clear_terminal = True