import random

import secrets
import numpy as np
#reproducibal
random.seed(1)


a = random.random()
print(a)

a = random.uniform(1, 10)
print(a)

a = random.randint(1, 10)
print(a)

a = random.randrange(1, 10)
print(a)

a = random.normalvariate(0, 1)
print(a)

mylist = list("AAABAAAACDEF"
              )
print(mylist)
a = random.choice(mylist)
print(a)

a = random.sample(mylist, 3)
print(a)

a = random.choices(mylist, k=3)
print(a)
a = mylist
random.shuffle(a)
print(a)

random.seed(1)
print(random.random())
print(random.randint(1, 10))

random.seed(0)
print(random.random())
print(random.randint(1, 10))

random.seed(2)
print(random.random())
print(random.randint(1, 10))

random.seed(3)
print(random.random())
print(random.randint(1, 10))


#secrets
print('random secrets')

a = secrets.randbelow(10)
print(a)

a = secrets.randbits(4)
print(a)

a = secrets.randbits(2)
print(a)

print(mylist)
#a = secrets.choices(mylist)
print(a)

a = np.random.rand(3)
print(a)

a = np.random.rand(3, 3)
print(a)

a = np.random.randint(0, 10, 3)
print(a)

a = np.random.randint(0, 10, (3,4))
print(a)

arr = np.array([[1, 0, 7, 7],
 [4, 7, 2, 4],
 [6, 2, 8, 9]])

print(arr)

np.random.shuffle(arr)
print(arr)


np.random.seed(1)

print(np.random.rand(3,3))

