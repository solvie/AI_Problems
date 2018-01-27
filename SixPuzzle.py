# SIX PUZZLE - Solving with Uninformed Searches
#
# Zero represents the empty slot
# Maintains closed list to store every expanded node so that we don't repeat states.
#
# 1. BFS
# 2. Uniform cost search
# 3. DFS
# 4. Iterative Deepening
#
# Solvie Lee 
# McGill University 

from copy import deepcopy

initialState = [[1,4,2], [5,3,0]], (1,2)
goalState = [[0,1,2],[5,4,3]], (0,0)


def appendStateToListIfLegal(puzzleState, zeroPosition, newZeroPosition, listToAppend, alreadyVisitedStates):
	tempPuzzleStateMatrix = deepcopy(puzzleState[0])
	numberMoved = tempPuzzleStateMatrix[newZeroPosition[0]][newZeroPosition[1]]
	tempPuzzleStateMatrix[zeroPosition[0]][zeroPosition[1]] = numberMoved
	tempPuzzleStateMatrix[newZeroPosition[0]][newZeroPosition[1]] = 0
	if (tempPuzzleStateMatrix,newZeroPosition) not in alreadyVisitedStates:
		listToAppend.append((numberMoved,(tempPuzzleStateMatrix,newZeroPosition)))

def expandNode(puzzleState, alreadyVisitedStates):
	puzzleStateMatrix, zeroPosition = puzzleState[0], puzzleState[1]
	#Generate a list of the next states, checking that they are legal, and that the state hasn't already been visited
	nextStates = [] # initialize list of next States to be returned

	if zeroPosition[0]-1>=0: #check if we can switch zero with UP
		appendStateToListIfLegal(puzzleState, zeroPosition, (zeroPosition[0]-1, zeroPosition[1]), nextStates,alreadyVisitedStates)

	if zeroPosition[0]+1<len(puzzleStateMatrix): #check if we can switch zero with DOWN,  len(puzzleStateMatrix)=numRows
		appendStateToListIfLegal(puzzleState, zeroPosition, (zeroPosition[0]+1, zeroPosition[1]), nextStates,alreadyVisitedStates)

	if zeroPosition[1]-1>=0: #check if we can switch zero with LEFT  len(puzzleStateMatrix)=numCols
		appendStateToListIfLegal(puzzleState, zeroPosition, (zeroPosition[0], zeroPosition[1]-1), nextStates,alreadyVisitedStates)

	if zeroPosition[1]+1<len(puzzleStateMatrix[0]): #check if we can switch zero with RIGHT
		appendStateToListIfLegal(puzzleState, zeroPosition, (zeroPosition[0], zeroPosition[1]+1), nextStates,alreadyVisitedStates)

	return nextStates

def dfs(startState, goalState): # return the results as a list
	alreadyVisitedStates = []
	stack = [startState]
	while stack:
		alreadyVisitedStates.append(deepcopy(stack[-1])) #peek at the top of the stack, add it to visited
		nextPossibleStates = expandNode(deepcopy(stack[-1]), alreadyVisitedStates) #expand the node to find the possible next state
		
		minValue = 1000 #arbitrarily large value. 
		if not nextPossibleStates: # if there are no more possible states, dead end. Pop the stack.
			stack.pop()
		else:
			for tileMoved, puzzleState in nextPossibleStates:
				puzzleStateMatrix, zeroPosition = puzzleState[0], puzzleState[1]
				if puzzleState ==goalState: # if it is the goal state, return the stack
					stack.append(deepcopy(puzzleState))
					return stack
				else: # if it is not the goal state, check if its the min, and push that one onto the stack
					if tileMoved<minValue:
						minValue = tileMoved
						minMovedState = puzzleState
			stack.append(deepcopy(minMovedState))
	return 'goal not found'

