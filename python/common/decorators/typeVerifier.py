import inspect

def typeVerifierDecorator(func):
    """
    Decorator, verifies function's parameters values types and return type are as declared
    """

    def func_wrapper(*args, **kwargs):
        params_definitions = inspect.getfullargspec(func)
        annotations = params_definitions.annotations
        args_names = params_definitions.args

        expected_return_type = annotations.get('return', None)
        # prepare parameters dictionary from **kwargs and *args
        params = dict()
        for a in range(len(args)):
            params[args_names[a]] = args[a]
        params.update(**kwargs)
        # verify parameters types
        for key in params.keys():
            real_type = type(params[key])
            requested_type = annotations.get(key, None)
            if requested_type is None:
                continue
            if not issubclass(real_type, requested_type):
                raise Exception(f'Parameter type mismatch, function: [{func.__name__}], parameter: [{key}] expected: {requested_type} got: {real_type}')
        # call function and verify return type
        ret = func(*args, **kwargs)
        real_return_type = type(ret)
        if expected_return_type is not None and not issubclass(real_return_type, expected_return_type):
            raise Exception(f'Parameter type mismatch, function: [{func.__name__}], return type, expected: {expected_return_type} got: {real_return_type}')
        return ret

    return func_wrapper

if __name__ == '__main__':
    class Mydict(dict):
        pass

    @typeVerifierDecorator
    def myFunc(a: int, b: str, c, e: dict, d: Mydict) -> str:
        print(a, b, c, d, e)
        return 'aaa'

    val = myFunc(1, 'hello', 'qqq', e=Mydict({1: 1, 2: 2}), d=dict({3: 3, 4: 4}))
    print(val)
