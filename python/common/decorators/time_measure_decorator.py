import time

def time_measure_decorator(func):
    """measure function run"""

    def func_wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        dif = end - start
        print(f'{func.__name__} {dif}s')
        return ret

    return func_wrapper

if __name__ == '__main__':
    @time_measure_decorator
    def measured_function():
        for i in range(1, 50):
            time.sleep(i / 1000)
        print('finished')

    @time_measure_decorator
    def other_measured_function(a, b, c):
        print('started', a, b, c)
        time.sleep(0.1)
        print('finished')
        return 'hello'

    measured_function()
    a1 = other_measured_function(1, b=2, c=3)
    print(a1)
