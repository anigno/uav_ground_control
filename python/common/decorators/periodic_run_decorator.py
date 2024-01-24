import asyncio
import threading
import time

from python.common.decorators.time_measure_between_calls_decorator import time_measure_between_calls_decorator

_periodic_run_loop = asyncio.get_event_loop()
_periodic_tasks = []

def periodic_run_decorator(interval: int):
    """Decorator for running periodic tasks, using asyncio main loop thread to run registered functions,tasks must not block!"""

    def internal(func):
        def wrapper_func(*args, **kwargs):
            t0 = time.process_time()
            ret = func(*args, **kwargs)
            t1 = time.process_time()
            next_delay = interval - (t1 - t0)
            if next_delay < 0:
                print('timeout', interval, next_delay)
            _periodic_run_loop.call_later(delay=next_delay, callback=wrapper_func)
            return ret

        _periodic_tasks.append(wrapper_func)
        return wrapper_func

    return internal

def _start():
    _periodic_run_loop.run_forever()

def start() -> threading.Thread:
    for t in _periodic_tasks:
        _periodic_run_loop.call_soon(t)
    thread = threading.Thread(target=_start)
    thread.start()
    return thread

def stop():
    _periodic_run_loop.stop()

if __name__ == '__main__':
    import math

    # @time_measure_function_decorator
    def do_work(number):
        for a in range(0, number):
            math.sqrt(a)

    @periodic_run_decorator(1)
    @time_measure_between_calls_decorator
    def worker_A1():
        do_work(100000)

    @periodic_run_decorator(1)
    @time_measure_between_calls_decorator
    def worker_A2():
        do_work(100000)

    @periodic_run_decorator(2)
    @time_measure_between_calls_decorator
    def worker_B():
        do_work(2000000)

    @periodic_run_decorator(3)
    @time_measure_between_calls_decorator
    def worker_C():
        do_work(100000)

    @periodic_run_decorator(4)
    @time_measure_between_calls_decorator
    def worker_D():
        do_work(100000)

    print('started')
    start()
    time.sleep(12)
    stop()
