from math import sqrt

#takes two points on the same Y plane and their distances to a point C and
#returns the X and Y coordinates of the point C
def get_third_point(aX, bX, Y, AC, BC):
	# if the sum of the two smaller sides of the triangle are less than
	# the longest side, then the triangle is possible, the third point
	# does not exist, and we return None
	AB = bX - aX
	distances = []
	distances.append(AB)
	distances.append(AC)
	distances.append(BC)
	distances.sort()
	if distances[0] + distances[1] < distances[2]:
		return None
	cX = (AC**2 - BC**2 - aX**2 + bX**2) / (2 * bX - 2 * aX)
	print("cX calculated as: " + str(cX))

	cY = sqrt(BC**2 - (cX - bX)**2) + Y
	print("cY calculated as: " + str(cY))

	return [cX, cY]