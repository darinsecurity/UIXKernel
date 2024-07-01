class OverrideSys:
    def __init__(self, original_sys=None, argv=None):
        self.original_sys = original_sys 
        if argv is None:
            argv = []
        self.argv = argv

    def __getattr__(self, name):
        if name == 'argv':
            return self.argv
        return getattr(self.original_sys, name)

    def __setattr__(self, name, value):
        if name in ('original_sys', 'argv'):
            object.__setattr__(self, name, value)
        else:
            setattr(self.original_sys, name, value)

    def __delattr__(self, name):
        if name in ('original_sys', 'argv'):
            object.__delattr__(self, name)
        else:
            delattr(self.original_sys, name)

    def __dir__(self):
        return dir(self.original_sys) + ['argv']