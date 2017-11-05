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

scale = 200

def showfig(to_show, name='colorMap'):
	fig = plt.figure(figsize=(6, 3))

	ax = fig.add_subplot(111)
	ax.set_title(name)
	plt.imshow(to_show)
	ax.set_aspect('equal')

	cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
	cax.get_xaxis().set_visible(False)
	cax.get_yaxis().set_visible(False)
	cax.patch.set_alpha(0)
	cax.set_frame_on(False)
	plt.colorbar(orientation='vertical')
	plt.show()

def loc_from_pos(pos):
	return 2 * pos/float(scale) - 1

def loc_from_ang(ang):
	return np.pi * ang/float(scale) - np.pi/2

def pos_from_loc(loc):
	pos = int((scale/2.0)*(loc + 1)) # let's try this for now
	if 0 <= pos <= scale - 1:
		return pos
	return None
	print "loc during error: ", loc
	print "pos during error: ", pos
	raise ValueError("Index out of bounds on call of pos_from_loc")

def ang_from_loc(loc):
	ang = int((scale/np.pi)*(loc + np.pi/2)) # let's try this for now
	if 0 <= ang <= scale - 1:
		return ang
	return None
	print "loc during error: ", loc
	print "ang during error: ", ang
	raise ValueError("Index out of bounds on call of pos_from_loc")


case_lookup = np.empty(shape=(scale, scale), dtype=np.int)
case_lookup.fill(-1)

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
print 7 in case_lookup

def rho(pos, ang):
	return np.sin(5 * pos) + np.cos(6 * ang)

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
		new_distribution = np.zeros(shape=(scale, scale))

		for pos in range(scale):
			for ang in range(scale):
				# In this situation, casenum is not the case number for the location in statespace we are calculating
				# rho for. Instead, it is the case numebr to be used for propagating back to the previous location,
				# namely, same position but negated angle.
				casenum = case_lookup[pos, -ang]
				loc = (loc_from_pos(pos), loc_from_ang(ang)) # this is still correct location. loc[1] to be negated later.
				if casenum != -1:
					invrs = updates[casenum](loc[0], - loc[1])
					invrs = (invrs[0], -invrs[1])
					#if not -np.pi / 2 - 0.01 < invrs[1] < np.pi / 2 + 0.01:
					#	print "invrs: ", invrs
					#	print "casenum: ", casenum
					#	print "loc: ", loc
					refang = ang_from_loc(invrs[1])
					refpos = pos_from_loc(invrs[0]) 
					# Note: this relies on the fact that the inverse is the same as the update for negative theta.
					# This is useful because it saves having to find out the region the thing came from to get an inverse
					# So yeah this is fine. Also backcase is the case that the inverse is in.
					if refang != None and refpos != None:
						backcase = case_lookup[refpos, refang]
						new_distribution[pos, ang] = self.current_state[refang, refpos] / abs(jacobians[backcase](*invrs))
					# check order of invrs[1] and 0 in the reference to current state. Right now we think current state
					# should be indexed by currentstate[angle, position]. Should be easy enough to check on.
		self.steps_from_start += 1
		self.current_state = new_distribution

dist = Distribution(rho)


# That should do it. probably best to represent this with pyplot

showfig(case_lookup)
"""
for i in range(len(minmaxes)):
	fig_rules = 5 * (case_lookup == i)
	showfig(fig_rules, name=str(i)+"boundaries")
"""
doupdate = 1
showfig(dist.current_state)

while doupdate:
	dist.update()
	showfig(dist.current_state)
	doupdate = input("Update again? 1/0\n")

