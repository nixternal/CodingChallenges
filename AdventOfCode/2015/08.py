#!/usr/bin/env python

# 1333
print("Part 1:", sum(len(s[:-1]) - len(eval(s)) for s in open('08.in')))

# 2046
print("Part 2:", sum(2 + s.count('\\') + s.count('"') for s in open('08.in')))
