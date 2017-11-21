import numpy as np
from scipy import sparse
import scipy.sparse.linalg as linalg
import sys
import time
from definitions import *
from matplotlib import pyplot as plt
import random
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

SCALE = 500

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
	print "Loading P-F Matrix from file..."
	PFMATRIX = sparse.load_npz("PFMATRIX.npz")
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
	#sparse.save_npz("PFMATRIX.npz", PFMATRIX)
	print "Done in", time.time() - st, "s."
	print "Running..."

def rho(pos, ang):
	return 1.1 - random.random() / float(5)
	#return (pos + 1) * (ang + np.pi / 2) / np.pi **2
	# off = np.sqrt(pos **2 + ang **2)
	# return np.cos(3 * off) / (1 + off **2)

class Distribution():

	def __init__(self, rho=rho, current_state=None, steps_from_start=None):
		self.rho = rho
		if not steps_from_start:
			self.steps_from_start = 0
		else:
			self.steps_from_start = steps_from_start
		try:
			current_state[0]
			self.current_state = current_state  #start distribution
		except:
			self.current_state = np.matrix([[rho(loc_from_pos(x), loc_from_ang(y)) for x in range(SCALE)] for y in range(SCALE)]).flatten().transpose()


	def update(self, show_integral = True):
		self.current_state = PFMATRIX.dot(self.current_state)
		if show_integral:
			print self.integral()
		self.steps_from_start += 1

	def limit(self, iterations = 1000, integrate = False):
		for i in range(iterations):
			self.update(show_integral = integrate)

	def display(self):
		showfig(self.__convert_to_matrix())

	def __convert_to_matrix(self):
		matrix = []
		for i in range(SCALE):
			matrix.append([float(i) for i in self.current_state[SCALE * i:SCALE * (i + 1)]])
		return np.array(matrix)

	def integral(self):
		integral = 0
		try:
			for i in self.current_state:
				integral += (i[0]**2 + i[1]**2)**0.5 / float(SCALE**2)
		except:
			for i in self.current_state:
				integral += i / float(SCALE**2)
		return integral

	def smooth(self, k=0.5):
		new_state = [i for i in self.current_state]
		for i in range(len(self.current_state)):
			try:
				weights = 1
				try:
					new_state[i] += k*self.current_state[i - SCALE]
					weights += k
				except:
					pass
				try:
					new_state[i] += k*self.current_state[i + SCALE]
					weights += k
				except:
					pass
				if i%SCALE != 0:
					new_state[i] += k*self.current_state[i - 1]
					weights += k
					try:
						new_state[i] += k*self.current_state[i + SCALE - 1]
						weights += k
					except:
						pass
					try:
						new_state[i] += k*self.current_state[i - SCALE - 1]
						weights += k
					except:
						pass
				if i%SCALE != -1:
					new_state[i] += k*self.current_state[i + 1]
					weights += k
					try:
						new_state[i] += k*self.current_state[i + SCALE + 1]
						weights += k
					except:
						pass
					try:
						new_state[i] += k*self.current_state[i - SCALE + 1]
						weights += k
					except:
						pass
				new_state[i] /= float(weights)
			except:
				print ":(", i
		self.current_state = np.array(new_state)

dist = Distribution(rho)

# doupdate = 1
# # print dist.integral()
# # dist.display()
#
# while doupdate:
# 	dist.update()
# 	dist.display()
# 	doupdate = input("Update again? 1/0\n")

def invariant(start_pos):
	"""constructs an invariant distribution by backpropogating one point to setting
	rho values to jacobian. Should scale after but I haven't gotten to that"""
	invariant = np.zeros(SCALE**2)
	pos, ang = start_pos[0], start_pos[1]
	invariant[index_from_CASE_LOOKUP((pos, ang))] = 1
	c = 0
	while True:
		c+= 1
		print c, pos, ang
		# In this situation, casenum is not the case number for the location in statespace we are calculating
		# rho for. Instead, it is the case numebr to be used for propagating back to the previous location,
		# namely, same position but negated angle.
		casenum = CASE_LOOKUP[pos, -ang]
		loc = (loc_from_pos(pos), loc_from_ang(ang)) # this is still correct location. loc[1] to be negated later.
		if casenum != -1:
			invrs = updates[casenum](loc[0], - loc[1])
			invrs = (invrs[0], -invrs[1])
			refang = ang_from_loc(invrs[1])
			refpos = pos_from_loc(invrs[0])

			if refang != None and refpos != None: #@xander when does that happen?
				backcase = int(CASE_LOOKUP[refpos, refang])
				if invariant[index_from_CASE_LOOKUP((refpos,refang))] == 0:
					invariant[index_from_CASE_LOOKUP((refpos,refang))] = float(jacobians[backcase](*invrs))
					pos, ang = refang, refpos
				else:
					break
	return invariant

def distribution_to_dataset(dist):
	X = []
	Y = []
	matrix_form = []
	for i in range(SCALE):
		matrix_form.append([float(i) for i in dist[SCALE * i:SCALE * (i + 1)]])
	for row in range(len(matrix_form)):
		for col in range(len(matrix_form[0])):
			X.append((row, col))
			Y.append(dist[index_from_CASE_LOOKUP((row, col))])
	return np.array(X), np.array(Y)
