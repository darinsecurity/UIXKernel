import os
import base64
import builtins

class BaseSystem:
    version = '1.1.1'
    subversion = ''
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

    @classmethod
    def init(self):
        pass

class Interrupts:
    interrupts_table = {}

    @classmethod
    def retrieve_interrupt(self, id):
        pass

    @classmethod
    def assign_interrupt(self, func, run_every, is_periodic, id):
        pass

    @classmethod
    def destroy_interrupt(self, id):
        pass

class LibraryAssembly:
    libraries = {}
    included = {}
    library_namespace = {}

class ProgramAssembly:
    programs = {}
    program_count = 0

    @classmethod
    def get_all_programs(self):
        l = []
        for k, v in self.programs.items():
            l.append(k)
        return l

class Flags:
    raise_exception_traceback = 0
    show_dmesg_output = 1

class SystemLib:
    supported_libraries = {}
    override_imports = {}
    _original_import_method = None

    @classmethod
    def _import_lib_h(self, name, *args, **kwargs):
        if self.override_imports.get(name, None):
            return self.override_imports[name]
        return self._original_import_method(name, *args, **kwargs)

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
    def import_host_lib(self, name, add_supported=True):
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
    persistent_state['usefs'] = True
    persistent_state['fsformat'] = None
    persistent_state['loc'] = '/kernel/kernel.cfg'

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
Hardware.init()
SystemLib._original_import_method = builtins.__import__
builtins.__import__ = SystemLib._import_lib_h

class FileSystem:
    filesystem_available = False

    @classmethod
    def init(self):
        Kernel.log('Finished os initialization!')
        pass

