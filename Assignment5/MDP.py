# CSCI 3202: Artificial Intelligence
# Assignment 5: Markov Decision Processes
# By Brennan McConnell

import sys
import math

DISCOUNT = 0.9

# Node Class used in our Maze Solver
class Node(object):

	def __init__(self, location, value):
		self.location = location
		self.value = value

		if value == 50:
			self.utility = 50
			self.optimalMove = "*"
			self.reward = 0
		else:
			self.utility = 0
			self.optimalMove = None

			if (value == 2):
				self.optimalMove = "W" # Let 'W' represent Wall

			if (value == 1):
				self.reward = -1
			elif (value == 3):
				self.reward = -2
			elif (value == 4):
				self.reward = 1
			else:
				self.reward = 0


	def getLocation(self):
		return self.location

	def getOptimalMove(self):
		return self.optimalMove

	def getReward(self):
		return self.reward

	def getUtility(self):
		return self.utility

	def getObstacle(self):
		return self.value

	def setOptimalMove(self, direction):
		self.optimalMove = direction

	def setUtility(self, utility):
		self.utility = utility

	def __cmp__(self, ntc):
		if self.utility > ntc.getUtility():
			return 1
		elif self.utility < ntc.getUtility():
			return -1
		elif self.utility == None:
			if ntc.getUtility() == None:
				return 0
			else:
				return -1
		elif ntc.getUtility() == None:
			return 1
		return 0

	def __str__(self):
		return (str(self.location)) + " - Utility: " + str(self.utility) + " - Direction: " + self.optimalMove


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
		worldMaze = constructWorld(sys.argv[1])
		print("Epsilon value not provided, using Default.")
		epsilon = 0.5
	elif len (sys.argv) == 1:
		print ("Maze not provided, using Default.")
		worldMaze = constructWorld("World1.txt")
		print("Epsilon value not provided, using Default.")
		epsilon = 0.5

	if (epsilon < 0):
		print("Epsilon cannot be less than 0, using Default.")

	print "\nSolving the maze with episolon value:", epsilon
	return (worldMaze, epsilon)


def constructWorld(fileName):
	worldMaze = []
	worldFile = open(fileName, "r").readlines()
	for line in reversed(worldFile):
		worldMaze.append(line.split(" "))

	nodeMaze = []
	for i in range(len(worldMaze)):
		nodeMaze.append([])
		for j in range(len(worldMaze[i])):
			nodeMaze[i].append(Node((j, i), int(worldMaze[i][j])))

	return nodeMaze


# This function uses value iteration to implement MDP of our maze
def setOverallOptimalMoves(worldMaze, epsilon):
	delta = float("inf")
	while (delta > epsilon * (1-DISCOUNT)/DISCOUNT):
		delta = 0
		for i in range(len(worldMaze)-1, -1, -1):
			for j in range(len(worldMaze[i])-1, -1, -1):
				tempDelta = evaluateUtility(i, j, worldMaze)
				if tempDelta > delta:
					delta = tempDelta


	print ("Finished calculations...\n")


def evaluateUtility(i, j, world):
	node = world[i][j]
	index_obstacle = node.getObstacle()

	if index_obstacle == 50 or index_obstacle == 2:
		return None

	# Must do bounds checking and then get the utilities of the s' around us
	if (i - 1) < 0:
		utilityDown = 0
	else:
		utilityDown = (world[i-1][j]).getUtility()

	if (i + 1) >= len(worldMaze):
		utilityUp = 0
	else:
		utilityUp = (world[i+1][j]).getUtility()

	if (j - 1) < 0:
		utilityLeft = 0
	else:
		utilityLeft = (world[i][j-1]).getUtility()

	if (j+1) >= len(worldMaze[i]):
		utilityRight = 0
	else:
		utilityRight = (world[i][j+1]).getUtility()

	upMoveUtility = ((0.8 * utilityUp + 0.1 * utilityLeft + 0.1 * utilityRight), "U")
	downMoveUtility = ((0.8 * utilityDown + 0.1 * utilityRight + 0.1 * utilityLeft), "D")
	rightMoveUtility = ((0.8 * utilityRight + 0.1 * utilityDown + 0.1 * utilityUp), "R")
	leftMoveUtility = ((0.8 * utilityLeft + 0.1 * utilityUp + 0.1 * utilityDown), "L")

	currentNodeUtility = node.getUtility()
	optimalUtility = max(upMoveUtility, downMoveUtility, rightMoveUtility, leftMoveUtility)
	node.setUtility(float(node.getReward() + DISCOUNT * optimalUtility[0]))
	node.setOptimalMove(optimalUtility[1])

	return abs(currentNodeUtility - node.getUtility())


def findOptimalPath(maze):
	print("\nOptimal Path:")
	print("Coordinates in (x, y) format.")
	i = 0
	j = 0
	currentNode = maze[i][j]
	while (currentNode.getOptimalMove() != "*"):
		print currentNode
		optMove = currentNode.getOptimalMove()
		if optMove == "U":
			i += 1
		elif optMove == "D":
			i -= 1
		elif optMove == "R":
			j += 1
		elif optMove == "L":
			j -= 1
		currentNode = maze[i][j]


def printMazeMoves(maze):
	print("Map:")
	for i in reversed(worldMaze):
		tmpArr = [str(x.getOptimalMove()) for x in i]
		print " ".join(tmpArr)



if __name__ == "__main__":
	(worldMaze, epsilon) = getArgs()
	setOverallOptimalMoves(worldMaze, epsilon)
	findOptimalPath(worldMaze)
	print("\n\n")
	printMazeMoves(worldMaze)
	print ("\n-----------------------------------\n")










