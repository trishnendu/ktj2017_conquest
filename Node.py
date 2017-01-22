class Node:
    def __init__(self,coordinate,t = None):
        self.type = t
        self.parent = None
        self.children = []
        self.pos = tuple(coordinate)

    def getType(self):
        return self.type

    def getParent(self):
        return self.parent
        
    def getchildren(self):
        return self.children

    def setType(self,t):
        self.type = t

    def setParent(self, pnode):
        self.parent = pnode
        
    def addChild(self, node):	
    	self.children.append(node)
        
    def distance(self, node):
    	return ((self.pos[0]-node.pos[0])**2+(self.pos[1]-node.pos[1])**2)**.5
    
    def ifNeighbour(self, node):
    	if abs(self.pos[0]-node.pos[0]) <= 1 and abs(self.pos[1]-node.pos[1]) <= 1 and self.pos != node.pos:
    		return True
    	else:
    		return False

