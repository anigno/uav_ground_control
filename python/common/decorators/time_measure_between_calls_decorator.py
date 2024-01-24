import time

def time_measure_between_calls_decorator(func):
    """measure time between calls of a function"""
    functions_dict = {}

    def wrapper(*args, **kwargs):
        t = time.process_time()
        if func.__name__ in functions_dict:
            print(func.__name__, t - functions_dict[func.__name__], 'from last call')
        functions_dict[func.__name__] = t
        ret = func(*args, **kwargs)
        return ret

    return wrapper
