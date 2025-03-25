def func():
  print('Start')
  
  yield
  
  print('Middle')
  
  yield
  
  print('End')
  
try:
  y = func()
  print(type(y))
  next(y)
  next(y)
  next(y)

except StopIteration as e:
  pass