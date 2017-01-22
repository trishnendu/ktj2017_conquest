def orientation(point1, point2, X):
	val = (X[1] - point1[1])*(point2[0] - point1[0]) - (point2[1] - point1[1])*(X[0] - point1[0])
	if val > 0:
		return 1
	elif val < 0:
		return -1
	else:
		return 0							

	
def onSegment(p,q,r):
	if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]):
		return True;
	return False;

def doesIntersect(seg1p1, seg1p2, seg2p1, seg2p2):
	f1 = orientation(seg1p1, seg1p2, seg2p2)
	f2 = orientation(seg1p1, seg1p2, seg2p1)
	f3 = orientation(seg2p1, seg2p2, seg1p1)
	f4 = orientation(seg2p1, seg2p2, seg1p2)
			
	if f1 != f2 and f3 != f4:
		return True
			
	if f1 == 0 and onSegment(seg1p1, seg2p1, seg1p2):
		return True
	if f2 == 0 and onSegment(seg1p1, seg2p2, seg1p2):
		return True
	if f3 == 0 and onSegment(seg2p2, seg1p2, seg2p1):
		return True
	if f4 == 0 and onSegment(seg2p2, seg1p1, seg2p1):
		return True	
	
def distance(point1, point2):
	return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**.5
	
	
