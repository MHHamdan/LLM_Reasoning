import functools


#mydecorator : allow to add functions to existing functions
def start_end_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('Start')
        r = func(*args, **kwargs)
        print('End')
        return r
    return wrapper




@start_end_decorator
def print_name():
    print('Alex')
print_name()
print('print_name = start_end_decorator(print_name)')
#
@start_end_decorator
def print_name():
    print('Alex')

@start_end_decorator
def add5(x):
    return x+5

add5(10)

r = add5(23)
print(r)

print(help(add5))
print(add5.__name__)

def repeat(num_times):
    def dectorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return dectorator_repeat


@repeat(num_times=5)
def greet(name):
    print(f'Hello {name}')

greet('Mohammedhamdan')


def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}= {v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Callling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {result!r}")
        return result
    return wrapper

@debug
@start_end_decorator
def say_hello(name):
    greeting = f'Hello {name}'
    print(greeting)
    return greeting

print('multiple mydecorator to a function')

say_hello('Mohammedhamdan')


print('Class mydecorator' * 4)


class CountCalls:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0
    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f'This is excuted {self.num_calls} calls/times')
        return self.func(*args, **kwargs)

cc = CountCalls(None)

#cc()

@CountCalls
def hello():
    print('Hello')

hello()
hello()
hello()
hello()
