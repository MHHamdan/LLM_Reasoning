#itertools: product, permutation, combination, accumalte, groupby, and infinite iterators"
#

from itertools import product
from itertools import permutations
from itertools import combinations, combinations_with_replacement
from itertools import accumulate
from itertools import groupby
from itertools import count, cycle, repeat


import operator

a = [1, 2]
b = [3, 4]
c = [5]

prod = product(a,b)
print(prod)
print(list(prod))

prod = product(a,c, repeat= 2)
print(list(prod))

a = [1,2,3]
perm = permutations(a)
print(list(perm))

perm = permutations(a, 2)
print(list(perm))

perm = permutations(a, 3)
print(list(perm))

perm = permutations(a, 4)
print(list(perm))

a = [1,2,3,4]

comb = combinations(a, 2)
print(list(comb))

comb = combinations_with_replacement(a, 2)
print(list(comb))

acc = accumulate(a)
print(a)
print(list(acc))

acc = accumulate(a, func=operator.mul)
print(a)
print(list(acc))

a = [1,2,7,3,4]

acc = accumulate(a, func=max)
print(a)
print(list(acc))

def smaller_than3(x):
    return x< 3


group_obj = groupby(a, key=smaller_than3)

for key, value in group_obj:
    print(key, list(value))

group_obj = groupby(a, key=lambda x: x<3)

for key, value in group_obj:
    print(key, list(value))

persons = [{'name':'ss', 'age':1}, {'name':'bad', 'age':1},
           {'name':'bb', 'age':1},{'name':'test', 'age':22}]

group_obj = groupby(persons, key=lambda x: x['age'])

for key, value in group_obj:
    print(key, list(value))

for i in count(10):
    print(i, end=' ')
    if i ==100:
        break
a = [1, 2, 3]
c= 0
"""
for i in cycle(a):
    print(i)
    if i == 321:
        break
"""

for i in repeat(1, 4):
    print(i, end='')