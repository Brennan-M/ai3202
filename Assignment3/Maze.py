# CSCI 3202: Artificial Intelligence
# Assignment 3: A* Maze Solver
# By Brennan McConnell

import sys


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
	worldFile = open(fileName, "r");
	for line in worldFile:
		worldMaze.append([int(i) for i in line.split()])

	return worldMaze

def printMaze(worldMaze):
	print("Maze:")
	for i in worldMaze:
		print i

def printHeuristic(h):
	print("")
	if h == 1:
		print("Heuristic: Manhattan")
	elif h == 2:
		print("Heuristic: Custom")


if __name__ == "__main__":
	(worldMaze, heuristic) = getArgs()
	printMaze(worldMaze)
	printHeuristic(heuristic)
	print ("\n-----------------------------------\n")
