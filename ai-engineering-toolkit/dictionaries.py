#Dictionary: Key/value pairs, Unsorted, and Mutable.

mydict = {
  "name": "Max",
  "age": 36,
  "city": "San Francisco"
}

print(mydict)

mydict2 = dict(name="Marry", age=2, city='san')

print(mydict2)

value = mydict2['age']
print(value)

mydict2['email'] = "mhafha@hgamfa.com"

print(mydict2)

del mydict2['email']
print(mydict2)

mydict2.pop('name')
print(mydict2)

mydict2.popitem()
print(mydict2)

if 'name' in mydict:
    print(mydict['name'])


try:
    print(mydict['namme'])
except:
    print('Error')


for key,value in mydict.items():
    print(key, 'has a ', value)


mydict3 = {"name":"MAX", "age":23, "city":"New York"}
print(mydict3)

mydict3cpy = mydict3

print(mydict3cpy)
mydict3cpy['email'] = 'max@example.com'

mydict3cpy = mydict3
print(mydict3cpy)
print(mydict3)

mydict4cpy = mydict3.copy()
mydict4cpy['copy'] = 'copymethod'
print(mydict4cpy)
print(mydict3)


mydict4cpy = dict(mydict3)
mydict4cpy['dict'] = 'dict'
print(mydict4cpy)
print(mydict3)

mydict4cpy.update(mydict3)
print(mydict4cpy, 'update')

mydict4cpy = {3: 9, 6:36, 9:81}
print(mydict4cpy)

value = mydict4cpy[3]
print(value)


mytuple = (3, 5)
mydict = {mytuple: 13}
print(mydict)