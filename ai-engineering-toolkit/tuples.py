#Tuple: ordered, immutable, allows duplicate elements


mytuple = ("max", 23, "Boston"
           )

print(mytuple)

mytuple = "max", 23, "Boston"


print(mytuple)

mytuple = ("max")

print(mytuple)

mytuple = ("max",)

print(mytuple)

mytuple = tuple(["max", 32, 'boston'])

print(mytuple)

item = mytuple[0]
print(item)

#mytuple[4] = 5 >>>> raise error as tupple ar not mutable

for i in mytuple:
    print(i, end="")

if "max" in mytuple:
    print('\nyes')
else:
    print('no')

mytuple1 = ('a','b','c','d','f','p','p')

print(len(mytuple1))
print(mytuple1.count('p'))

print(mytuple1.index('p'))

my_list = list(mytuple1)
print(my_list)

mytuple2 = tuple(my_list)
print(mytuple2)


a = (1,2,3,4,5,6,6,7,8)




b= a[2:5]

print(b)


print(a[::3])
print(a[::3])
print(a[::1])

mytuple = 'max', 33, 'boston'

name, age, city = mytuple
print(name,age,city)

mytp = (1,2,3,4,5,6,6,7)
i1,*i2,i3 = mytp
print(i1, i3,i2)




import sys


list11 = [1,3,4,5,'hello', 3,5, True]
tuple11 = (1,3,4,5,'hello', 3,5, True)
print(sys.getsizeof(list11), 'bytes')
print(sys.getsizeof(tuple11), 'bytes')


import timeit

print(timeit.timeit(stmt="[1,2,3,4,5,6,7,8]", number=1_000_000))
print(timeit.timeit(stmt="(1,2,3,4,5,6,7,8)", number=1_000_000))