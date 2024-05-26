# UIXKernel
<img src="/display/UIX_Large.png" alt="UIX Logo" style="width:25%;">

### A capable UNIX simulator
# UIX (Union OS) Interactive Python Subsystem

<details>
  <summary><b>Contents</b></summary>

  1. [Features](#features)
  2. [Supported Devices](#supported-devices)
  3. [Compilation](#compilation)
  4. [Usage](usage-of-uix-os)
  5. [Compilation Features](compiling-with-features)
</details>

This is the source code repository for the **Union IX Kernel** (or **UIX**), a capable universal UNIX-like operating system simulator that runs within Python. UIX OS runs under a Python subsystem defined with a set of operating-system-like POSIX classes (VPOSIX) and features of operating systems, such as microservices, memory management, etc.

<img src="/display/screenshot.png" alt="UIX Screenshot" style="width:40%;">

## Features
UIX is compiled with `uixcompile` as a single Python file which can run across any platform or distribution. The UIX file can be packaged with programs and games which are included within the system. With networking support to be added, UIX can run as a standardized network server.

- Virtualized file system: Run a file system entirely within memory on any device.
- Full hardware management and configuration (available to Python) with drivers for devices.
- Capable of running as a full system on microcontrollers.
- Set of user libraries and programs, with configurations for environments.
- Threading and interrupts on Pi Pico.

## Supported Devices
- Any online Python web compiler.
- Raspberry Pi Pico (via MicroPython).
- TI-Nspire CX II graphing calculator.
- Unix, Windows.

## Compilation
### How to Compile UIX OS

Compilation can be done with the `uixcompile` command, which handles all libraries, source code compilation, etc., as provided in the `compile` folder.

```bash
uixcompile [-h] [-dist DIST] [-base-config BASE_CONFIG] [-target TARGET]
```

To compile, you will need to specify:

### Base Configuration
A base configuration (`compile/base`)
The default is `default_config.py` which provides the programs, libraries, and compilation procedures for the operating system, as well as kernel headers for source compilation.

```python
# compile/base/default_config.py
class Args:
    target_dist = "default"
    package_programs = ['tictactoe.py', 'guessthenumber.py', 'bugged_program.py', 'lineq.py']
    libs = ['lwdatetime.py']
    version = "1.1"
    target_kernel = 'uixkernel-1.1.py'
    autoinsert_header = "### PACKAGE-BIN // AUTOINSERT ###"
    libar_header = "### LIBRARY // AUTOREPLACE ###"
    endar_header = "### END // AUTOREPLACE ###"
    use_code_compilation = True
    clean_code_space = True
```

This configuration provides the application-specific (not architecture-specific) features the operating system will be compiled with. For example, `lwdatetime.py` is the lightweight date time management library used within UIX-OS. All configuration is written as a Python class.

### Distribution Target
Next, you need to specify a specific platform (or dist) to compile on. The default is `unix`, which should run on all platforms that include Python standard libraries. However, you can specify custom libraries or **compilation headers**, which add new features to the kernel.

For example, the TI Nspire's Python interpreter does not include a `base64` library, so `unix` compiled OSes will not run on that platform. As a solution, you can specify a compatible base64 library (`base64_compat.py`) in the dist compilation, which will replace the required lib.

```python
# compile/dist/nspire.py
class Args:
    target_dist = "nspire"
    base_libs = {'base64': 'base64_compat.py'}
    libs = ['lwdatetime.py']
    headers = {'freemem'}
```

This target (`nspire`) also comes with a compilation header: `freemem`. When `freemem` is specified in compilation, the kernel will try to conserve memory by freeing unused space. This can, for example, be useful on embedded systems. To compile the `nspire` version of UIX, you can easily specify:

```bash
./uixcompile -dist=nspire
```

and `uixcompile` will follow the configuration specified for the distribution `nspire`.

### Distribution Specific Modules
Sometimes, in compilation, you need to specify a platform-specific kernel module (not just library) that is used in the kernel. This is easily done by providing `dist_specific_module` in the compilation Args.

```python
# compile/dist/rp2.py
class Args:
    target_dist = "rp2"
    base_libs = {'base64': 'base64_micropython.py'}
    dist_specific_module = {
        "interrupts": "interrupts/interrupts_rp2.py",
        "fsdriver": "fsdriver/fsdriver_rp2.py"
    }
```

In this case, the modules for 'fsdriver' will be replaced with those in `fsdriver/fsdriver_rp2.py`, and compilation will follow accordingly.

### Compilation Target
All compiled kernels will be saved in `result/`, with the name `uixos-{ver}-{dist}.py` (`{ver}` corresponds to the base version, and `{dist}` the target dist). However, you can easily specify a new target name with `<ver>` and `<dist>` tags, and the compiler will follow accordingly.

```bash
./uixcompile -dist=rp2 -target=alpha-{dist}.py
```

When this command is run, the output is:

```bash
~/UIXKernel-11$ ./uixcompile -dist=rp2 -target=alpha-{dist}.py
UIXCompile for UIXKernel (1.0)
Using base target: compile/base/default_config.py
Using dist target: compile/dist/rp2.py
...
INFO:root:Saving result to result/alpha-rp2.py
```

## Usage of UIX OS

Once the OS file (a single Python file) is run, you will be booted into a shell. This is known as the **Base System Interface** (or `bsi`) for short.

<img src="https://github.com/darinsecurity/UIXKernel/assets/110881816/1b437a96-c349-4477-bb7d-c7fac63f25a3" alt="Screenshot" style="width:55%;">

`bsi` is the default shell. Just like any UNIX system, commands can be run which in turn execute programs. However, the BSI shell includes a set of internal commands, related to diagnostics and other tools, that run even without any programs. Some internal features of the system are controlled with these commands.

Type `help` to get a list of commands.

<img src="https://github.com/darinsecurity/UIXKernel/assets/110881816/6fb34bad-4000-4c2b-af76-1f5d8f3754f2" alt="Help Screenshot" style="width:60%;">

You can easily package your own commands or use those included within the UIX operating system.

This system was not packaged with filesystem support. Filesystem support is included in base distributions, which in turn also includes the standard system commands. To learn more about compiling system features, go [here](#compiling-with-features).

## Compiling with Features
UIX includes a host of compilation headers which control the features of your operating system:

### Available Features
<details>
  <summary>hardware</summary>
  Add kernel hardware support and features related to hardware management, GPIO, clock management, etc.
  When this is toggled, the command `hwservice` is packaged into the BSI.

  `hwservice` provides a general hardware overview available on the system. When `clockmod` is enabled, the command can also change the frequency of the CPU.
</details>

<details>
  <summary>interrupts</summary>
  Add threading support and interrupt support to the kernel. This is vital for multiprocessing tasks and services, which require threading and/or interrupts to take place.

  On embedded MicroPython platforms such as the Pi Pico (`rp2`), this will use the MicroPython `_thread` feature and also timers for multithreading.
</details>

<details>
  <summary>clockmod</summary>
  Add support for managing CPU clock frequency and information. Currently, this is supported only for MicroPython, not other systems. This is integrated into the `hwservice` command which requires `hardware` to also be specified.

  Usage:
  ```bash
  hwservice freq <hz: int>
  ```

  Example:
  ```bash
  hwservice freq 250000000
  ```
</details>

<details>
  <summary>networking</summary>
  ** IN PROGRESS ** Implement network support and configuration. Not functional yet.
</details>

<details>
  <summary>filesystem</summary>
  ** IN PROGRESS ** Implement full file system support for the host system. Configurations are made to make the file system suitable for execution. This is critical to most features that require files.
  On Python interpreters where file systems (or functions, such as `open()`) aren't available, specify `simulatedfs` to create a

 virtual in-memory file system. This will reconfigure `os`, and create a new `open()` function that uses the VFS instead.

  On embedded systems, specify `createhostfs` to reformat and set up the host file systems. This is supported for MicroPython only.
</details>

<details>
  <summary>createhostfs</summary>
  ** IN PROGRESS ** On MicroPython and embedded systems, reformat the entire flash / available storage for use within the UIX operating system.

  On the Raspberry Pi Pico, this formats the file system to "VfsLfs2" by default.
</details>

<details>
  <summary>simulatedfs</summary>
  ** IN PROGRESS ** Create the simulated file system inside memory and configure utility functions and Python to use the virtual file system.
</details>

<details>
  <summary>freemem</summary>
  After boot, delete non-essential data and functions to conserve memory.
</details>
