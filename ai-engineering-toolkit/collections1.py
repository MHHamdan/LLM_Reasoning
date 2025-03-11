#Collections: counters, nametuple, orderdict, defaultdict, deque


from collections import Counter

from collections import namedtuple
from collections import OrderedDict

from collections import defaultdict

from collections import deque

a = "aaabbbcccccccccccccccccccccccccccccc cc"

my_counter = Counter(a)

print(my_counter)
print(my_counter.keys())
print(my_counter.items())
print(my_counter.values())
print(my_counter)
print(my_counter.most_common(1))
print(my_counter.most_common(2))
print(my_counter.most_common(1)[0])
print(my_counter.most_common(1)[0][0])
print(my_counter.elements())
print(list(my_counter.elements()))


Point = namedtuple('Point', 'x,y ')
pt = Point(1, -4)
print(pt.x, pt.y)



ordered_dict = OrderedDict()

ordered_dict['f'] = 1
ordered_dict['b'] = 2
ordered_dict['c'] = 3
ordered_dict['d'] = 4
ordered_dict['e'] = 5
ordered_dict['a'] = 6

print(ordered_dict)

ordered_dict = {}

ordered_dict['f'] = 1
ordered_dict['b'] = 2
ordered_dict['c'] = 3
ordered_dict['d'] = 4
ordered_dict['e'] = 5
ordered_dict['a'] = 6

print(ordered_dict)

d = defaultdict(int)

d['a'] = 1
d['b'] = 2
d['c'] = 3

print(d)
print(d['b'])
print(d['t'])


d = deque()

d.append(1)
d.append(2)


print(d)

d.appendleft(44)
print(d)

print(d)

d.pop()
print(d)

d.extend([3,4,5,6,6])
print(d)

d.rotate(1)
print(d)

d.rotate(-1)
print(d)
