import threading
import base64

class BaseSystem:
    version = 1
    subversion = 1
    name = 'UIXKernel'
    prefix = 'uix'
    default_program = 'bsi'
    vposix = 'VPOSIX/1.0'
    subsystem = 'Python'
    author = 'Darin Tanner'

class util:

    def isnumeric(x):
        allowed = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        for i in x:
            if i not in allowed:
                return False
        return True

class SimpleDEC:

    def loads(string):
        result = {}
        for line in string.split('\n'):
            split_line = line.split('=', 1)
            if len(split_line) != 2:
                continue
            result[split_line[0]] = split_line[1]

    def dumps(table):
        result = ''
        for key, value in table.items():
            result += '{}={}\n'.format(key, value)
        return result

class Hardware:
    cpu_count = 1
    cpu_freq = 0

class Interrupts:
    Timer = threading.Timer
    interrupts_table = {}

    class RepeatTimer(Timer):

        def run(self):
            while not self.finished.wait(self.interval):
                self.function(*self.args, **self.kwargs)
            del self

    @classmethod
    def retrieve_interrupt(self, id):
        return self.interrupts_table.get(id, None)

    @classmethod
    def assign_interrupt(self, func, id, run_every=-1, is_periodic=True):
        timer = None
        if run_every != -1:
            timer = threading.Thread(target=func)
        else:
            timer = self.RepeatTimer(run_every, func)
        self.interrupts_table[id] = timer
        timer.start()
        return id

    @classmethod
    def destroy_interrupt(self, id):
        timer = self.interrupts_table.get(id)
        if timer:
            timer.cancel()
            del timer
            return True
        else:
            return False

class LibraryAssembly:
    libraries = {}
    included = {}
    library_namespace = {}

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
    raise_exception_traceback = 1
    show_dmesg_output = 1

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
        exec('import ' + name, custom_globals)
        return custom_globals[name]

    def supports_lib(name):
        return name in SystemLib.supported_libraries

    @classmethod
    def import_lib(self, name, add_supported=True):
        if self.supports_lib(name):
            return (True, None)
        try:
            __import__(name)
            if add_supported:
                SystemLib.supported_libraries[name] = True
            return (True, None)
        except ImportError as e:
            return (False, e)
        except Exception as e:
            return (False, e)

class Kernel:
    logs = []
    compilation_headers = []
    timestamp_started = -1.0
    persistent_state = {'updated': None}

    @classmethod
    def log(self, x, end='\n', store=True):
        print(x, end=end)
        if store:
            self.logs.append([x, end])

    @classmethod
    def reboot(self):
        self.log('Reboot is not implemented on this system! Exiting..')

    @classmethod
    def exit(self):
        if SystemLib.supports_lib('sys'):
            import sys
            sys.exit()
        exit()

class Info:

    def get_header():
        return 'Running ' + BaseSystem.name + ' ' + str(BaseSystem.version) + '.' + str(BaseSystem.subversion) + ' ' + BaseSystem.vposix + ' in ' + BaseSystem.subsystem + ' Subsystem'

def log(x, end='\n', store=True):
    Kernel.log(x, end, store)

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
    system_type = 'linux/unix'

