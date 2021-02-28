#!/usr/bin/env python

# # #
# Exploration of how priority queue works
#

from queue import PriorityQueue

print("--- Study 1 ---")

pq1 = PriorityQueue()

for v in [1,10,5,3]:
    pq1.put(v)
    print(pq1.qsize())

print("size", pq1.qsize())

while not pq1.empty():
    v = pq1.get()
    print("Item", v)

# conclusion:
# Items will be retrieved in sorted ascending order

print("--- Study 2 ---")
print("priority queue with custom objects")

class Person(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # sufficient to make PriorityQueue work
    def __lt__(self, other):
        return self.age < other.age

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

    def __repr__(self):
        return "<{}: name={}, age={}>".format(self.__class__.__name__,
                                              self.name, self.age)

persons = [
    Person("Alex",    40),
    Person("Bob",     30),
    Person("Charlie", 10),
    Person("Dave",    15),
    Person("Eve",     10)
]

pq2 = PriorityQueue()

print("size", pq2.qsize())
#print("length", len(pq2)) # python sucks
for p in persons:
    pq2.put(p)
    print("size", pq2.qsize())

try:
    if persons[1] in pq2:
        print(persons[1], "exists in the queue")
except TypeError as e:
    print("Python sux:", e)

while not pq2.empty():
    p = pq2.get()
    print(p)

# Output will be:
#<Person: name=Charlie, age=10>
#<Person: name=Eve,     age=10>
#<Person: name=Dave,    age=15>
#<Person: name=Bob,     age=30>
#<Person: name=Alex,    age=40>

# Q: possible to define a method that the queue will use for comparing objects?
# Q: nope
