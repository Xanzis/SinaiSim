import numpy as np

def arccot(a): # This exists so I can have a continuous arccot for my boundaries
	if a == 0:
		return np.pi / 2
	if a < 0:
		return np.arctan(1/a) + np.pi
	return np.arctan(1/a)

def delta(position, angle):
	r = 0.3333
	a = position
	t = angle
	thingy = -1 - a **2 + 2 * r **2 
	thingy += - (-1 + a **2)*np.cos(2 * t)
	thingy += - 2 * a * np.sin(2 * t)
	thingy *= 2
	return np.sqrt(thingy)
	"""
	=Sqrt[2(-1 - a^2 + 2 r^2 - (-1 + a^2) Cos[2 theta] - 2 a Sin[2 theta])]
	for use in calculating updates for the circle
	"""

"""
Case definition:
r1 Hits right without hitting circle
r2 Hits left without hitting circle
r3 Hits opposite without hitting circle, passing circle on left
r4 Hits opposite without hitting circle, passing circle on right
r5 Hits circle, comes back
r6 Hits circle, goes right
r7 Hits circle, goes left
r8 Hits circle, goes opposite (on right side)
r9 Hits circle, goes opposite (on left side)
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
	a = position
	thingy1 = (a - 1j) - np.roots([a * (81 + 81j) - 81 + 81j,  -9 -18j - 9 * a, 0, a + 1 - 2j, 1 + 1j - a * (1 - 1j)])[3]
	thingy2 = (a - 1j) - np.roots([a * (81 + 81j) - 81 + 81j, (-18 - 9j) + 9j * a, 0, (-2 + 1j) - 1j * a, (-1 -1j) + a * (1 - 1j)])[3]
	mn = - np.pi / 2 - np.arctan2(thingy2.imag, thingy2.real)
	mx = - np.pi / 2 - np.arctan2(thingy1.imag, thingy1.real)
	return (mn, mx)
def r6_minmax_angle(position):
	mx, mn = r7_minmax_angle(-position)
	mn *= -1
	mx *= -1
	return (mn, mx)
def r7_minmax_angle(position):
	a = position
	thingy2 = (a - 1j) - np.roots([a * (81 + 81j) - 81 + 81j, (-18 - 9j) + 9j * a, 0, (-2 + 1j) - 1j * a, (-1 -1j) + a * (1 - 1j)])[3]
	mx = - np.pi / 2 - np.arctan2(thingy2.imag, thingy2.real)
	if np.arctan((a + 1)/2) > np.pi/4 - np.arcsin(1 / (3 * np.sqrt(2))):
		mn = - np.pi / 2 - np.arctan(1 / -a) - np.arcsin(1 / (3 * np.sqrt(1 + a**2)))
	else:
		mnthing = (a - 1j) - np.roots([(81 + 81j) * a - 81 + 81j, 9 * a - 9, 0, 1 - a, 1 + 1j - a * (1 - 1j)])[3]
		mn = -np.pi / 2 - np.arctan2(mnthing.imag, mnthing.real)
	#mn = max()
	#mn = -4
	#mx = 4
	return (mn, mx)
def r8_minmax_angle(position):
	a = position
	thingy2 = (a - 1j) - np.roots([a * (81 + 81j) - 81 + 81j, (-18 - 9j) + 9j * a, 0, (-2 + 1j) - 1j * a, (-1 -1j) + a * (1 - 1j)])[3]
	mn = - np.pi / 2 - np.arctan2(thingy2.imag, thingy2.real)
	mx = 2
	# bit of a hack here. relies on the fact that other regions override, and on the fact that I'm lazy
	return (mn, mx)
def r9_minmax_angle(position):
	mx, mn = r8_minmax_angle(-position)
	mn *= -1
	mx *= -1
	return (mn, mx)

def r1_update(position, angle):
	newpos = (1 - position) * np.tan(np.pi / 2 - angle) - 1
	new_angle = - np.pi / 2 + angle
	return (newpos, new_angle)
def r2_update(position, angle):
	#newpos = 1 - (1 + position) * np.tan(np.pi / 2 - angle)
	#new_angle = np.pi / 2 - angle
	position *= -1
	angle *= -1
	newpos, new_angle = r1_update(position, angle)
	newpos *= -1
	new_angle *= -1
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
	delta = delta(position, angle)
	a = position
	t = angle
	r = 0.3333
	num = 0
	den = 0
	num += a * delta
	num += - 2 * a * (-1 + r **2) * np.cos(t)
	num += a * delta * np.cos(2 * t)
	num += - 2 * a * np.cos(3 * t)
	num += 3 * np.sin(t)
	num += a **2 * np.sin(t)
	num += - 4 * r **2 * np.sin(t)
	num += delta * np.sin(2 * t)
	num += - np.sin(3 * t)
	num += a **2 * np.sin(3 * t)
	thing = -2 * a + a * delta * np.cos(t) - 2 * a * np.cos(2 * t) + delta * np.sin(t)
	den += (-1 - 3 a **2 + 2 * r **2) * np.cos(t)
	den += - (-1 + a **2) * np.cos(3 * t)
	den += 2 * np.sin(t) * thing
	"""
	position = 
	(a delta - 2 a (-1 + r^2) Cos[theta] + a delta Cos[2 theta] - 
   2 a Cos[3 theta] + 3 Sin[theta] + a^2 Sin[theta] - 
    4 r^2 Sin[theta] + delta Sin[2 theta] - Sin[3 theta] + 
    a^2 Sin[3 theta])/((-1 - 3 a^2 + 2 r^2) Cos[
      theta] - (-1 + a^2) Cos[3 theta] + 
    2 Sin[theta] (-2 a + a delta Cos[theta] - 2 a Cos[2 theta] + 
       delta Sin[theta]))
	"""
	newpos = num/den
	atn = 0
	atn += a + a * np.cos(2 * t)
	atn += - delta * np.sin(t) + np.sin(2 * t)
	atn /= 1 + delta * np.cos(t) - np.cos(2 * t) + a * np.sin(2 * t)
	"""
	angle =
	theta + 2 ArcTan[(
    a + a Cos[2 theta] - delta Sin[theta] + Sin[2 theta])/(
    1 + delta Cos[theta] - Cos[2 theta] + a Sin[2 theta])]
	"""
	new_angle = t + 2 * np.arctan(atn)
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
def r9_update(position, angle):
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
def r9_inverse(position, angle):
	oldpos = 0
	oldangle = 0
	return (oldpos, oldangle)

# note: by jacobian, I actually mean determinant of the jacobian

def r1_jacobian(position, angle):
	return 1
def r2_jacobian(position, angle):
	return 1
def r3_jacobian(position, angle):
	return 1 # return 1 is actually correct here
def r4_jacobian(position, angle):
	return 1 # here too. Also, might be true for all non-circle cases
def r5_jacobian(position, angle):
	delta = delta(position, angle)
	a = position
	t = angle
	r = 0.3333
	num = 2 * r **2 * np.cos(t)
	den = 0
	den += (3 * a **2 + 2 * r **2 - 1) * np.cos(t)
	den += - a **2 cos(3 * t)
	den += a * delta * np.sin(2 * t)
	den += - 2 * a * np.sin(t)
	den += - 2 * a * np.sin(3 * t)
	den += - delta * np.cos(2 * t)
	den += delta
	den += np.cos(3 * t)
	return num / den
def r6_jacobian(position, angle):
	return 1
def r7_jacobian(position, angle):
	return 1
def r8_jacobian(position, angle):
	return 1
def r9_jacobian(position, angle):
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
	7: r8_minmax_angle,
	8: r9_minmax_angle
}
updates = {
	0: r1_update,
	1: r2_update,
	2: r3_update,
	3: r4_update,
	4: r5_update,
	5: r6_update,
	6: r7_update,
	7: r8_update,
	8: r9_update
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
	8: r9_inverse
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
	8: r9_jacobian
}
