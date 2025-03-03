import numpy as np
import time
from definitions import *
from matplotlib import pyplot as plt
import sys
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


case_lookup = np.empty(shape=(scale, scale), dtype=np.uint8)
case_lookup.fill(-1)

inva_lookup = np.empty(shape=(scale, scale))
inva_lookup.fill(-2)
invt_lookup = np.empty(shape=(scale, scale))
invt_lookup.fill(-2)

# case_lookup is a lookup table for which case a value is in.
# 'x' axis is position and 'y' axis is angle

st = time.time()

if '-l' in sys.argv:
	print "Loading lookup table from file..."
	case_lookup = np.load("case_lookup.sn")
	"""
	inva_lookup = np.load("inva_lookup.sn")
	invt_lookup = np.load("invt_lookup.sn")
	"""
else:
	print "Loading lookup table from scratch..."
	print('|'.rjust(60))
	for pos in range(scale):
		for ang in range(scale):
			for i in range(len(minmaxes)): #i shifted keys in dictionary to make this nicer. maybe we should shift names of regions too?
				mnmx = minmaxes[i](loc_from_pos(pos))
				if mnmx[0] <= loc_from_ang(ang) <= mnmx[1]:
					#print "nifty"
					case_lookup[pos, ang] = i
					break
		print('.'.rjust((60 * pos) / scale))
		sys.stdout.write("\033[F")
	case_lookup.dump("case_lookup.sn")
	print "case_lookup done."
	"""
	print "Loading inverses from scratch..."
	for pos in range(scale):
		for ang in range(scale):
			casenum = case_lookup[pos, -ang]
			if casenum != -1:
				loc = (loc_from_pos(pos), loc_from_ang(ang))
				invrs = updates[casenum](loc[0], - loc[1])
				invrs = (invrs[0], -invrs[1])
				inva_lookup[pos, ang] = invrs[0]
				invt_lookup[pos, ang] = invrs[1]
	print "inva_lookup and invt_lookup done."
	inva_lookup.dump("inva_lookup.sn")
	invt_lookup.dump("invt_lookup.sn")
	"""

print "Done after", time.time() - st, "s."
print "Running..."

#print case_lookup
#print 7 in case_lookup

def rho(pos, ang):
	return 1
	return (pos + 1) * (ang + np.pi / 2) / np.pi **2
	off = np.sqrt(pos **2 + ang **2)
	return np.cos(3 * off) / (1 + off **2)

class Distribution():

	def __init__(self, rho, current_state=None, steps_from_start=None):
		self.rho = rho
		if not steps_from_start:
			self.steps_from_start = 0
		else:
			self.steps_from_start = steps_from_start
		if current_state is None:
			self.current_state = np.array([[rho(loc_from_pos(y), loc_from_ang(x)) for x in range(scale)] for y in range(scale)])
		else:
			self.current_state = current_state
		# ^^ start distribution

	def update(self):
		st = time.time()
		new_distribution = np.zeros(shape=(scale, scale))
		print('|'.rjust(60))


		for pos in range(scale):
			for ang in range(scale):
				casenum = case_lookup[pos, -ang]
				check = False
				# In this situation, casenum is not the case number for the location in statespace we are calculating
				# rho for. Instead, it is the case numebr to be used for propagating back to the previous location,
				# namely, same position but negated angle.
				casenum = case_lookup[pos, -ang]
				if casenum in [7, 8]:
					check = True
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
						new_val = self.current_state[refang, refpos] / abs(jacobians[backcase](*invrs))
						if casenum in [7, 8] and new_val == 0:
							print "writing 0 for a region related to r8/r9"
							print "refang, refpos:", refang, refpos
							print "backcase:", backcase
							print "jacobian of backcase", abs(jacobians[backcase](*invrs))
							print "state at inverse:", self.current_state[refpos, refang]
						new_distribution[pos, ang] = new_val
					#else:
					#	print casenum, invrs, loc[0], -loc[1]
					#if check and new_distribution[]
					# check order of invrs[1] and 0 in the reference to current state. Right now we think current state
					# should be indexed by currentstate[angle, position]. Should be easy enough to check on.
			print('.'.rjust((60 * pos) / scale))
			sys.stdout.write("\033[F")

		self.steps_from_start += 1
		self.current_state = new_distribution
		print "Done updating after", time.time() - st, "s"

statefile = None
if len(sys.argv) - ('-l' in sys.argv) == 2:
	statefile = sys.argv[2]
	try:
		dist = Distribution(rho, current_state=np.load(statefile))
	except IOError:
		print "No file found under that name. Will create file and dump data after iterating."
		dist = Distribution(rho)
else:
	dist = Distribution(rho)


# That should do it. probably best to represent this with pyplot

"""
for i in range(len(minmaxes)):
	fig_rules = 5 * (case_lookup == i)
	showfig(fig_rules, name=str(i)+"boundaries")
"""
doupdate = 1

showfig(case_lookup)
showfig(dist.current_state)
while doupdate:
	print "Area (ish):", np.sum(dist.current_state)
	dist.update()
	if statefile:
		dist.current_state.dump(statefile)
	showfig(dist.current_state)
	doupdate = input("Update again? 1/0\n")

"""
for round in range(20):
	print "Round", round
	dist.update()
	if statefile:
		dist.current_state.dump(statefile)
"""
