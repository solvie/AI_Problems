# SIX PUZZLE - Solving with Uninformed Searches
#
# Maintains closed list to store every expanded node so that we don't repeat states.
#
# 1. BFS
# 2. Uniform cost search
# 3. DFS
# 4. Iterative Deepening
#
# Solvie Lee 
# McGill University 

# Define initial and goal states
#
# Each state is a tuple of the six puzzle state as a matrix,
# and the position of the zero within it.
from copy import deepcopy

initialState = [[1,4,2], [5,3,0]], (1,2)
goalState = [[0,1,2],[5,4,3]], (0,0)

alreadyVisitedStates=[]

def appendToListIfLegal(puzzleStateMatrix, zeroPosition, newZeroPosition, listToAppend):
	tempPuzzleStateMatrix = copy.deepcopy(puzzleStateMatrix)
	tempPuzzleStateMatrix[zeroPosition[0]][zeroPosition[1]] = puzzleStateMatrix[newZeroPosition[0]][newZeroPosition[1]]
	tempPuzzleStateMatrix[newZeroPosition[0]][newZeroPosition[1]] = 0
	if tempPuzzleStateMatrix not in alreadyVisitedStates:
		listToAppend.append((tempPuzzleStateMatrix,newZeroPosition))

def findAdjacentStates(puzzleState, alreadyVisitedStates):
	# based on the number of rows and columns
	puzzleStateMatrix, zeroPosition = puzzleState[0], puzzleState[1]

	numRows = len(puzzleStateMatrix) # necessary to determine illegal operators
	numCols = len(puzzleStateMatrix[0])

	#Generate a list of the next states, checking that they are legal, and that the state hasn't already been visited
	nextStates = [] # initialize list of next States to be returned

	if zeroPosition[0]-1>=0: #check if we can switch zero with UP
		appendToListIfLegal(puzzleStateMatrix, zeroPosition, (zeroPosition[0]-1, zeroPosition[1]), nextStates)

	if zeroPosition[0]+1<numRows: #check if we can switch zero with DOWN
		appendToListIfLegal(puzzleStateMatrix, zeroPosition, (zeroPosition[0]+1, zeroPosition[1]), nextStates)

	if zeroPosition[1]-1>=0: #check if we can switch zero with LEFT
		appendToListIfLegal(puzzleStateMatrix, zeroPosition, (zeroPosition[0], zeroPosition[1]-1), nextStates)

	if zeroPosition[1]+1<numCols: #check if we can switch zero with RIGHT
		appendToListIfLegal(puzzleStateMatrix, zeroPosition, (zeroPosition[0], zeroPosition[1]+1), nextStates)

	return nextStates


