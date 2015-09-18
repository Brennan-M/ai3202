# Node Class used in our Maze Solver

class Node(object):

	def __init__(self, location, distanceToStart = None, parent = None):
		self.location = location
		self.distanceToStart = distanceToStart
		self.parent = parent

	def getLocation(self):
		return self.location

	def getDistanceToStart(self):
		return distanceToStart

	def getParent(self):
		return parent

	def setDistanceToStart(self, dist):
		self.distanceToStart = dist

	def setParent(self, pNode):
		self.parent = pNode