class Info:

    def get_header():
        return 'Running ' + BaseSystem.name + ' ' + str(BaseSystem.version) + ' ' + BaseSystem.vposix + ' in ' + BaseSystem.subsystem + ' Subsystem'

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
    prefix = '#'
    current_working_dir = '/'

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
                cmd = 'info'
            if cmd == 'info':
                print('Hardware service info:\nCPU Count: {}\nCPU Frequency :{}\n'.format(Hardware.cpu_count, Hardware.cpu_freq))
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
    def display_init_msg(self):
        print(self.msg + ' on ' + str(CompatFlags.system_type))
        suffix_word = ''
        if ProgramAssembly.program_count != 1:
            suffix_word = 's'
        print('{} program{} on system.'.format(ProgramAssembly.program_count, suffix_word))
        print('Type `help` for help.')

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
        suffix_word = ''
        if ProgramAssembly.program_count != 1:
            suffix_word = 's'
        while True:
            try:
                additional_prefix = ''
                additional_prefix = os.getcwd()
                user_input = input('({}) {}:{} '.format(self.prefix, BaseSystem.prefix, additional_prefix))
                args = user_input.split(' ')
                if args == ['']:
                    raise self.BlankTermInput
                command = args[0]
                command_method = self.get_command(command)
                is_packaged_program = command in ProgramAssembly.programs
                if command_method:
                    command_method(self.Commands, user_input)
                elif is_packaged_program:
                    return (command, command, args)
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
LibraryAssembly.libraries['lwdatetime'] = "class lwdatetime:\n\n    def get_time_difference(timestamp1, timestamp2, units):\n        if timestamp1 > timestamp2:\n            timestamp1, timestamp2 = (timestamp2, timestamp1)\n        total_seconds = timestamp2 - timestamp1\n        time_units = {'years': 31536000, 'days': 86400, 'hours': 3600, 'minutes': 60, 'seconds': 1}\n        result = {}\n        for unit in units:\n            if unit in time_units:\n                unit_value = time_units[unit]\n                result[unit] = total_seconds // unit_value\n                total_seconds %= unit_value\n        return 'The system has been up for ' + ', '.join([unit + ': ' + str(int(result[unit])) for unit in units])"
LibraryAssembly.included['lwdatetime'] = True
ProgramAssembly.programs['tictactoe'] = 'board = [\'-\', \'-\', \'-\', \'-\', \'-\', \'-\', \'-\', \'-\', \'-\']\ngame_on = True\ncurrent_player = \'X\'\n\ndef display_board():\n    print(board[0] + \' | \' + board[1] + \' | \' + board[2] + \'      \' + \'1|2|3\')\n    print(board[3] + \' | \' + board[4] + \' | \' + board[5] + \'      \' + \'4|5|6\')\n    print(board[6] + \' | \' + board[7] + \' | \' + board[8] + \'      \' + \'7|8|9\')\n\ndef players():\n    print(\'Select Player - X or O\')\n    p1 = input(\'Player1: \')\n    p2 = \'\'\n    if p1 == \'X\':\n        p2 = \'O\'\n        print(\'Player2: \' + p2)\n    elif p1 == \'O\':\n        p2 = \'X\'\n        print(\'Player2: \' + p2)\n    elif p1 != \'O\' or p1 != \'X\':\n        print(\'Sorry,invalid input. Type X or O\')\n        play_game()\n\ndef player_position():\n    global current_player\n    print(\'Current Player: \' + current_player)\n    position = input(\'Choose position from 1 - 9: \')\n    valid = False\n    while not valid:\n        while position not in [\'1\', \'2\', \'3\', \'4\', \'5\', \'6\', \'7\', \'8\', \'9\']:\n            position = input(\'Choose position from 1 - 9: \')\n        position = int(position) - 1\n        if board[position] == \'-\':\n            valid = True\n        else:\n            print(\'Position already selected, choose another position!\')\n    board[position] = current_player\n    display_board()\n\ndef play_game():\n    print(\'My Tic Tac Toe Game\')\n    display_board()\n    players()\n    while game_on:\n        player_position()\n\n        def check_winner():\n            global game_on\n            if board[0] == board[1] == board[2] != \'-\':\n                game_on = False\n                print(\'Congratulations \' + board[0] + \' you WON!\')\n            elif board[3] == board[4] == board[5] != \'-\':\n                game_on = False\n                print(\'Congratulations \' + board[3] + \' you WON!\')\n            elif board[6] == board[7] == board[8] != \'-\':\n                game_on = False\n                print(\'Congratulations \' + board[6] + \' you WON!\')\n            elif board[0] == board[3] == board[6] != \'-\':\n                game_on = False\n                print(\'Congratulations \' + board[0] + \' you WON!\')\n            elif board[1] == board[4] == board[7] != \'-\':\n                game_on = False\n                print(\'Congratulations \' + board[1] + \' you WON!\')\n            elif board[2] == board[5] == board[8] != \'-\':\n                game_on = False\n                print(\'Congratulations \' + board[2] + \' you WON!\')\n            elif board[0] == board[4] == board[8] != \'-\':\n                game_on = False\n                print(\'Congratulations \' + board[0] + \' you WON!\')\n            elif board[2] == board[4] == board[6] != \'-\':\n                game_on = False\n                print(\'Congratulations \' + board[6] + \' you WON!\')\n            elif \'-\' not in board:\n                game_on = False\n                print("It\'s a Tie")\n                exit()\n\n        def flip_player():\n            global current_player\n            if current_player == \'X\':\n                current_player = \'O\'\n            else:\n                current_player = \'X\'\n        flip_player()\n        check_winner()\nplay_game()'
ProgramAssembly.programs['guessthenumber'] = "import random\nwhile True:\n    print('Can you guess the number? The number is between 1 and 100.')\n    guess_count = 0\n    actual_number = random.randint(1, 100)\n    user_number = 0\n    while user_number != actual_number:\n        user_input = input('> ')\n        try:\n            user_number = int(user_input)\n        except Exception as e:\n            print('Please provide a valid number. ')\n            continue\n        if user_number == actual_number:\n            print('You guessed the number! It was {}.'.format(user_number))\n            break\n        else:\n            print('Try again! The number is ', end='')\n            if user_number > actual_number:\n                print('smaller.')\n            else:\n                print('bigger.')\n    play_again = input('Play again? (Y/N)')\n    if play_again != 'Y':\n        break"
ProgramAssembly.programs['lineq'] = "def get_coordinates():\n    x1, y1 = map(float, input('Enter the first point (x1 y1): ').split())\n    x2, y2 = map(float, input('Enter the second point (x2 y2): ').split())\n    return ((x1, y1), (x2, y2))\n\ndef calculate_slope_intercept(point1, point2):\n    x1, y1 = point1\n    x2, y2 = point2\n    if x1 == x2:\n        raise ValueError('The two points must have different x-coordinates for a non-vertical line.')\n    m = (y2 - y1) / (x2 - x1)\n    b = y1 - m * x1\n    return (m, b)\n\ndef main():\n    while True:\n        point1, point2 = get_coordinates()\n        try:\n            m, b = calculate_slope_intercept(point1, point2)\n            if b >= 0:\n                print('The equation of the line is: y = {:.2f}x + {:.2f}'.format(m, b))\n            else:\n                print('The equation of the line is: y = {:.2f}x - {:.2f}'.format(m, abs(b)))\n        except ValueError as e:\n            print(e)\n        if input('Try again? (Y/N): ').upper() != 'Y':\n            break\nmain()"
ProgramAssembly.programs['pycoremark'] = "import time\n\ndef get_tick():\n    try:\n        return time.perf_counter()\n    except Exception as e:\n        return time.ticks_ms() / 1000\nprint('Running PyCoreMark')\nstart = get_tick()\nx = 1\nfor _ in range(100):\n    x += 1\nbasic_loop_performance = get_tick() - start\nstart = get_tick()\nx = ''\nfor _ in range(100):\n    x += 'a'\ndel x\nstring_add_performance = get_tick() - start\nstart = get_tick()\nfor _ in range(10):\n    x = []\n    for _ in range(100):\n        x.append('a' * 50)\n    for item in x:\n        del item\n    del x\nmem_alloc_performance = get_tick() - start\ntotal_score = 10 / (basic_loop_performance + string_add_performance + mem_alloc_performance)\nprint('Score: {}'.format(total_score))"
ProgramAssembly.programs['cd'] = "import os\nimport sys\nargs = sys.argv\nif len(args) == 1:\n    args.append('/')\nos.chdir(args[1])"
ProgramAssembly.programs['ls'] = "import os\nimport sys\nspecify_arg = ''\nif len(sys.argv) == 2:\n    specify_arg = sys.argv[1]\nuse_dir_func = False\nif use_dir_func == False:\n    print('  '.join(os.listdir(os.path.join(os.getcwd(), specify_arg))))\nelse:\n    print('  '.join(os.listdir(os.getcwd() + specify_arg)))"
ProgramAssembly.programs['cat'] = "import os\nimport sys\nif len(sys.argv) == 1:\n    while True:\n        try:\n            print(input())\n        except Exception as e:\n            break\nelse:\n    with open(sys.argv[1], 'r') as f:\n        print(f.read())"
ProgramAssembly.program_count = 8

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
    library_code = library
    exec(library_code, custom_globals)
    if custom_globals.get(library_name, False):
        LibraryAssembly.library_namespace[library_name] = custom_globals[library_name]
        LibraryAssembly.libraries[library_name] = True
        SystemLib.supported_libraries[library_name] = True
    else:
        del LibraryAssembly.libraries[library_name]
