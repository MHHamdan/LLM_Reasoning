#generate object inside the method >>> more efficient with a yield function
#Generators are memory efficient


import sys


def mygenerator():
    yield 1
    yield 2
    yield 3

g = mygenerator()
print(g)

# for i in g:
#     print(i)

#
# value = next(g)
# print(value)
# value = next(g)
# print(value)
# value = next(g)
# print(value)
# value = next(g)
# # print(value)
#
# print(sum(g))
print(sorted(g))


def countdown(num):
    print('Starting ')
    while num > 0:
        yield num
        num -= 1
cd = countdown(4)

value = next(cd)
print(value)
value = next(cd)
print(value)
value = next(cd)
print(value)
value = next(cd)
print(value)
# value = next(cd)
# print(value)


def firstn(n):
    nums = []
    num = 0

    while num < n:
        nums.append(num)
        num += 1
    return nums

mylist = firstn(10)
print(mylist)

mylist = sum(firstn(10))
print(mylist)

def firstn_generator(n):
    num = 0
    while num < n:
        yield num
        num +=1
print(sys.getsizeof(firstn(1000000)))
print(sum(firstn(10)
          ))
print(sys.getsizeof(firstn_generator(1000000)))
print(sum(firstn_generator(10)))

print('generator get the first elemnts on the fly')


def fibonacci(limit):
    # 0 , 1  then the sum of the previous two numbers
# 0 1 1 2 3 5 ..
    a,b = 0, 1

    while a < limit:
        yield a
        a, b = b, a + b

fib = fibonacci(30)

for i in fib:
    print(i, end=' ')

print('\nmygenerator set')
mygenerator = (i for i in range(100000) if i % 2 == 0)
print(sys.getsizeof(mygenerator), ' 22222 in set')
for i in mygenerator:
    print(i , end=' ')

print('\nmygenerator list')
mygenerator = [i for i in range(100000) if i % 2 == 0]
print(sys.getsizeof(mygenerator), ' 22222 in list')
for i in mygenerator:
    print(i , end=' ')

#print('\n', list(mygenerator))