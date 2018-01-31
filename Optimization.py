# Optimization - Hill-climbing and Simulated Annealing
#
# The function in question:
# y = sin(x^2/2)/log_2(x+4)
#
# Solvie Lee 
# McGill University

import math
import random
#import matplotlib.pyplot as plt
import csv
import seaborn as sns
import pandas as pd
import numpy as np
 

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
def twoDHillClimbing(step_size, startPoint, xmin, xmax, ):
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

def simulatedAnnealing(step_size, startPoint, xmin, xmax, temperature):
	x = startPoint
	numsteps = 0
	time = 0
	frozen = False
	steady = False
	steadyval = None
	steadycount = 0
	while True:
		temperature = 0.9999*temperature
		if round(temperature, 5)==0:
			frozen = True
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
		numsteps+=1
		if randomNeighbor[1] > y:
			x = randomNeighbor[0]
			y = randomNeighbor[1]
		else:
			if steadyval ==y:
				steadycount+=1
			else:
				steadyval = y
				steadycount=0
			if steadycount>100 and frozen:
				break
			if random.uniform(0,1)<math.exp((-y+randomNeighbor[1])/temperature):
				x = randomNeighbor[0]
				y = randomNeighbor[1]		
	return ((round(x,2),round(y, 5)), (step_size,numsteps))

def writeCompleteCsvTableHillCli(title, motherarray):
	with open(title,'w') as csvfile:
		fieldnames=['Start index', 'Step size', 'x', 'y', 'Steps to convergence']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for i in range (0,len(motherarray)):
			childarray = motherarray[i]
			for positionTuple, stepTuple in childarray:
				writer.writerow({'Start index': i ,'Step size': stepTuple[0] ,'x': positionTuple[0], 'y': positionTuple[1], 'Steps to convergence': stepTuple[1]})

def writeCompleteCsvTableSimAnn(title, motherarray):
	with open(title,'w') as csvfile:
		fieldnames=['Start index', 'Step size', 'x', 'y', 'Steps to convergence']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for i in range (0,len(motherarray)):
			childarray = motherarray[i]
			for positionTuple, stepTuple in childarray:
				writer.writerow({'Start index': i ,'Step size': stepTuple[0] ,'x': positionTuple[0], 'y': positionTuple[1], 'Steps to convergence': stepTuple[1]})


def saveFunctionPlot():
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
	plt.figure()
	plt.plot(xvals,yvals)
	plt.axis([0, 10, -1, 1])
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('Graph of function y = sin(x^2/2)/log_2(x+4)')
	plt.savefig('functiongraph.svg')

def hillClimbingResults(writeCSV):
	currentIndex=0
	currentStep=0.01
	motherArray=[] #motherArray[i] indicates values for starting point = i
	while currentIndex <=10:
		subArray = []
		while currentStep <=0.1:
			subArray.append(twoDHillClimbing(currentStep, currentIndex,0,10))
			currentStep+=0.01
		currentIndex+=1
		currentStep=0.01
		motherArray.append(subArray)
	if writeCSV:
		writeCompleteCsvTable('allresults_hill-climbing.csv', motherArray)
	return motherArray


def simulatedAnnealingResults(temperatures, generateCSV):
	currentStep=0.02
	motherArray=[] 
	for temperature in temperatures:
		subArray = []
		for iteration in range (1,10):
			subArray.append(simulatedAnnealing(currentStep, 5,0,10, temperature))
		motherArray.append(subArray)
	return motherArray
# simulatedAnnealingResults([0.01,0.1, 1,5,10,20])
#apple = simulatedAnnealingResults([1,5,10])

def findMaxConvergeValuesForEach(array): #prints in latex format
	for index in range (0,10):
		maxtup = array[index][0][0]
		maxval = array[index][0][0][1] #y val
		for positionTuple, stepTuple in array[index]:
			if positionTuple[1]>maxval:
				maxval = positionTuple[1]
				maxtup = positionTuple
		print(str(index) + " & " + str(maxtup[0]) + " & " + str(maxtup[1])+"\\\\")

def findUniqueVals(inputarray):
	retarray = []
	for array in inputarray:
		for tuptup in array:
			if tuptup[0] not in retarray:
				print('adding')
				retarray.append(tuptup[0])
	retarray.sort(key=lambda tup: tup[0])
	return retarray

def generateHeatmapTableSimAnn(temperatures, resultsarray):
	with open('heatmap','w') as csvfile:
		fieldnames=['Temperature']
		vals = findUniqueVals(resultsarray)
		for i in range (0, len(vals)):
			fieldnames.append(str(vals[i]))
		print(fieldnames)

		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		i =0
		for temp in temperatures:
			dictionary={}
			dictionary['Temperature']= temp
			for val in vals:#initialize dictionary
				dictionary[str(val)] = 0
			childarray = resultsarray[i]
			for positionTuple, stepTuple in childarray:
				for val in vals:
					if positionTuple[1]==val[1]:
						dictionary[str(val)] = dictionary[str(val)]+1
			print(temp)
			print(dictionary)
			writer.writerow(dictionary)
			i+=1




