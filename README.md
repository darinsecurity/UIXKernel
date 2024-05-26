# UIXKernel
<img src="/display/UIX_Large.png" alt="UIX Logo" style="width:25%;">

# UIX (Union OS) Interactive Python Subsystem

### Capable UNIX Simulator

The Union IX Kernel (or UIX) is the kernel for the UIX 'operating system' that runs within Python. UIX is universal, and can run on many platforms. The UIX Subsystem defines a set of POSIX-like classes (VPOSIX), including interrupt support, device scheduling, microservices, memory management, etc. that turn any Python environment into a fully capable system, or serve as an educational aid. The UIX source file (a single .py file) is compiled using `uixcompile` which compiles and processes every Python library (`/build`) into a single text file that can be deployed anywhere. UIX comes packages with programs and games, and you can easily package your own programs as well. Networking access is to also be added, allowing for a standard configuration of network servers.

<img src="/display/screenshot.png" alt="UIX Logo" style="width:40%;">

## Features:
- Virtualized file system. Run a file system entirely within memory, simulating a UNIX system.
- Full hardware management and configuration (available to Python) with drivers for devices.
- Capable of running as a full system on microcontrollers. 
- Set of user library and programs, with configurations for environments.
- Threading, interrupts on Pi Pico

## Supported devices:
- Any online Python web compiler
- Raspberry Pi Pico (via MicroPython)
- TI-Nspire graphing calculator
- Unix, Windows
