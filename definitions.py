import numpy as np

def arccot(a): # This exists so I can have a continuous arccot for my boundaries
	if a == 0:
		return np.pi / 2
	if a < 0:
		return np.arctan(1/a) + np.pi
	return np.arctan(1/a)

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
"""

def r1_minmax_angle(position):
	mn = max(np.arcsin(0.333 / np.sqrt(1 + position **2)) + arccot(position) - np.pi / 2, np.arctan((1 - position) / 2))
	mx = np.pi / 2
	return (mn, mx)
def r2_minmax_angle(position):
	mn = - np.pi / 2
	mx = min( - np.arctan(position) - np.arcsin(0.333 / np.sqrt(1 + position**2)), - np.arctan((1 + position) / 2))
	return (mn, mx)
def r3_minmax_angle(position):
	mn = - np.arctan((1 + position)/2)
	mx = (np.pi / 2) - arccot(-position) - np.arcsin(0.333 / np.sqrt(1 + position**2))
	return (mn, mx)
def r4_minmax_angle(position):
	mn = np.arcsin(0.333 / np.sqrt(1 + position**2)) + arccot(position) - np.pi / 2
	mx = np.arctan((1 - position) / 2)
	return (mn, mx)
def r5_minmax_angle(position):
	mn = 0
	mx = 0
	return (mn, mx)
def r6_minmax_angle(position):
	mn = 0
	mx = 0
	return (mn, mx)
def r7_minmax_angle(position):
	mn = 0
	mx = 0
	return (mn, mx)
def r8_minmax_angle(position):
	mn = 0
	mx = 0
	return (mn, mx)

def r1_update(position, angle):
	newpos = 0
	new_angle = 0
	return (newpos, new_angle) #we don't have to call it new_angle but before
								# you had theta and then newtheta in the return
								# so we need to at least pick one of those two.
def r2_update(position, angle):
	newpos = 0
	new_angle = 0
	return (newpos, new_angle)
def r3_update(position, angle):
	newpos = - 2 * np.tan(angle) - position
	new_angle = - angle
	return (newpos, new_angle)
def r4_update(position, angle):
	newpos = - 2 * np.tan(angle) - position
	new_angle = - angle
	return (newpos, new_angle)
def r5_update(position, angle):
	newpos = 0
	new_angle = 0
	return (newpos, new_angle)
def r6_update(position, angle):
	newpos = 0
	new_angle = 0
	return (newpos, new_angle)
def r7_update(position, angle):
	newpos = 0
	new_angle = 0
	return (newpos, new_angle)
def r8_update(position, angle):
	newpos = 0
	new_angle = 0
	return (newpos, new_angle)

def r1_inverse(position, angle):
	oldpos = 0
	oldangle = 0
	return (oldpos, oldangle)
def r2_inverse(position, angle):
	oldpos = 0
	oldangle = 0
	return (oldpos, oldangle)
def r3_inverse(position, angle):
	oldpos = - position - 2 * np.tan(- angle)
	oldangle = - angle
	return (oldpos, oldangle)
def r4_inverse(position, angle):
	oldpos = - position - 2 * np.tan(- angle)
	oldangle = - angle
	return (oldpos, oldangle)
def r5_inverse(position, angle):
	oldpos = 0
	oldangle = 0
	return (oldpos, oldangle)
def r6_inverse(position, angle):
	oldpos = 0
	oldangle = 0
	return (oldpos, oldangle)
def r7_inverse(position, angle):
	oldpos = 0
	oldangle = 0
	return (oldpos, oldangle)
def r8_inverse(position, angle):
	oldpos = 0
	oldangle = 0
	return (oldpos, oldangle)

def r1_jacobian(position, angle):
	return 1
def r2_jacobian(position, angle):
	return 1
def r3_jacobian(position, angle):
	return 1 # return 1 is actually correct here
def r4_jacobian(position, angle):
	return 1 # here too. Also, might be true for all non-circle cases
def r5_jacobian(position, angle):
	return 1
def r6_jacobian(position, angle):
	return 1
def r7_jacobian(position, angle):
	return 1
def r8_jacobian(position, angle):
	return 1

# Following dictionaries should be a better format for fast lookup:
minmaxes = {
	0: r1_minmax_angle,
	1: r2_minmax_angle,
	2: r3_minmax_angle,
	3: r4_minmax_angle,
	4: r5_minmax_angle,
	5: r6_minmax_angle,
	6: r7_minmax_angle,
	7: r8_minmax_angle
}
updates = {
	0: r1_update,
	1: r2_update,
	2: r3_update,
	3: r4_update,
	4: r5_update,
	5: r6_update,
	6: r7_update,
	7: r8_update
}
inverses = {
	0: r1_inverse,
	1: r2_inverse,
	2: r3_inverse,
	3: r4_inverse,
	4: r5_inverse,
	5: r6_inverse,
	6: r7_inverse,
	7: r8_inverse,
}

jacobians = {
	0: r1_jacobian,
	1: r2_jacobian,
	2: r3_jacobian,
	3: r4_jacobian,
	4: r5_jacobian,
	5: r6_jacobian,
	6: r7_jacobian,
	7: r8_jacobian,
}