log('Decoding programs..')
for program_name, program in ProgramAssembly.programs.items():
    ProgramAssembly.programs[program_name] = program

def run_lib_check():
    check_lib = ['os', 'sys', 'math', 'time', 'random', 'signal', 'threading', 'cmath', 'ast', 'zlib', 'traceback', 'gc']
    for lib in check_lib:
        log('Checking if `' + lib + '` is available.. ', end='')
        success, error = SystemLib.import_host_lib(lib)
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
if SystemLib.supports_lib('gc'):
    import gc
    log('Freeing memory: ')
    CompatibilityUnits.checks_code.clear()
    CompatibilityUnits.checks_patches.clear()
    del insignia, run_lib_check, print_insignia
    gc.collect()
else:
    log('No garbage collector library, can not free memory')
log('Filesystem enabled!')
FileSystem.init()
log('Capturing state..')
clear_terminal = False
POSIX.Interpreter.capture_variable()
log('Starting loop..\n')
BaseSystemInterface.display_init_msg()
while True:
    try:
        POSIX.ProgramState.set_default_interface()
        exec_name, exec_program, exec_args = BaseSystemInterface.run()
        POSIX.ProgramState.alter_interface(exec_name)
        sys = __import__('sys')
        try:
            setattr(sys, 'argv', exec_args)
        except AttributeError:
            sys.argv = exec_args
        exec(ProgramAssembly.programs[exec_name])
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
            elif str(Flags.raise_exception_traceback) == '1':
                raise e
            else:
                print('No traceback available on this system.')
            clear_terminal = False
            print('-' * 20)
            POSIX.Interpreter.restore_variable()
            continue
    clear_terminal = True