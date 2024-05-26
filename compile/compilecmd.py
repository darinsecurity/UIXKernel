from extension import ext
import runcompile
import sys
import os
import argparse
version = "1.0"

parser = argparse.ArgumentParser(description="uixcompile: Compile the UIX Kernel to yield the UIX Operating System")
print(f"UIXCompile for UIXKernel ({version})")
parser.add_argument('-dist', help="Target distribution (in /compile/dists.) Specifies custom profile that supplements arguments.", default="unix")
parser.add_argument('-base-config', type=str, help="Specify base configuration (config.py) overlayed over the target distribution.", default="default_config")
parser.add_argument('-target', help="Target result name. Specify <dist> for dist, <ver> for version string.", default="uixos-{ver}-{dist}.py")
args = vars(parser.parse_args())

class Default():
   pass

def merge_classes(bottom, top):
    class Merged(bottom):
        pass

    for attr_name in dir(top):
        if not attr_name.startswith('__'):
            top_attr_value = getattr(top, attr_name)
            bottom_attr_value = getattr(bottom, attr_name, None)

            if isinstance(top_attr_value, list) and isinstance(bottom_attr_value, list):
                merged_value = list(set(bottom_attr_value + top_attr_value))
            elif isinstance(top_attr_value, set) and isinstance(bottom_attr_value, set):
                merged_value = bottom_attr_value | top_attr_value
            elif isinstance(top_attr_value, dict) and isinstance(bottom_attr_value, dict):
                merged_value = {**bottom_attr_value, **top_attr_value}
            else:
                merged_value = top_attr_value

            setattr(Merged, attr_name, merged_value)

    return Merged


Args = ""
Output = ""

base_path = os.path.join("compile", "base", ext(args['base_config'], ".py"))
print(f"Using base target: {base_path}")
if os.path.exists(base_path) == False:
   print(f"Path not found for base target: {base_path}")
   exit()

custom_locals = {}
base_Args = ""
base_Output = ""
with open(base_path, "r") as f:
   exec(f.read(), {}, custom_locals)
base_Args = custom_locals["Args"]
base_Output = custom_locals.get("Output") or Default
####
dist_path = os.path.join("compile", "dist", ext(args['dist'], '.py'))
print(f"Using dist target: {dist_path}")
if os.path.exists(dist_path) == False:
   print(f"Path not found for base target: {dist_path}")
   exit()

custom_locals = {}
dist_Args = ""
dist_Output = ""
with open(dist_path, "r") as f:
   exec(f.read(), {}, custom_locals)
dist_Args = custom_locals["Args"]
dist_Output = custom_locals.get("Output") or Default

print("Merging classes..")
Args = merge_classes(base_Args, dist_Args)
Output = merge_classes(base_Output, dist_Output)

Args.dist = (args['dist'],None)

print("Formatting target name..")
target_name = args['target']
target_name = target_name.replace("{ver}", Args.version[0])
target_name = target_name.replace("{dist}", Args.dist[0])
print(f"Compiling target: `{target_name}` for dist `{Args.dist[0]}`")
Output.output_file = target_name
print("#"*15)
runcompile.compile(Args, Output)