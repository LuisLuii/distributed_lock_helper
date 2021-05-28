from multipledispatch import dispatch

@dispatch(int, int)
def area(l, b):
  return l * b

@dispatch(int)
def area(r):
  import math
  return math.pi * r ** 2

@dispatch()
def area():
  return 'none'

print(area('True'))