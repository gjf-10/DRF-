from django.test import TestCase

# Create your tests here.
class Empty:
    pass
class A:
    def __init__(self):
        self.name = "kevin"
a = A()
print(getattr(a, 'name'))