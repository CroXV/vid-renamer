import sys


class ExitProgram:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value.upper() == 'Q':
            print('Exiting Program...')
            sys.exit()
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
