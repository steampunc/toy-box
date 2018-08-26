def josephus(n):
 loop = [i + 1 for i in range(n)]
 
 i = 0
 while loop.count(0) < n - 1:
  x = 1
  a = i+1
  while loop[a % n] == 0:
   x += 1 
   a = a + 1
  loop[(i+x) % n] = 0
  x = 1
  a = i+1
  while loop[a % n] == 0:
   x += 1 
   a = a + 1
  i = (i+x) % n
 return(loop[i])

responses = []
for i in range(1,1000):
 responses.append(josephus(i))
print(responses)
