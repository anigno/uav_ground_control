import os

class PrintableParams:
    @staticmethod
    def to_string(obj: object, is_multiline=False, header=''):
        line_break = os.linesep if is_multiline else ','
        s = f'{header}{os.linesep}'
        for k in obj.__dict__:
            s = s + f'{k}={str(obj.__dict__[k])}{line_break}'
        if not is_multiline:
            s = s[0:-1]
        return s

    @staticmethod
    def print(obj: object, is_multiline=False, header=''):
        print(PrintableParams.to_string(obj, is_multiline, header))

if __name__ == '__main__':
    class Class1:
        def __init__(self):
            self.a = 123
            self.b = {1: '111', 2: '222'}

    class Class2(Class1):
        def __init__(self):
            super().__init__()
            self.c = [1, 2, 3]

    c = Class2()
    PrintableParams.print(c)
    PrintableParams.print(c, True, 'some header')
