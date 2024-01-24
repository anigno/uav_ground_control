def run_once_decorator(func):
    """run function one time only"""
    already_run = False

    def wrapper(*args, **kwargs):
        nonlocal already_run
        if not already_run:
            already_run = True
            return func(*args, **kwargs)

    return wrapper

if __name__ == '__main__':
    @run_once_decorator
    def my_func1():
        print('once1')

    @run_once_decorator
    def my_func2():
        print('once2')

    @run_once_decorator
    def my_func3():
        print('once3')

    my_func1()
    my_func2()
    my_func1()
    my_func2()
    my_func3()
    my_func3()
    my_func3()
    my_func1()
    my_func2()
