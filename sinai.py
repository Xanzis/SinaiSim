import numpy as np 
import time
from definitions import *
from matplotlib import pyplot as plt
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

scale = 100

case_lookup = np.zeros(shape=(scale, scale), dtype=np.int)

# case_lookup is a lookup table for which case a value is in.
# 'x' axis is position and 'y' axis is angle

for pos in range(scale):
	for ang in range(scale):
		for i in range(1, len(minmaxes) + 1):
			mnmx = minmaxes[i](2 * pos/float(scale) - 1)
			if mnmx[0] <= np.pi * ang/float(scale) - np.pi/2 <= mnmx[1]:
				#print "nifty"
				case_lookup[pos, ang] = i

print case_lookup

def rho(pos, ang):
	return 1

start_dist = np.array([[rho(2 * x/float(scale) - 1, np.pi * y/float(scale) - (np.pi / 2)) for x in range(scale)] for y in range(scale)])
# starting distribution

new_dist = np.zeros(shape=(scale, scale))

for pos in range(scale):
	for ang in range(scale):
		casenum = case_lookup[pos, ang]
		loc = (2 * pos/float(scale) - 1, np.pi * ang/float(scale) - (np.pi/2))
		if casenum:
			invrs = inverses[casenum](*loc)
			new_dist[pos, ang] = rho(*invrs) / abs(jacobians[casenum](*loc))

# That should do it. probably best to represent this with pyplot

fig = plt.figure(figsize=(6, 3))

ax = fig.add_subplot(111)
ax.set_title('colorMap')
plt.imshow(case_lookup)
ax.set_aspect('equal')

cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
cax.get_xaxis().set_visible(False)
cax.get_yaxis().set_visible(False)
cax.patch.set_alpha(0)
cax.set_frame_on(False)
plt.colorbar(orientation='vertical')
plt.show()