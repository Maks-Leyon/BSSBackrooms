import sys
import os
c = [1]
b = [2,3]
c.extend(b)
print(c)
print(b)
print(c[0])
print(c[1])

print(sys.path.insert(0, os.path.abspath('../../')))

print(sys.path)