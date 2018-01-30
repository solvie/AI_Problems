# Optimization - Hill-climbing and Simulated Annealing
#
# y = sin(x^2/2)/log_2(x+4)
#
# Solvie Lee 
# McGill University

import math
import random
import matplotlib.pyplot as plt
import csv

def applyEquation(x):
	return math.sin(x*x/2.0)/math.log(x+4,2)

def findMaxReturnIndex(arrayOfTuples):
	maxvar = arrayOfTuples[0][1]
	maxtup = arrayOfTuples[0]
	for tup in arrayOfTuples:
		if tup[1] > maxvar:
			maxvar = tup[1]
			maxtup = tup
	return maxtup


#x min and xmax constrains the search to a certain domain
def TwoDHillClimbing(step_size, startPoint, xmin, xmax, ):
	x = startPoint
	numsteps = 0
	while True:
		neighbors=[] #tuples with index, value
		xleft = x-step_size
		if xleft >= xmin:
			neighbors.append((xleft, applyEquation(xleft)))
		xright = x+step_size
		if xright <=xmax:
			neighbors.append((xright,applyEquation(xright)))
		y = applyEquation(x)

		bestSuccessor = findMaxReturnIndex(neighbors)
		if bestSuccessor[1] <= y:
			return ((round(x,2),round(y, 5)), (step_size,numsteps))
		x = bestSuccessor[0]		
		numsteps+=1
	print('something went wrong')
	return None

def simulatedAnnealing(step_size, startPoint, xmin, xmax, temperature, runtime):
	x = startPoint
	numsteps = 0
	time = 0
	while time < runtime:
		temperature = 0.999*temperature
		# print('temperature')
		# print(temperature)
		time+=1
		randomNeighbor = None
		neighbors = []
		xleft = x-step_size
		if xleft >= xmin:
			neighbors.append((xleft, applyEquation(xleft)))
		xright = x+step_size
		if xright <=xmax:
			neighbors.append((xright,applyEquation(xright)))
		if len(neighbors)==1:
			randomNeighbor = neighbors[0]
		else:
			randomNeighbor = neighbors[int(round(random.uniform(0,1),0))]
		y = applyEquation(x)
		# if time <200 or time%500==0:
			# print('temp&the math')
			# print(temperature)
			# print((-y+randomNeighbor[1]))
			# print(math.exp(-abs(y-randomNeighbor[1])/temperature))
		if randomNeighbor[1] > y or random.uniform(0,1)<math.exp((-y+randomNeighbor[1])/temperature):
			# print('CHOOSING TO MOVE')
			# print((-y+randomNeighbor[1]))
			# print(math.exp(-abs(y-randomNeighbor[1])/temperature))
			x = randomNeighbor[0]
			y = randomNeighbor[1]
		else:
			# print('nah we aint picking this this')
			continue	
		numsteps+=1
	return ((round(x,2),round(y, 5)), (step_size,numsteps))

def writeCompleteCsvTable(title, motherarray):
	with open(title,'w') as csvfile:
		fieldnames=['Start index', 'Step size', 'x', 'y', 'Steps to convergence']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for i in range (0,len(motherarray)):
			childarray = motherarray[i]
			for positionTuple, stepTuple in childarray:
				writer.writerow({'Start index': i ,'Step size': stepTuple[0] ,'x': positionTuple[0], 'y': positionTuple[1], 'Steps to convergence': stepTuple[1]})


xvals=[]
yvals=[]
step_size = 0.01
i=0
x=0

while x <= 10:
	x = i*step_size
	xvals.append(x)
	yvals.append(applyEquation(x))
	i+=1

#plt.figure()
#plt.plot(xvals,yvals)
plt.axis([0, 10, -1, 1])
plt.xlabel('x')
plt.ylabel('y')
plt.title('Graph of function y = sin(x^2/2)/log_2(x+4)')
#plt.savefig('functiongraph.svg')


# currentIndex=0
# currentStep=0.01
# motherArray=[] #motherArray[i] indicates values for starting point = i
# while currentIndex <=10:
# 	subArray = []
# 	while currentStep <=0.1:
# 		subArray.append(TwoDHillClimbing(currentStep, currentIndex,0,10))
# 		currentStep+=0.01
# 	currentIndex+=1
# 	currentStep=0.01
# 	motherArray.append(subArray)
# print('motherarray')
# print(motherArray)
# writeCompleteCsvTable('allresults_hill-climbing.csv', motherArray)


currentIndex=0
currentStep=0.05
motherArray=[] #motherArray[i] indicates values for starting point = i
# while currentIndex <=10:
subArray = []
for temperature in [0.03,1,5,10]:#,1, 5,10]:#,1,1000,1000000,1000000000]:#,0.03,0.04]:
	subArray = []
	print('temp')
	print(temperature)
	for iteration in range (1,10):
		subArray.append(simulatedAnnealing(currentStep, 5,0,10, temperature, 1000000))
	# currentIndex+=1
	# currentStep=0.01
	print(subArray)
motherArray.append(subArray)
print('motherarray')
# print(motherArray)


#plt.figure()
plt.plot(xvals,yvals)
plt.xlabel('Steps to convergence')
plt.ylabel('y')
plt.title('Graph starting at 0')


