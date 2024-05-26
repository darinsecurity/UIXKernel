# UIXKernel
<img src="/display/UIX_Large.png" alt="UIX Logo" style="width:25%;">

### Capable UNIX Simulator
# UIX (Union OS) Interactive Python Subsystem

<details>
  <summary><b>Contents</b></summary>

  1. [Features](#features)
  2. [Supported devices](#supported-devices)
  3. [Compile with UIXCompile](#compilation)
</details>

This is the source code repository for the **Union IX Kernel** (or **UIX**), a capable universal UNIX-like operating system simulator that runs within Python. UIX OS runs under a Python subsystem defined with a set of operating-system like POSIX classes (VPOSIX), and features of operating systems, such as micro services, memory management, etc. 

<img src="/display/screenshot.png" alt="UIX Logo" style="width:40%;">

## Features
UIX is compiled with `uixcompile` as a single Python file which can be ran across any platform or distribution. The UIX file can be packaged with programs and games which are included within the system. With networking support to be added, UIX can run as a standardized network server.

- Virtualized file system. Run a file system entirely within memory on any device. 
- Full hardware management and configuration (available to Python) with drivers for devices.
- Capable of running as a full system on microcontrollers. 
- Set of user library and programs, with configurations for environments.
- Threading, interrupts on Pi Pico

## Supported devices
- Any online Python web compiler
- Raspberry Pi Pico (via MicroPython)
- TI-Nspire CX II graphing calculator
- Unix, Windows

# Compilation
### How to compile UIX OS

Compilation can be done with the `uixcompile` command, which handles all libraries, source code compilation, and etc. as provided in the `compile` folder.

```bash
uixcompile [-h] [-dist DIST] [-base-config BASE_CONFIG] [-target TARGET]
```

To compile, you will need to specify:

### Base configuration
+ A base configuration (`compile/base`)
The default is `default_config.py` which provides the programs, libraries, and compilation procedures for the operating system, as well as kernel headers for source compilation.
```python
# compile/base/default_config.py
class Args:
   target_dist="default",
   package_programs = ['tictactoe.py', 'guessthenumber.py', 'bugged_program.py', 'lineq.py']
   libs = ['lwdatetime.py']
   version="1.1",
   target_kernel = 'uixkernel-1.1.py'
   autoinsert_header = "### PACKAGE-BIN // AUTOINSERT ###"
   libar_header = "### LIBRARY // AUTOREPLACE ###"
   endar_header = "### END // AUTOREPLACE ###"

   use_code_compilation=True,
   clean_code_space=True,
```
This provides the application-specific (not architecture specific) features the operating system will be compiled with. For example, `lwdatetime.py` is the lightweight date time management library used within UIX-OS. All configuration is written as a Python class.


### Distribution Target
Next, you need to specify a specific platform (or dist) to compile on. The default is `unix`, which should run on all platforms that include Python standard libraries. However, you can specify custom libraries, or **compilation headers**, which add new features to the kernel.
For example, the TI Nspire's Python interpreter does not include a `base64` library, and so `unix` compiled OSes will not run on that platform. 
As a solution to this, you can specify a compatible base64 library (`base64_compat.py`) in the dist compilation, which will replace the required lib.


```python
# compile/dist/nspire.py
class Args:
   target_dist = "nspire",
   base_libs = {'base64':'base64_compat.py'}
   libs = ['lwdatetime.py']

   headers = {'freemem'}
```

This target (`nspire`) also comes with a compilation header: `freemem`. When `freemem` is specified in compilation, the kernel will try to conserve memory by freeing unused space. This can, for example, be useful on embedded systems.
To compile the `nspire` version of UIX, you can easily specify:
```
./uixcompile -dist=nspire
```
and `uixcompile` will follow the configuration specified for the distribution `nspire`. 

### Distribution Specific Modules

Sometimes, in compilation, you need to specify a platform-specific kernel module (not just library) that is used in the kernel.
This is easily done by providing `dist_specific_module` in the compilation Args.
```
# compile/dist/rp2.py
class Args:
   target_dist = "rp2",
   base_libs = {'base64': 'base64_micropython.py'}
   dist_specific_module = {
       "interrupts": "interrupts/interrupts_rp2.py",
       "fsdriver": "fsdriver/fsdriver_rp2.py"
   }
...
```

In this case, the modules for 'fsdriver' will be replaced with those in `fsdriver/fsdriver_rp2.py`, and compilation will follow accordingly.


### Compilation Target
All compiled kernels will be saved in `result/`, with the name `uixos-{ver}-{dist}.py`. (`{ver}`> corresponds to the base version, and `{dist}` the target dist.)
However, you can easily specify a new target name with `<ver>` and `<dist>` tags and the compiler will follow accordingly.

```
./uixcompile -dist=rp2 -target=alpha-{dist}.py
```

When this command is ran, the output is:

```
~/UIXKernel-11$ ./uixcompile -dist=rp2 -target=alpha-{dist}.py
UIXCompile for UIXKernel (1.0)
Using base target: compile/base/default_config.py
Using dist target: compile/dist/rp2.py
...
INFO:root:Saving result to result/alpha-rp2.py
```



