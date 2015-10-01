# CSCI 3202: Artificial Intelligence
# Assignment 5: Markov Decision Processes
# By Brennan McConnell

import sys
import math

EXIT_STATE = "*"

# Node Class used in our Maze Solver
class Node(object):

	def __init__(self, location, value):
		self.location = location
		self.obstacle = obstacle

		if value == 50:
			self.utility = 50
			self.optimalMove = EXIT_STATE
		else:
			self.utility = 0
			self.optimalMove = None

			if (value == 1):
				self.reward = -1
			elif (value == 3):
				self.reward = -2
			elif (value == 4):
				self.reward = 1


	def getLocation(self):
		return self.location

	def getOptimalMove(self):
		return self.optimalMove

	def getReward(self):
		return self.reward

	def getUtility(self):
		return self.utility

	def setOptimalMove(self, direction):
		self.optimalMove = direction

	def setReward(self, reward):
		self.reward = reward

	def setUtility(self, utility):
		self.utility = utility

	def __cmp__(self, ntc):
		if self.utility > ntc.getUtility():
			return 1
		elif self.utility < ntc.getUtility():
			return -1
		elif self.utility = None:
			if ntc.getUtility() = None:
				return 0
			else:
				return -1
		elif ntc.getUtility() = None:
			return 1
		return 0


def solveMaze(worldMaze, heuristic):
	endPosition = (0, len(worldMaze[0]) - 1)

	start = (len(worldMaze) - 1, 0) # Assigns our starting index to the bottom left
	startNode = Node(start, 0)

	openOptions = []
	visited = {}
	openOptions.append(startNode)
	count = 1

	while (len(openOptions) > 0):

		tempNode = getMinimumNode(openOptions)
		
		for node in openOptions:
			if node.getLocation() == tempNode.getLocation():
				openOptions.remove(node)
				break


		if (tempNode.getLocation() != endPosition):

			currentLocation = tempNode.getLocation()
			visited[currentLocation] = True

			for i in range(currentLocation[0] - 1, currentLocation[0] + 2):
				for j in range(currentLocation[1] - 1, currentLocation[1] + 2):
					
					if (i >= 0 and i < len(worldMaze)):
						if (j >= 0 and j < len(worldMaze[0])):
							if (visited.get((i,j), False) != True): # We have not visited it yet
								if (worldMaze[i][j] != 2):

									adjNode = Node((i,j))
									adjNode.setParent(tempNode)
									adjNode.setDistanceToStart(heuristic, worldMaze[i][j], endPosition, worldMaze)
									
									alterExisting = False
									for node in openOptions:
										if node.getLocation() == (i,j):
											alterExisting = True
											if node.getDistanceToStart() > adjNode.getDistanceToStart():
												node.distanceToStart = adjNode.getDistanceToStart()
											break
												

									if alterExisting == False:
										# If we add a node to our array, we have evaluated a node.
										count += 1
										openOptions.append(adjNode)

		else:
			traceInformation(tempNode, worldMaze, count)
			return

	print "no Solution Found"


# We are forced to assume valid file input.
def getArgs():
	print("\n-----------------------------------\n")

	
	if len(sys.argv) > 3:
		print("Illegal Arguments Provided.")
		print("Proper usage is: <file> <epsilon>")
		print ("\n-----------------------------------\n")
		sys.exit()

	if len(sys.argv) == 3:
		worldMaze = constructWorld(sys.argv[1])
		epsilon = float(sys.argv[2])
	elif len(sys.argv) == 2:
		print("Epsilon value not provided, using Default.")
		epsilon = 0.5
	elif len (sys.argv) == 1:
		print ("Maze not provided, using Default.")
		worldMaze = constructWorld("World1.txt")
		print("Epsilon value not provided, using Default.")
		epsilon = 0.5

	print "\nSolving the maze with episolon value:", epsilon
	return (worldMaze, epsilon)

def constructWorld(fileName):
	worldMaze = []
	worldFile = open(fileName, "r")
	for line in worldFile:
		worldMaze.append([int(i) for i in line.split()])

	return worldMaze

def printMaze(worldMaze):
	print("Path:")
	for i in worldMaze:
		tmpArr = [str(x) for x in i]
		print " ".join(tmpArr)


# def traceInformation(node, maze, count):
# 	cost = 0
# 	path = []
# 	heuristicTrace = []

# 	print "\nTotal Heuristic cost: ", node.getDistanceToStart()
	
# 	tmp_ptr = node
# 	while (tmp_ptr):
# 		path.append(tmp_ptr.getLocation())
# 		if not tmp_ptr.getParent() == None:
# 			stepDistance = abs(tmp_ptr.getParent().getLocation()[0] - tmp_ptr.getLocation()[0]) + abs(tmp_ptr.getParent().getLocation()[1] - tmp_ptr.getLocation()[1])
# 			if stepDistance == 1:
# 				cost += 10
# 			elif stepDistance == 2:
# 				cost += 14
# 			if worldMaze[tmp_ptr.getLocation()[0]][tmp_ptr.getLocation()[1]] == 1:
# 				cost += 10
# 			heuristicTrace.append(tmp_ptr.getDistanceToStart())
# 		tmp_ptr = tmp_ptr.getParent()

# 	heuristicTrace.append(0)

# 	print "Total Cost: ", cost
# 	print "Nodes Evaluted: ", count

# 	print "\nPath:"
# 	for i in range(len(path) - 1, -1, -1):
# 		print path[i], "with heuristic cost", heuristicTrace[i]
# 	print("")

# 	for x,y in path:
# 		maze[x][y] = 'X'

# 	printMaze(maze)


if __name__ == "__main__":
	(worldMaze, epsilon) = getArgs()
	solveMaze(worldMaze, epsilon)
	print ("\n-----------------------------------\n")










