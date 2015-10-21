# CSCI 3202: Artificial Intelligence - Assignment 5
# By Brennan McConnell
## Running MDP.py
Execute the following command:
```
python MDP.py <fileName> <epsilon>
```

##Answers to Questions
Utimately, no value of epsilon changed the optimal path taken. With that being said
the Move Policy did change based on epsilon values. This really would only matter
if our starting position was in a different location. But, the optimal path from
the starting position (0,0) never changes. The Move Policy changed when epsilon 
was greater than 20.2. I tried multiple epsilon values until I encoutered this change. 
My explanation for this change is straightforward, since our epsilon is higher, we will
stop iterating sooner due to the fact that delta (the biggest change) will now not be large
enough to signify that we might continue to converge on an answer should we keep iterating.
Thus we allow for a larger 'error'. As we get smaller with our epsilon and we allow less error,
(and force our program to keep iterating until almost no changes are being applied to the utilities),
we converge on the most optimal path. Thus when our epsilon is 20.2 and the Move Policy changes, this
is simply because we stopped iterating early and had too large of an error allowed and
we could have narrowed it down more by selecting a better epsilon, such as 0.5 like we do for our example.

## Output Of MDP.py
### Note - To view in the correct format, view the raw file (original README source), or run MDP.py

### World 1.txt
-----------------------------------


Solving the maze with epsilon value: 0.5
Finished calculations...


Optimal Path:
Coordinates in (x, y) format.
(0, 0) - Utility: 0.792984681064 - Direction: U
(0, 1) - Utility: 0.983170211162 - Direction: U
(0, 2) - Utility: 1.51540129824 - Direction: U
(0, 3) - Utility: 2.09308802252 - Direction: R
(1, 3) - Utility: 2.71770959917 - Direction: U
(1, 4) - Utility: 3.51304469172 - Direction: U
(1, 5) - Utility: 3.49033984961 - Direction: R
(2, 5) - Utility: 4.40862795591 - Direction: R
(3, 5) - Utility: 5.57424345649 - Direction: R
(4, 5) - Utility: 6.96637838652 - Direction: U
(4, 6) - Utility: 8.36327516163 - Direction: U
(4, 7) - Utility: 9.74680974852 - Direction: R
(5, 7) - Utility: 13.8808198928 - Direction: R
(6, 7) - Utility: 18.1856286505 - Direction: R
(7, 7) - Utility: 26.646706459 - Direction: R
(8, 7) - Utility: 36.0 - Direction: R
(9, 7) - Utility: 50 - Direction: *



Move Policy:
R R R R R R R R R *
W W R R U U W U W U
R R R R U U W R R U
W U W W R R R U W U
R U W R U W U U R U
U U W R U W R U W U
U L W U U W U U W W
U R R R R R U U L L

-----------------------------------
