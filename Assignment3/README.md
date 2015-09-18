# CSCI 3202: Artificial Intelligence - Assignment 3
# By Brennan McConnell
## Running Maze.py
Execute the following command:
```
python Maze.py <fileName> <heuristic>
```
<heuristic> is either a 1 to represent the Manhattan Heuristic 
or 2 to represent my Custom Heuristic


## My heuristic
### Equations and Logistics
My heuristic is very straightforward and logical. Simply put, a mountain is ignored when moving
diagonally unless the next diagonal move beyond that is also a mountain in which case a very 
large penalty occurs. On top of this, the original Manhattan heuristic is also 
still put into place because it provides a logical movement that moving diagonal is 
cheaper than 2 horizontal/vertical moves.
```
hCost = 0
if isMountain == 1 and worldMaze[self.location[0]][self.location[1]] == 1:
	hCost += 100
elif isMountain == 1 and stepDistance == 2: # stepDistance == 2 signifies a diagonal move
	# Previously added 10 since it was a mountain, so line below is just resetting the cost.
	hCost -= 10
self.distanceToStart += abs(endP[0] - self.location[0]) + abs(endP[1] - self.location[1]) + hCost
```
As can be seen above, when moving diagonally, mountains will be ignored except for the case
in which two diagonal mountains occur in a row. And diagonal moves are still preferred over
horizontal and vertical moves through the Manhattan Heuristic. It is important to note 
that mountains are not ignored when moving vertically and horizontally, because this would be
ignorant.

### Motivation and Reasoning
The reason I chose my heuristic is simply based on the fact that the penalty incurred
for a diagonal mountain move is irrelevant unless two moves are made in the same row.
For example, if there is one mountain and you perform two diagonal moves to cross it. 
The cost is 14+14+10 = 38, and moving around it with 2 vertical and 2 horizontal moves
would cost 40. Thus it is preferable to ignore the fact that this object exists and continue
to assume (based on the Manhattan heuristic) that we want to choose diagonal moves over
vertical/horizontal. However in the case that two mountains are placed in a row diagonally,
the benefit is lost because the taxation of mountain crossing finally catches up with us. 
For example, now the cost to move across 2 mountains diagonally = 14 + 14 + 14 + 10 + 10 = 62,
whilst simply performing vertical/horizontal moves around this would result in a cost equal to 
60 for 3 vertical and 3 horizontal moves. This tradeoff only gets worse as more diagonal mountains
are placed in a row. Thus the goal of my heuristic is to always move diagonally, even if a
mountain is in the way EXCEPT if you will do 2 diagonal mountains in a row. Therefore I capitalize 
on the fact that objects are irrelevant under certain circumstances and do not always
have to be considered.

### Performance and Results
My custom heuristic tied with the Manhattan heuristic in world 1 (although it evaluated 1 less node).
This is because my heuristic still uses the Manhattan as a base to make sure diagonals are preferred, and
world 1 is not suited to my heuristics advantage. World 1 contains no areas in which two diagonal mountains
are next to each other nor do mountains really get in the way in world 1 of the already optimal path. In world 2, my heuristic did indeed outperform by a cost of 2 and it evaluated 6 less nodes. While the advantage did
not arise because we ignored a mountain, it arose because we avoided doing a double diagonal mountain move
that the orignal Manhattan heuristic made. Ultimately, I am confident that my custom heuristic will outperform
the Manhattan heuristic in all aspects simply because it modifies the original manhattan in an important way.


## Output Of Maze.py
### Note - To view in the correct format, view the raw file (original README source), or run Maze.py

### World 1: Manhattan Heuristic
-----------------------------------

Heuristic: Manhattan

Total Heuristic cost:  211
Total Cost:  130
Nodes Evaluted:  62

