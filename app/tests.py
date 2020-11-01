from django.test import TestCase

# Create your tests here.
# 包装分配，wrapper_assignment
WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__',
                       '__annotations__')
WRAPPER_UPDATES = ('__dict__',)
def update_wrapper(wrapper,wrapped,assigned = WRAPPER_ASSIGNMENTS,updated = WRAPPER_UPDATES):
    for attr in assigned:
        try:
            print(attr,'0000')
            value = getattr(wrapped, attr)
            print(value,'111')
        except AttributeError:
            print("meiyougaishuxing ")
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        print(attr,'222222')
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    print(wrapper)
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper


class P():
    def __init__(self, k):
        self.name = k
    @classmethod
    def view(cls, k):
        print("我先来的")
        def vie():
            print("我来过吗？",cls)
            self = cls(k)
            print("vie 内部", self)
        vie.vie_class = cls
        vie.vie_initkwargs = k
        print(cls)
        print(vie.__dict__,"经过update_wrapper之前")
        p = update_wrapper(vie, cls,updated=())
        print(p.__dict__)
        return vie


class p1(P):
    @classmethod
    def view(cls):
        print(cls)  # <class '__main__.p1'>
        view = super().view('li')
        # view()4
        return view

class myP(p1):
    def get(self):
        print("你好")

p = myP.view()
    #
print(getattr(p, '__module__'))
# ('__dict__',)
# getattr(wrapped, attr, {})
from parse import parse

# print(parse("hello", "hello"))
# print('hello', 'hello')


