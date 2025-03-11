#Lists: ordered, mutable, allows duplicate elements.

mylist = [1, 2, 3, 4, 'banana', 'burger', 'cherry', 'apple']

print(mylist)

mylist2 = [4, 5, 6, 6, 'apple', 'apple', True, False, True]

print(mylist2)

item = mylist2[-1]

print(item)

for i in mylist2:
    print(i, end=' ')

if 'banana' in mylist2:
    print('\nyes')
else:
    print('\nNo')


print(len(mylist), 'elements')

mylist.append(mylist2)
print(mylist)

mylist.extend(mylist2)
print(mylist)

mylist2.insert(0,'blueberry')
print(mylist2)

ritem = mylist2.pop()
print(ritem, mylist2)

print(mylist2)
rritem = mylist2.clear()
print(mylist2)
print(mylist)
reve = mylist.reverse()
print(reve)




mylist = [0] * 5
print(mylist
      )

mylist3 = [1,2,3,4,5]
new_list = mylist + mylist3
print(new_list
      )

a = new_list[1:]

print(a)

a = new_list[::2]

print(a)
a = new_list[::-1]

print(a)

list_org = ["banana", "burger", "apple"]

list_cpy = list_org
print(list_cpy)

list_cpy.append('lemmeon')

print(list_org )


list_cpy1 = list_org.copy()
list_cpy1.append('strewbot')

print(list_cpy1)
print(list_org )

list_cpy2 = list(list_org)
list_cpy2.append('fruits')

print(list_cpy2)
print(list_org )

list_cpy3 = list_org[:]
list_cpy3.append('vigitables')

print(list_cpy3)
print(list_org )


#list comperhension

mylista = [1, 2, 3,4,5,6]
b = [x * x for x in mylista]
print(mylista)
print(b)