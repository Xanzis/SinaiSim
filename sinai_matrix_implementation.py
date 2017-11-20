import numpy as np
from scipy import sparse
import scipy.sparse.linalg as linalg
import sys
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

SCALE = 1000

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
	return 2 * pos/float(SCALE) - 1

def loc_from_ang(ang):
	return np.pi * ang/float(SCALE) - np.pi/2

def pos_from_loc(loc):
	pos = int((SCALE/2.0)*(loc + 1)) # let's try this for now
	if 0 <= pos <= SCALE - 1:
		return pos
	return None
	print "loc during error: ", loc
	print "pos during error: ", pos
	raise ValueError("Index out of bounds on call of pos_from_loc")

def ang_from_loc(loc):
	ang = int((SCALE/np.pi)*(loc + np.pi/2)) # let's try this for now
	if 0 <= ang <= SCALE - 1:
		return ang
	return None
	print "loc during error: ", loc
	print "ang during error: ", ang
	raise ValueError("Index out of bounds on call of pos_from_loc")

def index_from_CASE_LOOKUP((pos,ang)):
	return SCALE * pos + ang

CASE_LOOKUP = np.empty(shape=(SCALE, SCALE), dtype=np.int)
CASE_LOOKUP.fill(-1)

# CASE_LOOKUP is a lookup table for which case a value is in.
# 'x' axis is position and 'y' axis is angle

if '-l' in sys.argv:
	print "Loading lookup table from file..."
	CASE_LOOKUP = np.load("CASE_LOOKUP.sn")
else:
	print "Loading lookup table..."
	st = time.time()
	print('|'.rjust(60))
	for pos in range(SCALE):
		for ang in range(SCALE):
			for i in range(len(minmaxes)): #i shifted keys in dictionary to make this nicer. maybe we should shift names of regions too?
				mnmx = minmaxes[i](loc_from_pos(pos))
				if mnmx[0] <= loc_from_ang(ang) <= mnmx[1]:
					#print "nifty"
					CASE_LOOKUP[pos, ang] = i
					break
		print('.'.rjust((60 * pos) / SCALE))
		sys.stdout.write("\033[F")
	CASE_LOOKUP.dump("CASE_LOOKUP.sn")
	print "Done in", time.time() - st, "s."

print "Loading P-F MATRIX..."
st = time.time()
print('|'.rjust(60))
PFMATRIX = sparse.eye(SCALE**2)
PFMATRIX = sparse.lil_matrix(PFMATRIX)
for pos in range(SCALE):
	for ang in range(SCALE):
		# In this situation, casenum is not the case number for the location in statespace we are calculating
		# rho for. Instead, it is the case numebr to be used for propagating back to the previous location,
		# namely, same position but negated angle.
		casenum = CASE_LOOKUP[pos, -ang]
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
			if refang != None and refpos != None: #@xander when does that happen?
				backcase = int(CASE_LOOKUP[refpos, refang])
				othercase = int(index_from_CASE_LOOKUP((pos, ang)))
				new = 1 / float(jacobians[backcase](*invrs))
				PFMATRIX[othercase, othercase] = 0
				PFMATRIX[othercase, index_from_CASE_LOOKUP((refpos, refang))] = new
			else:
				pass
				##print "broken"
		else:
			pass
			#print "broken"
			# check order of invrs[1] and 0 in the reference to current state. Right now we think current state
			# should be indexed by currentstate[angle, position]. Should be easy enough to check on.
		print('.'.rjust((60 * pos) / SCALE))
		sys.stdout.write("\033[F")

PFMATRIX = sparse.csr_matrix(PFMATRIX)
print "Done in", time.time() - st, "s."
print "Running..."

#print CASE_LOOKUP
#print 7 in CASE_LOOKUP

def rho(pos, ang):
	off = np.sqrt(pos **2 + ang **2)
	return np.cos(3 * off) / (1 + off **2)

class Distribution():

	def __init__(self, rho, current_state=None, steps_from_start=None):
		self.rho = rho
		if not steps_from_start:
			self.steps_from_start = 0
		else:
			self.steps_from_start = steps_from_start
		if not current_state:
			self.current_state = np.matrix([[rho(loc_from_pos(x), loc_from_ang(y)) for x in range(SCALE)] for y in range(SCALE)]).flatten().transpose()
		else:
			self.current_state = current_state
		# ^^ start distribution

	def update(self):
		self.current_state = PFMATRIX.dot(self.current_state)
		self.steps_from_start += 1

	def limit(self, iterations = 1000):
		for i in range(iterations):
			self.update()

	def display(self):
		showfig(self.__convert_to_matrix())


	def __convert_to_matrix(self):
		matrix = []
		for i in range(SCALE):
			matrix.append([float(i) for i in self.current_state[SCALE * i:SCALE * (i + 1)]])
		return np.array(matrix)

dist = Distribution(rho)


# That should do it. probably best to represent this with pyplot

showfig(CASE_LOOKUP)
"""
for i in range(len(minmaxes)):
	fig_rules = 5 * (CASE_LOOKUP == i)
	showfig(fig_rules, name=str(i)+"boundaries")
"""
doupdate = 1
dist.display()

while doupdate:
	dist.update()
	dist.display()
	doupdate = input("Update again? 1/0\n")
