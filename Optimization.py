# Optimization - Hill-climbing and Simulated Annealing
#
# y = sin(x^2/2)/log_2(x+4)
#
# Solvie Lee 
# McGill University

import math
import matplotlib.pyplot as plt

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
def TwoDHillClimbing(step_size, startPoint, xmin, xmax):
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
			return (round(x,2),round(y, 5), numsteps) #index, convergence value, numsteps
		x = bestSuccessor[0]		
		numsteps+=1
	print('something went wrong')
	return None


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


currentIndex=0
currentStep=0.01
motherArray=[] #motherArray[i] indicates values for starting point = i
while currentIndex <=10:
	subArray = []
	while currentStep <=0.1:#tab me
		subArray.append(TwoDHillClimbing(currentStep, currentIndex,0,10))
		currentStep+=0.01
	currentIndex+=1
	currentStep=0.01
	motherArray.append(subArray)#tab me
print(currentIndex)
print('motherarray 0')
print(motherArray[1])

#plt.figure()
plt.plot(xvals,yvals)
plt.xlabel('Steps to convergence')
plt.ylabel('y')
plt.title('Graph starting at 0')


