from Node import Node
from rrt_ktj import rrt_sssd
from BasicComputationalGeometry import orientation, distance, doesIntersect
import json, math, time
import matplotlib.pyplot as plt

class PathPlan:
	
	def __init__(self,inputfilename):
		infile = open(inputfilename)
		objects = json.loads(infile.read())
		self.obs = []
		if "obs" in objects:
			for item in objects["obs"]:
				self.obs.append(Node(item,'o'))
		self.obs_all_points_on_a_line = []
		self.obs_end_points_on_a_line = []
		self.obs_singlepoint = set()
		self.convert_obstacles()
		
	def PlanPath(self, src, dest):
		PathForsssd = rrt_sssd(src, dest, self.obs, self.obs_end_points_on_a_line)
		return PathForsssd.rrt_driver()
			
	def convert_obstacles(self):
		checked = {}
		for node1 in self.obs:
			for node2 in self.obs:
				if node1.ifNeighbour(node2):
					#print(("Neighbour",node1.pos,node2.pos,node1.ifNeighbour(node2)))
					flag1 = node1.pos in checked
					flag2 = node2.pos in checked 
					if flag1^flag2:
						if node2.pos not in checked and node1.pos in checked:
							node1, node2 = node2, node1
						
						for index in checked[node2.pos]:
							if not bool(orientation(self.obs_all_points_on_a_line[index][0].pos, self.obs_all_points_on_a_line[index][1].pos, node1.pos)):
								if node1.pos not in checked:
									checked[node1.pos] = []
									#print((node1.pos,"Added as on line ",self.obs_all_points_on_a_line[index][0].pos, self.obs_all_points_on_a_line[index][1].pos, node1.pos))
								checked[node1.pos].append(index)
								self.obs_all_points_on_a_line[index].append(node1)
								break;
						else:
							self.obs_all_points_on_a_line.append([node1, node2])
							lp = len(self.obs_all_points_on_a_line) - 1
							checked[node1.pos] = []
							#print((node1.pos,"Added as not on line ",node2.pos, node1.pos))
							checked[node1.pos].append(lp)
							checked[node2.pos].append(lp)	
							
					elif not flag1 and not flag2:
						self.obs_all_points_on_a_line.append([node1, node2])
						lp = len(self.obs_all_points_on_a_line) - 1	
						if node1.pos not in checked:
							checked[node1.pos] = []
						if node2.pos not in checked:
							checked[node2.pos] = []
							#print((node1.pos,"Added as first seen",node2.pos, node1.pos))
						checked[node1.pos].append(lp)
						checked[node2.pos].append(lp)	
					
					else:
						occur1 = set(checked[node1.pos])
						occur2 = set(checked[node2.pos])
						if not bool(occur1 & occur2):
							self.obs_all_points_on_a_line.append([node1, node2])
							lp = len(self.obs_all_points_on_a_line) - 1	
							checked[node1.pos].append(lp)
							checked[node2.pos].append(lp)	
		'''						
		print(checked)
		for i in range(len(self.obs_all_points_on_a_line)):
			print(" | ".join(str(x.pos) for x in self.obs_all_points_on_a_line[i]))
		'''
		self.obs_singlepoint = set([x.pos for x in self.obs]) - set(checked.keys())
		#print((self.obs_singlepoint, set([x.pos for x in self.obs]), set(checked.keys())))
		
		for i in range(len(self.obs_all_points_on_a_line)):
			minx = math.inf
			maxx = - math.inf
			point1 = None
			point2 = None
			for node in self.obs_all_points_on_a_line[i]:
				if minx > node.pos[0]:
					minx = node.pos[0]
					point1 = node
				if maxx < node.pos[0]:
					maxx = node.pos[0]
					point2 = node
			if point1 == point2:
				miny = math.inf
				maxy = - math.inf
				for node in self.obs_all_points_on_a_line[i]:
					if miny > node.pos[1]:
						miny = node.pos[1]
						point1 = node
					if maxy < node.pos[1]:
						maxy = node.pos[1]
						point2 = node
			self.obs_end_points_on_a_line.append([point1,point2])
		'''
		for i in range(len(self.obs_end_points_on_a_line)):
			print(" | ".join(str(x.pos) for x in self.obs_end_points_on_a_line[i]))	 
		'''
	def isObstacleInMiddle(self, point1, point2):
		for endnodes in self.obs_end_points_on_a_line:
			if doesIntersect(endnodes[0].pos, endnodes[1].pos, point1, point2):
				return True
		return False
		
	def PathSmoothing(self, path):
		p = path.copy()
		#smoothPath = [p.pop()]
		smoothPath = []
		while len(p) > 1:
			curp = p.pop()
			smoothPath.append(curp)			
			print((curp,p))
			pathdis = [distance(curp,p[-1])]
			for i in range(len(p)-2,0,-1):
				pathdis.append(pathdis[-1]+distance(p[i+1],p[i]))
			print(pathdis)
			print((len(pathdis), len(p)))
			for i in range(1,len(p)):
				if distance(curp, p[i]) < pathdis[len(p)-i-1] and not self.isObstacleInMiddle(curp, p[i]):
					p = p[:i+1]
					break
			'''
			if i == len(p)-1:
				p.reverse()
				smoothPath.extend(p)
				return smoothPath
			'''
		smoothPath.append(p[0])
		return smoothPath	
		
		
if __name__=='__main__':
	t = time.time()
	pp = PathPlan("testcase3.json")
	path = pp.PlanPath((250,100),(250,250))
	#path = [(250, 250), (396, 295), (396, 290), (395, 285), (394, 280), (393, 275), (392, 270), (391, 265), (390, 260), (389, 255), (388, 250), (387, 245), (386, 240), (385, 235), (384, 230), (250, 100)]
	#path = pp.PathSmoothing(path)
	#best_path = pp.PathSmoothing(path)
	#print("smooth", best_path)
	print(time.time()-t)
	
	plt.axis([0,500,0,500])
	plt.plot(250,100,'yo',250,250,'ro',[x.pos[0] for x in pp.obs],[x.pos[1] for x in pp.obs],'r*',[x[0] for x in path],[x[1] for x in path],'g*',[x[0] for x in path],[x[1] for x in path],'b')
	plt.show()
	
	path = pp.PathSmoothing(path)
	print(path)
	plt.axis([0,500,0,500])
	plt.plot(250,100,'yo',250,250,'ro',[x.pos[0] for x in pp.obs],[x.pos[1] for x in pp.obs],'r*',[x[0] for x in path],[x[1] for x in path],'g*',[x[0] for x in path],[x[1] for x in path],'b')
	plt.show()
	