class BaseSystemInterface:
    msg = Info.get_header()
    prefix = '$:'

    class BlankTermInput(Exception):
        pass

    class Commands:
        commands = {'author', 'echo', 'posix_exit', 'help', 'exit_system', 'exit', 'dmesg', 'uptime', 'clear', 'debug_prog', 'setflag', 'enabletraceback'}
        commands.add('hwservice')
        commands.add('reboot')

        class HWService:
            hw_service_list = {'info', 'help'}

        def reboot(self, input):
            Kernel.reboot()

        def hwservice(self, input):
            input = input.split()[1:]
            cmd = ''
            if len(input) == 0:
                cmd = 'help'
            else:
                cmd = input[0]
            if cmd not in self.HWService.hw_service_list:
                cmd = 'help'
            if cmd == 'help':
                print('Usage: hwservice\n Hardware service for UIX.')
            elif cmd == 'info':
                print('Hardware service info:\nCPU Count:{} \nCPU Frequency :{}\n'.format(Hardware.cpu_count, Hardware.cpu_freq))
                print('Commands: {}'.format(', '.join(self.HWService.hw_service_list)))

        def enabletraceback(self, input):
            self.setflag(self=self, input='setflag raise_exception_traceback=1')

        def setflag(self, input):
            msg = 'setflag: Set a sysflag\nUsage:\n setflag {flag}={value}'
            input = input.split(' ')[1:]
            if len(input) != 1:
                print(msg)
                return
            split_input = input[0].split('=', 1)
            if len(split_input) != 2:
                print(msg)
                return
            if getattr(Flags, split_input[0], None) == None:
                print('The flag `{}` does not exist.'.format(split_input[0]))
            setattr(Flags, split_input[0], split_input[1])

        def debug_prog(self, input):
            print(ProgramAssembly.programs)

        def clear(self, input):
            POSIX.clear_term()

        def uptime(self, input):
            if not SystemLib.supports_lib('time'):
                print('This system does not include the `time` library, no time support.')
                return
            if not SystemLib.supports_lib('lwdatetime'):
                print('Please compile UIXKernel with the included `lwdatetime` library for datetime support.')
                return
            import time
            if hasattr(time, 'time') == False:
                print('Time function lacks .time() property, can not capture time.')
                return
            lwdatetime = SystemLib.resolve_lib('lwdatetime')
            cur_time = time.time()
            print(lwdatetime.get_time_difference(cur_time, Kernel.timestamp_started, ['days', 'hours', 'minutes', 'seconds']))

        def dmesg(self, input):
            for log in Kernel.logs:
                print(log[0], end=log[1])

        def exit(self, input=None):
            self.exit_system(input)

        def exit_system(self, input=None):
            POSIX.exit_system()

        def author(self, input):
            print(BaseSystem.author)

        def echo(self, input):
            print(input[5:])

        def posix_exit(self, input):
            POSIX.exit_program()

        def help(self, input):
            print('{}: Available commands'.format(BaseSystem.name))
            print(', '.join(self.commands))
            print()
            print('Available programs')
            print(', '.join(ProgramAssembly.get_all_programs()))

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
        print(self.msg + ' on ' + str(CompatFlags.system_type))
        suffix_word = ''
        if ProgramAssembly.program_count != 1:
            suffix_word = 's'
        print('{} program{} on system.'.format(ProgramAssembly.program_count, suffix_word))
        print('Type `help` for help.')
        while True:
            try:
                user_input = input(self.prefix + ' ')
                args = user_input.split(' ')
                if args == ['']:
                    raise self.BlankTermInput
                command = args[0]
                command_method = self.get_command(command)
                is_packaged_program = command in ProgramAssembly.programs
                if command_method:
                    command_method(self.Commands, user_input)
                elif is_packaged_program:
                    return (command, command)
                else:
                    print('{}: unknown command or program `{}`'.format(BaseSystem.prefix, command))
            except self.BlankTermInput:
                pass

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
        print('\x1bc', end='')

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
    Kernel.exit()

def test_exec(code):
    try:
        exec(code)
        return True
    except Exception:
        return False
insignia = '###########\n###### ####\n###### ####\n#####  ####\n#      ####\n###     ###\n####      #\n####  #####\n#### ######\n#### ######\n###########'

def print_insignia():
    for line in insignia.split('\n'):
        lookup = {'#': '#='}
        msg = ''
        for char in line:
            char = lookup.get(char, char * 2)
            msg += char
        print(msg)
print_insignia()
log('\n' + Info.get_header())
log('Checking if this system has `exec` capabilities..')
if test_exec('') == False:
    log('`exec` required for system! Fail!')
    call_exit()
