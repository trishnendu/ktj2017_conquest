import json, math, random, time
import matplotlib.pyplot as plt
from Node import Node
from BasicComputationalGeometry import doesIntersect

class rrt_sssd:
	def __init__(self, src, dest, all_obs, obs_end_points, sl=math.inf):
		self.rootNode = Node(src, 'b')
		self.destNode = Node(dest, 'd')
		self.allNodes = [self.rootNode]
		'''
		self.foods = []
		
		if "food" in allobjects:
			for item in allobjects["food"]:
				self.foods.append(Node(item,'f'))
		self.woods = []
		if "wood" in allobjects:
			for item in allobjects["wood"]:
				self.woods.append(Node(item,'w'))
		
		self.obs = []
		if "obs" in allobjects:
			for item in allobjects["obs"]:
				self.obs.append(Node(item,'o'))
		'''
		self.obs = all_obs
		self.steplength = sl
		self.all_points_on_board = set()
		for i in range(400):
			for j in range(400):
				self.all_points_on_board.add((i,j))
		self.all_points_on_board -= set([x.pos for x in self.obs])
		self.obs_end_points_on_a_line = obs_end_points
		'''
		for endNodes in self.obs_end_points_on_a_line:
			print((endNodes[0].pos,endNodes[1].pos))
		''' 
							

	def nearNode(self, rnode):
		mindist = math.inf
		nnode = None
		for tmpnode in self.allNodes:
			dis = rnode.distance(tmpnode)
			if dis < mindist:
				mindist = dis
				nnode = tmpnode
		return nnode
	
	def findType(self, coordinate):
		if coordinate in self.obs:
			return 'o'
		return 'n'
		
		'''
		if coordinate in self.foods:
			return 'f'
		if coordinate in self.woods:
			return 'w'
		'''
				
	def nextStepNode(self, curTreeNode, rnode):
		dis = rnode.distance(curTreeNode)
		if dis < self.steplength:
			return rnode
		dx = float(rnode.pos[0] - curTreeNode.pos[0]) / dis 
		dy = float(rnode.pos[1] - curTreeNode.pos[1]) / dis 	
		StepNode = Node((curTreeNode.pos[0] + math.ceil(dx*self.steplength), curTreeNode.pos[1] + math.ceil(dy*self.steplength)))
		return StepNode
	  
	def isObstacleInMiddle(self, curTreeNode, tnode):
		for endnodes in self.obs_end_points_on_a_line:
			if doesIntersect(endnodes[0].pos, endnodes[1].pos, curTreeNode.pos, tnode.pos):
				return True
		return False
		
	def addtoTree(self, TreeNode, NewNode):  
	    #print(("Trying to add ",TreeNode.pos,NewNode.pos,"curr list",";".join(str(x.pos) for x in self.allNodes)))
	    t = self.findType(NewNode.pos)
	    if t == 'o':
	    	return False, False
	    #print((NewNode not in self.allNodes ,not self.isObstacleInMiddle(TreeNode, NewNode)))
	    if NewNode not in self.allNodes and not self.isObstacleInMiddle(TreeNode, NewNode):
	    	NewNode.setType(t)
	    	NewNode.setParent(TreeNode)
	    	TreeNode.addChild(NewNode)
	    	self.allNodes.append(NewNode)
	    	#self.add_allIntermidiateNode(TreeNode, NewNode)
	    	if NewNode.pos == self.destNode.pos:
	    		return True, True
	    	else:
	    		if not self.isObstacleInMiddle(NewNode, self.destNode):
	    			self.destNode.setParent(NewNode)
	    			NewNode.addChild(self.destNode)
	    			self.allNodes.append(self.destNode)
	    			return True, True
	    		return True, False
	    return False, False
	    
	def alreadyInTree(self, Node):
		for node in self.allNodes:
			if Node.pos == node.pos:
				return True
		return False	
	
	def rrt_driver(self):
		#print((self.rootNode.pos, self.destNode.pos))
		added, reached = self.addtoTree(self.rootNode, self.destNode)
		visited = set()
		while not reached:
			valid_points = self.all_points_on_board - set([x.pos for x in self.allNodes])
			while len(valid_points) > 0:
				randpos = random.sample(valid_points,1)[0]
				if randpos not in visited:
					break
				valid_points.remove(randpos)
			if len(valid_points) == 0:
				print("destination unreachable! ):")
				return
			#print(("Got randnode ", randpos))
			randnode = Node(randpos)
			prev = self.nearNode(randnode)		 
			added, reached = self.addtoTree(prev, randnode)
			if not added:
				#prev = self.rootNode
				while True:	
					stepnode = self.nextStepNode(prev, randnode)
					added, reached = self.addtoTree(prev, stepnode)
					if reached: 
						break
					if not added:
						visited.add(stepnode.pos)
						#print(("Can't add stepnode", stepnode.pos))
						break
					else:
						prev = stepnode
			else:
				visited.add((randnode.pos))
				'''
				#print(("Adding as ok", randnode.pos))
				#added, reached = self.addtoTree(randnode, self.destNode)
			#print("############## printing dfs tree #################")
			#self.print_dfs_tree()			
			#print("################ print complete #################")
		'''
		print(("reached",reached))
		path = []
		
		path1 = []
		curNode = self.destNode
		while curNode and curNode.pos not in path1:
				path1.append(curNode.pos)
				curNode = curNode.parent
		print(("Actual Path", path1))
		'''
		curNode = self.destNode
		while curNode != None:
			if self.isObstacleInMiddle(curNode, self.rootNode):
				path.append(curNode.pos)
				curNode = curNode.parent
			else:
				path.extend([curNode.pos,self.rootNode.pos])
				break
		print(("Path", path))
		'''
		return path1
		
	'''	
	def print_bfs_tree(self):
		queue = [self.rootNode]
		while len(queue) != 0:
			curNode = queue[0]		
			print ((curNode.pos,"->",",".join(x.pos for x in curNode.children)))
			queue.extend(curNode.children)
	
	def print_dfs_tree(self,node = None):
		if node is None:
			node = self.rootNode
		#print(node.pos)
		path = []
		if len(node.children) == 0:
			while node:
				path.append(node)
				node = node.parent
			print(" -> ".join(str(x.pos) for x in reversed(path)))
			return 	
		for child in node.children:	
			#print(("parent : ",node.pos,"child : ", " | ".join(str(x.pos) for x in node.children))) 
			self.print_dfs_tree(child)
	'''		
			
if __name__ == '__main__':
	infile = open("testcase3.json")
	objects = json.loads(infile.read())
	t = time.time()
	test = rrt_sssd((250,100),(250,250), objects)
	t = time.time() - t 
	path1, path = test.rrt_driver()
	#print(path)
	print(("time",t))
'''
	plt.axis([0,400,0,400])
	plt.plot([test.rootNode.pos[0]],[test.rootNode.pos[1]],'yo',[test.destNode.pos[0]],[test.destNode.pos[1]],'ro',[x.pos[0] for x in test.obs],[x.pos[1] for x in test.obs],'r*',[x[0] for x in path1],[x[1] for x in path1],'b*',[x[0] for x in path1],[x[1] for x in path1],'g')
	plt.show()
	plt.axis([0,400,0,400])
	plt.plot([test.rootNode.pos[0]],[test.rootNode.pos[1]],'yo',[test.destNode.pos[0]],[test.destNode.pos[1]],'ro',[x.pos[0] for x in test.obs],[x.pos[1] for x in test.obs],'r*',[x[0] for x in path],[x[1] for x in path],'g*',[x[0] for x in path],[x[1] for x in path],'b')
	plt.show()
	#print(" / ".join(str(x.pos) for x in test.allNodes))			
'''
