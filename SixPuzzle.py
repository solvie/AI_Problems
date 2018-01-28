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

def constructBFSPathFromVisited(allVisitedStatesNParents, startState, goalState):
	path = [] 
	currentState = goalState
	path.append(goalState)
	while currentState != startState:
		for stateAndParent in allVisitedStatesNParents[:]:
			if stateAndParent[0] == currentState:
				currentState= stateAndParent[1]
				allVisitedStatesNParents.remove(stateAndParent)
				path.insert(0,currentState) # insert into beginning of array
	return path

# Breadth First Search
def getBFSSolution(startState, goalState):
	alreadyVisitedStates = []
	alreadyVisitedStatesNParents = []
	queue = [(startState, None)] 
	while queue:
		currentTuple = deepcopy(queue[0])
		alreadyVisitedStatesNParents.append(deepcopy(currentTuple))
		if queue[0][0] ==goalState:
			return constructBFSPathFromVisited(alreadyVisitedStatesNParents, startState, goalState)
		
		alreadyVisitedStates.append(deepcopy(currentTuple[0])) #peek at the front of the queue, add it to visited
		nextPossibleStates = expandNode(currentTuple[0], alreadyVisitedStates) #expand the node to find the possible next state
		if nextPossibleStates: # dead end has been reached, dequeue
			tupleListToBeSorted = []
			for tileMoved, puzzleState in nextPossibleStates:
				puzzleStateMatrix, zeroPosition = puzzleState[0], puzzleState[1]
				tupleListToBeSorted.append((tileMoved, deepcopy(puzzleState)))
			tupleListToBeSorted.sort(key=lambda tup: tup[0]) # sort so that lower moves go first
			for tileMoved, state in tupleListToBeSorted:
				queue.append((deepcopy(state),deepcopy(currentTuple[0])))
		queue.pop(0) # dequeue what was just worked on. 
	return 'Ran BFS, goal not found'

#Depth First Search
def getDFSSolution(startState, goalState): # return the results as a list
	alreadyVisitedStates = [] #includes states
	stack = [startState]
	while stack:
		if stack[-1] ==goalState:
			return stack
		alreadyVisitedStates.append(deepcopy(stack[-1])) #peek at the top of the stack, add it to visited
		nextPossibleStates = expandNode(deepcopy(stack[-1]), alreadyVisitedStates) #expand the node to find the possible next state
		minValue = len(initialState[0])*len(initialState[0][0]) #set initial minValue to larger than largest on puzzle
		if not nextPossibleStates: # Dead end reached. Pop the stack.
			stack.pop()
		else:
			for tileMoved, puzzleState in nextPossibleStates:
				puzzleStateMatrix, zeroPosition = puzzleState[0], puzzleState[1]
				if tileMoved<minValue:
					minValue = tileMoved
					minMovedState = puzzleState
			stack.append(deepcopy(minMovedState))
	return 'Ran DFS, goal not found'

# Iterative Deepening Search
def getIDSSolution(startState, goalState):
	depthLimit =1
	alreadyVisitedStates = [] #includes states
	stack = [startState]
	while True:
		while stack:
			if stack[-1] ==goalState:
				return stack
			alreadyVisitedStates.append(deepcopy(stack[-1])) #peek at the top of the stack, add it to visited
			nextPossibleStates = expandNode(deepcopy(stack[-1]), alreadyVisitedStates) #expand the node to find the possible next state
			minValue = len(initialState[0])*len(initialState[0][0]) #set initial minValue to larger than largest on puzzle
			if not nextPossibleStates or len(stack) == depthLimit: # Dead end reached, OR the depth limit has been reached. Pop the stack.
				stack.pop()
			else:
				for tileMoved, puzzleState in nextPossibleStates:
					puzzleStateMatrix, zeroPosition = puzzleState[0], puzzleState[1]
					if tileMoved<minValue:
						minValue = tileMoved
						minMovedState = puzzleState
				stack.append(deepcopy(minMovedState))
		# Reinitialize and increase depth limit
		alreadyVisitedStates = []
		stack = [startState] 
		depthLimit+=1
	return 'Ran IDS, goal not found'

