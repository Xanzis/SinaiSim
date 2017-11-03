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
r8 Hits circle, goes opposite --> shouldn't this be split into hitting on
either side?

See definitons.py to view and edit the function boundaries, updates, etc.
"""

scale = 100

def loc_from_pos(pos):
	return 2 * pos/float(scale) - 1

def loc_from_ang(ang):
	return np.pi * ang/float(scale) - np.pi/2

def pos_from_loc(loc):
	pos = int((scale/2.0)*(loc + 1)) # let's try this for now
	if -1 <= pos <= 1:
		return pos
	raise ValueError("Index out of bounds on call of pos_from_loc")

def ang_from_loc(loc):
	ang = int((scale/np.pi)*(loc + np.pi/2)) # let's try this for now
	if -1 <= pos <= 1:
		return ang
	raise ValueError("Index out of bounds on call of pos_from_loc")


case_lookup = np.empty(shape=(scale, scale), dtype=np.int)
case_lookup.fill(5)

# case_lookup is a lookup table for which case a value is in.
# 'x' axis is position and 'y' axis is angle

for pos in range(scale):
	for ang in range(scale):
		for i in range(len(minmaxes)): #i shifted keys in dictionary to make this nicer. maybe we should shift names of regions too?
			mnmx = minmaxes[i](loc_from_pos(pos))
			if mnmx[0] <= loc_from_ang(ang) <= mnmx[1]:
				#print "nifty"
				case_lookup[pos, ang] = i
				break

print case_lookup

def rho(pos, ang):
	return 1

class Distribution():

	def __init__(self, rho, current_state=None, steps_from_start=None):
		self.rho = rho
		if not steps_from_start:
			self.steps_from_start = 0
		else:
			self.steps_from_start = steps_from_start
		if not current_state:
			self.current_state = np.array([[rho(loc_from_pos(x), loc_from_ang(y)) for x in range(scale)] for y in range(scale)])
		else:
			self.current_state = current_state
		# ^^ start distribution

	def update(self):
		"""okay so i just copied in your code here but i noticed that iterations
		of the distribution don't depend on the past state of the distribution
		which seems wrong? --> I think we need to match inverse points to the nearest
		point in the distribution, but I don't know if that'll preserve the one to one
		quality (almost definitely won't)"""
		new_distribution = np.zeros(shape=(scale, scale))

		for pos in range(scale):
			for ang in range(scale):
				casenum = case_lookup[pos, ang]
				loc = (loc_from_pos(pos), loc_from_ang(ang))
				if casenum != None: #why is this if statement here also casenum isn't boolean??
					invrs = inverses[casenum](*loc)
					new_distribution[pos, ang] = self.current_state[ang_from_loc(invrs[1], invrs[0])] / abs(jacobians[casenum](*loc))
					# check order of invrs[1] and 0 in the reference to current state. Right now we think current state
					# should be indexed by currentstate[angle, position]. Should be easy enough to check on.
		self.steps_from_start += 1
		self.current_state = new_distribution

dist = Distribution(rho, )

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

