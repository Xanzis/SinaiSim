import numpy as np 
import time
from definitions import *
# This imports all globals and functions from definitions. I jsut did this to save space 

"""
Case definition:
r1 Hits right without hitting circle
r2 Hits left without hitting circle
r3 Hits opposite without hitting circle, passing circle on left
r4 Hits opposite without hitting circle, passing circle on right
r5 Hits circle, comes back
r6 Hits circle, goes right
r7 Hits circle, goes left
r8 Hits circle, goes opposite

See definitons.py to view and edit the function boundaries, updates, etc.
"""

scale = 1000

case_lookup = np.zeros(shape=(scale, scale), dtype=np.int)

# case_lookup is a lookup table for which case a value is in.
# 'x' axis is position and 'y' axis is angle

for pos in range(scale):
	for ang in range(scale):
		for i in range(1, len(minmaxes) + 1):
			mnmx = minmaxes[i](pos/float(scale) - (np.pi / 2))
			if mnmx[0] < ang/float(scale) - 1 < mnmx[1]:
				case_lookup[pos, ang] = i