Path:
(7, 0) with heuristic cost 0
(7, 1) with heuristic cost 25
(7, 2) with heuristic cost 49
(6, 3) with heuristic cost 75
(5, 3) with heuristic cost 96
(4, 4) with heuristic cost 118
(3, 5) with heuristic cost 139
(3, 6) with heuristic cost 155
(3, 7) with heuristic cost 170
(2, 8) with heuristic cost 186
(1, 9) with heuristic cost 201
(0, 9) with heuristic cost 211

Path:
0 0 0 0 1 0 1 1 0 X
2 2 1 1 0 0 2 0 2 X
0 0 0 0 0 0 2 0 X 0
2 0 2 2 0 X X X 2 0
0 0 2 0 X 2 1 0 1 0
0 0 2 X 0 2 0 0 2 0
0 0 2 X 1 2 0 1 2 2
X X X 0 0 0 0 0 0 0

-----------------------------------



### World 1: Custom Heuristic
-----------------------------------

Heuristic: Custom

Total Heuristic cost:  211
Total Cost:  130
Nodes Evaluted:  61

Path:
(7, 0) with heuristic cost 0
(7, 1) with heuristic cost 25
(7, 2) with heuristic cost 49
(6, 3) with heuristic cost 75
(5, 3) with heuristic cost 96
(4, 4) with heuristic cost 118
(3, 5) with heuristic cost 139
(3, 6) with heuristic cost 155
(3, 7) with heuristic cost 170
(2, 8) with heuristic cost 186
(1, 9) with heuristic cost 201
(0, 9) with heuristic cost 211

Path:
0 0 0 0 1 0 1 1 0 X
2 2 1 1 0 0 2 0 2 X
0 0 0 0 0 0 2 0 X 0
2 0 2 2 0 X X X 2 0
0 0 2 0 X 2 1 0 1 0
0 0 2 X 0 2 0 0 2 0
0 0 2 X 1 2 0 1 2 2
X X X 0 0 0 0 0 0 0

-----------------------------------



### World 2: Manhattan Heuristic
-----------------------------------

Heuristic: Manhattan

Total Heuristic cost:  224
Total Cost:  144
Nodes Evaluted:  60

Path:
(7, 0) with heuristic cost 0
(7, 1) with heuristic cost 25
(7, 2) with heuristic cost 49
(6, 3) with heuristic cost 75
(5, 3) with heuristic cost 96
(4, 4) with heuristic cost 119
(3, 5) with heuristic cost 140
(3, 6) with heuristic cost 156
(2, 7) with heuristic cost 184
(1, 8) with heuristic cost 210
(0, 9) with heuristic cost 224

Path:
0 0 0 0 0 0 0 0 0 X
2 2 1 1 0 2 2 1 X 0
0 0 0 0 0 2 2 X 1 0
2 2 2 2 0 X X 1 1 0
0 0 0 0 X 2 1 1 1 0
0 2 2 X 2 2 0 0 2 0
0 0 2 X 1 2 0 1 2 2
X X X 0 0 0 0 0 0 0

-----------------------------------



### World 2: Custom Heuristic
-----------------------------------

Heuristic: Custom

Total Heuristic cost:  234
Total Cost:  142
Nodes Evaluted:  54

Path:
(7, 0) with heuristic cost 0
(6, 0) with heuristic cost 25
(5, 0) with heuristic cost 49
(4, 1) with heuristic cost 75
(4, 2) with heuristic cost 96
(4, 3) with heuristic cost 116
(3, 4) with heuristic cost 137
(2, 4) with heuristic cost 154
(1, 4) with heuristic cost 170
(0, 5) with heuristic cost 188
(0, 6) with heuristic cost 201
(0, 7) with heuristic cost 213
(0, 8) with heuristic cost 224
(0, 9) with heuristic cost 234

Path:
0 0 0 0 0 X X X X X
2 2 1 1 X 2 2 1 1 0
0 0 0 0 X 2 2 1 1 0
2 2 2 2 X 0 0 1 1 0
0 X X X 0 2 1 1 1 0
X 2 2 0 2 2 0 0 2 0
X 0 2 0 1 2 0 1 2 2
X 0 0 0 0 0 0 0 0 0

-----------------------------------