log('Decoding libraries.. ')
for library_name, library in LibraryAssembly.libraries.items():
    custom_globals = {}
    library_code = base64.b64decode(library) + '\n{} = {}'.format(library_name, library_name).encode()
    exec(library_code, custom_globals)
    if custom_globals[library_name]:
        LibraryAssembly.library_namespace[library_name] = custom_globals[library_name]
        LibraryAssembly.libraries[library_name] = True
        SystemLib.supported_libraries[library_name] = True
    else:
        del LibraryAssembly.libraries[library_name]
log('Decoding programs..')
for program_name, program in ProgramAssembly.programs.items():
    ProgramAssembly.programs[program_name] = base64.b64decode(program)

def run_lib_check():
    check_lib = ['os', 'sys', 'math', 'time', 'random', 'signal', 'threading', 'cmath', 'ast', 'zlib', 'traceback', 'gc']
    for lib in check_lib:
        log('Checking if `' + lib + '` is available.. ', end='')
        success, error = SystemLib.import_lib(lib)
        if success:
            log('OK')
        else:
            log('FALSE')
    log('Supported libraries: ' + ', '.join(SystemLib.get_supported()))
run_lib_check()
log('Starting VPOSIX runtime..')
checks = CompatibilityUnits.get_all_checks()
if len(checks) > 0:
    log('Using compatibility checks compiled for: ' + ', '.join(checks))
    for check in checks:
        code = CompatibilityUnits.get_code_check(check)
        custom_locals = {'modified': False}
        if not code:
            continue
        exec(code, globals(), custom_locals)
        if custom_locals['modified']:
            print('Modification occured.')
        print('Attempted check `{}` (stat: {})'.format(check, custom_locals['modified']))
del checks
patches = CompatibilityUnits.get_all_patches()
if len(patches) > 0:
    log('Applying compatibility patches in sequential order: ' + ', '.join(patches))
    for patch in patches:
        code = CompatibilityUnits.get_code_patch(patch)
        custom_locals = {}
        exec(code, globals(), custom_locals)
del patches
if SystemLib.supports_lib('time'):
    import time
    if hasattr(time, 'time'):
        Kernel.timestamp_started = time.time()
log('Capturing state..')
clear_terminal = False
POSIX.Interpreter.capture_variable()
log('Starting loop..\n')
while True:
    try:
        POSIX.ProgramState.set_default_interface()
        if clear_terminal:
            POSIX.clear_term()
        exec_name, exec_program = BaseSystemInterface.run()
        POSIX.ProgramState.alter_interface(exec_name)
        program_locals = {}
        program_globals = {'os': os}
        exec(ProgramAssembly.programs[exec_name], program_locals, program_globals)
    except KeyboardInterrupt:
        active_program = POSIX.ProgramState.active_program
        if active_program == 'bsi':
            print('\nExiting system..')
            call_exit()
        else:
            print('\nExiting program..')
            POSIX.Interpreter.restore_variable()
    except POSIX.Interrupts.ProgramExit:
        active_program = POSIX.ProgramState.active_program
        if active_program == 'bsi':
            print('Received POSIX exit program signal from Base System Interface. This is not supported. Restarting interpreter..')
        POSIX.Interpreter.restore_variable()
    except POSIX.SystemInterrupts.ExitSystem:
        call_exit()
    except Exception as e:
        active_program = POSIX.ProgramState.active_program
        is_running_program = True
        if active_program == 'bsi':
            is_running_program = False
        if is_running_program or True:
            print('\n' + '-' * 20)
            print('{}: Error. Program `{}` encountered an exception while running, and must exit. '.format(BaseSystem.prefix, active_program))
            print('Exception: {}'.format(type(e).__name__))
            if SystemLib.supports_lib('traceback'):
                import traceback
                traceback.print_exc()
            elif Flags.raise_exception_traceback == 1:
                raise e
            else:
                print('No traceback available on this system.')
            clear_terminal = False
            print('-' * 20)
            POSIX.Interpreter.restore_variable()
            continue
    clear_terminal = True