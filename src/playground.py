bar = 1

print(1 + 1 + (lambda x : 0 if  x == 1 else x + 1)(10))