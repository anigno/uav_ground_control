class NoInstanceMeta(type):
    def __call__(cls, *args, **kwargs):
        raise TypeError(f"Instances not allowed for class: {cls.__name__}")

if __name__ == '__main__':
    class SomeClass(metaclass=NoInstanceMeta):
        VAR = 'hello'

    # access without instance
    a = SomeClass.VAR
    try:
        # access with instance produces exception
        SomeClass().VAR
    except Exception as ex:
        print(ex)
