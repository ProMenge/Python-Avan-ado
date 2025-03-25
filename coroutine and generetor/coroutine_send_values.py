def func():
  print('Part 1')
  
  x = yield
  
  print(x)
  print('Part 2')
  
  a=yield
  
  print(a)
  print('Part 3')
  
try:
  
  y = func()
  next(y)
  
  y.send(6)
  y.send(12)
  
except StopIteration as e:
  pass