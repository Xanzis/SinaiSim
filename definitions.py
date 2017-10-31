import numpy as np 

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
	mn = 0
	mx = 0
	return (mn, mx)
def r2_minmax_angle(position):
	mn = 0
	mx = 0
	return (mn, mx)
def r3_minmax_angle(position):
	mn = 0
	mx = 0
	return (mn, mx)
def r4_minmax_angle(position):
	mn = 0
	mx = 0
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
	theta = 0
	return (newpos, newtheta)
def r2_update(position, angle):
	newpos = 0
	theta = 0
	return (newpos, newtheta)
def r3_update(position, angle):
	newpos = 0
	theta = 0
	return (newpos, newtheta)
def r4_update(position, angle):
	newpos = 0
	theta = 0
	return (newpos, newtheta)
def r5_update(position, angle):
	newpos = 0
	theta = 0
	return (newpos, newtheta)
def r6_update(position, angle):
	newpos = 0
	theta = 0
	return (newpos, newtheta)
def r7_update(position, angle):
	newpos = 0
	theta = 0
	return (newpos, newtheta)
def r8_update(position, angle):
	newpos = 0
	theta = 0
	return (newpos, newtheta)

def r1_inverse(position, angle):
	oldpos = 0
	oldangle = 0
	return (oldpos, oldangle)
def r2_inverse(position, angle):
	oldpos = 0
	oldangle = 0
	return (oldpos, oldangle)
def r3_inverse(position, angle):
	oldpos = 0
	oldangle = 0
	return (oldpos, oldangle)
def r4_inverse(position, angle):
	oldpos = 0
	oldangle = 0
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

def r1_jacobian():
	return 1
def r2_jacobian():
	return 1
def r3_jacobian():
	return 1 # return 1 is actually correct here
def r4_jacobian():
	return 1 # here too. Also, might be true for all non-circle cases
def r5_jacobian():
	return 1
def r6_jacobian():
	return 1
def r7_jacobian():
	return 1
def r8_jacobian():
	return 1

# Following dictionaries should be a better format for fast lookup:
minmaxes = {
	1: r1_minmax_angle,
	2: r2_minmax_angle,
	3: r3_minmax_angle,
	4: r4_minmax_angle,
	5: r5_minmax_angle,
	6: r6_minmax_angle,
	7: r7_minmax_angle,
	8: r8_minmax_angle
}
updates = {
	1: r1_update,
	2: r2_update,
	3: r3_update,
	4: r4_update,
	5: r5_update,
	6: r6_update,
	7: r7_update,
	8: r8_update
}
inverses = {
	1: r1_inverse,
	2: r2_inverse,
	3: r3_inverse,
	4: r4_inverse,
	5: r5_inverse,
	6: r6_inverse,
	7: r7_inverse,
	8: r8_inverse,
}

jacobians = {
	1: r1_jacobian,
	2: r2_jacobian,
	3: r3_jacobian,
	4: r4_jacobian,
	5: r5_jacobian,
	6: r6_jacobian,
	7: r7_jacobian,
	8: r8_jacobian,
}