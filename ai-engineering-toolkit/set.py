#sets: unordered, mutable, no duplicates

myset = {1, 2, 3, 5}

print(myset)

myset = {1, 1, 5, 6, 2, 3, 5}

print(myset)

myset = set("hello")
print(myset)
myset = set([1,4,5,6])
print(myset)

myset.add(454)
print(myset)

myset.remove(454)
print(myset)

myset.discard(432442)
print(myset)

myset.clear()
print(myset, 'clear')

myset = set([2,4,5,6])
print(myset)
myset.pop()
print(myset, 'pop')

print(myset)


for i in myset:
    print(i)

if 1 in myset:
    print('yes')


odds = {1, 2, 3, 5, 7}
evens = {0, 2, 4, 6}
primes = {2, 3, 5, 7}

u = odds.union(evens)
print(u)

i = odds.intersection(evens)
print(i)

i = odds.intersection(primes)
print(i)


i = evens.intersection(primes)
print(i)

diff = odds.difference(evens)
print(diff)

diff = evens.difference(odds)
print(diff)


symdiff = evens.symmetric_difference(odds)
print(symdiff)

#modify our set in place so we

evens.update(odds)
print(evens)

evens.difference_update(odds)
print(evens)

evens.symmetric_difference_update(odds)
print(evens)


print(evens.issubset(odds))
print(evens.issubset(primes))
print(evens.issuperset(odds))

print(evens.isdisjoint(odds))


evens = odds

print(evens)

evens.add(3243234)
print(evens)
print(odds)

evens = set(odds)

print(evens)

evens.add(10000000)
print(evens)
print(odds)


evens = odds.copy()

print(evens)

evens.add(8555555)
print(evens)
print(odds)


a = frozenset([1,2,3,4,5])

print(a)

