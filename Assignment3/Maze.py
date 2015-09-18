# CSCI 3202: Artificial Intelligence
# Assignment 3: A* Maze Solver
# By Brennan McConnell

import sys
import math

# Node Class used in our Maze Solver
class Node(object):

	def __init__(self, location, distanceToStart = 0, parent = None):
		self.location = location
		self.distanceToStart = distanceToStart
		self.parent = parent

	def getLocation(self):
		return self.location

	def getDistanceToStart(self):
		return self.distanceToStart

	def getParent(self):
		return self.parent

	def setDistanceToStart(self, h, isMountain, endP, worldMaze):
		pLoc = self.parent.getLocation()
		stepDistance = abs(pLoc[0] - self.location[0]) + abs(pLoc[1] - self.location[1])
		if stepDistance == 1:
			self.distanceToStart = 10 + self.parent.getDistanceToStart()
		else:
			self.distanceToStart = 14 + self.parent.getDistanceToStart()

		if isMountain == 1:
			self.distanceToStart += 10

		if h == 1:
			self.distanceToStart += abs(endP[0] - self.location[0]) + abs(endP[1] - self.location[1])
		elif h == 2:
			hCost = 0
			if isMountain == 1 and worldMaze[self.location[0] - 1][self.location[1] + 1] == 1:
				hCost += 100
			elif isMountain == 1 and stepDistance == 2:
				hCost -= 10
			self.distanceToStart += abs(endP[0] - self.location[0]) + abs(endP[1] - self.location[1]) + hCost


	def setParent(self, pNode):
		self.parent = pNode



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

def getMinimumNode(openOptions):
	result = openOptions[0]
	for node in openOptions:
		if node.getDistanceToStart() < result.getDistanceToStart():
			result = node

	return result

# We are forced to assume valid file input.
def getArgs():
	print("\n-----------------------------------\n")

	if len(sys.argv) != 3:
		print("Illegal Arguments Provided.")
		print("Proper usage is: <file> <heuristic>")
		print("Argument for heuristic is an integer, 1 or 2")
		print ("\n-----------------------------------\n")
		sys.exit()

	worldMaze = constructWorld(sys.argv[1])
	heuristic = int(sys.argv[2])

	if (heuristic != 1 and heuristic != 2):
		print("Invalid heuristic selected.")
		print("Solving the maze using default heuristic: Manhattan...\n")
		heuristic = 1

	return (worldMaze, heuristic)

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

def printHeuristic(h):
	if h == 1:
		print("Heuristic: Manhattan")
	elif h == 2:
		print("Heuristic: Custom")

def traceInformation(node, maze, count):
	cost = 0
	path = []
	heuristicTrace = []

	print "\nTotal Heuristic cost: ", node.getDistanceToStart()
	
	tmp_ptr = node
	while (tmp_ptr):
		path.append(tmp_ptr.getLocation())
		if not tmp_ptr.getParent() == None:
			stepDistance = abs(tmp_ptr.getParent().getLocation()[0] - tmp_ptr.getLocation()[0]) + abs(tmp_ptr.getParent().getLocation()[1] - tmp_ptr.getLocation()[1])
			if stepDistance == 1:
				cost += 10
			elif stepDistance == 2:
				cost += 14
			if worldMaze[tmp_ptr.getLocation()[0]][tmp_ptr.getLocation()[1]] == 1:
				cost += 10
			heuristicTrace.append(tmp_ptr.getDistanceToStart())
		tmp_ptr = tmp_ptr.getParent()

	heuristicTrace.append(0)

	print "Total Cost: ", cost
	print "Nodes Evaluted: ", count

	print "\nPath:"
	for i in range(len(path) - 1, -1, -1):
		print path[i], "with heuristic cost", heuristicTrace[i]
	print("")

	for x,y in path:
		maze[x][y] = 'X'

	printMaze(maze)


if __name__ == "__main__":
	(worldMaze, heuristic) = getArgs()
	printHeuristic(heuristic)
	solveMaze(worldMaze, heuristic)
	print ("\n-----------------------------------\n")










