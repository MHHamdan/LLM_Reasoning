#Strings: ordered, immutable, text representation

string = 'home land'
print(string)

string = 'hom\'e land'
print(string)

string = """home land
yes"""
print(string)

string = """home land \
yes"""
print(string)

char = string[0]
print(char)

char = string[-1]
print(char)

substring = string[0:4]
print(substring)

substring = string[:4]
print(substring)

substring = string[:]
print(substring)

substring = string[::1]
print(substring)

substring = string[::2]
print(substring)

substring = string[::-1]
print(substring)

string2 = "Canada"

sentence = string + " "+ string2

print(sentence)


for i in string:
    print(i, end=' ')

if 'e' in string:
    print('\nyes')

else:
    print('no')

mystring = '   Hellow World   '
print(mystring)

mystring1 = mystring.strip()
print(mystring1)

print(mystring)


print(mystring.upper() + mystring.lower() + mystring)

print(mystring.startswith('H'))

print(mystring.find('H'))

print(mystring.find('hdlfs'))

print(mystring.count('lsdfjfls'))

print(mystring.replace('World', 'Universe'))

mystring3 = "How, are, you, doing"
print(mystring3)
my_list = mystring3.split(",")
print(my_list)

new_string = '-'.join(my_list)
print(new_string)


from timeit import default_timer as timer
list3 = ['a'] * 1000000
#print(list3)

start = timer()
mystring3 = ''
for i in list3:
    mystring3 += i
stop = timer()
t = (stop-start)

print( '  this takes a ', t , 'mmsec')

start1 = timer()
mystring3 = ''.join(list3)
stop1 = timer()
t1= (stop1-start1)
print( '  this takes a ', t1 , 'mmsec')



#% , .format(), f-string,

var = "Tom"
string = "The variable is %s" %var
print(string)

var = 333
string = "The variable is %d" %var
print(string)

var = 333.43235
string = "The variable is %f" %var
print(string)

var = 333.43235
string = "The variable is %.2f" %var
print(string)


var = 333.43235
string = "The variable is {}".format(var)
print(string)


var = 333.43235
string = "The variable is {:.2f}".format(var)
print(string)

var = 333.43235
var1 = 33
string = "The variable is {:.2f} and {}".format(var, var1)
print(string)


var = 333.43235
var1 = 33
string = f"The variable is {var} and {var1}"
print(string)

var = 333.43235
var1 = 33
string = f"The variable is {var*2} and {var1}"
print(string)
