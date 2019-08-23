import sys


class EmptyStringError(Exception):
    pass


class ValueConditions:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value.upper() == 'Q':
            print('\nClosing script...')
            sys.exit()
        elif value == '':
            raise EmptyStringError('Value is equal to an empty string.')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
