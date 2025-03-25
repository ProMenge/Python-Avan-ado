def my_gen():
  n=1
  print('Primeiro print, n eh igual a {}'.format(n))
  
  yield n
  
  
  n+= 1
  print('segundo print, n eh igual a {}'.format(n))
  yield n
  
  
  n+=1
  print('Terceiro print, n eh igual a {}'.format(n))
  yield n
  
test = my_gen()
next(test)
next(test)
next(test)
next(test)