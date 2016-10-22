from enum import Enum
import time
import copy

class sitch(Enum):
	across = 1
	down = 2

class Assignment:
	row = 0 #row of first letter
	col = 0 #col of first letter
	word = ""
	sitchType = sitch.across


	def __init__(self, row=0, col=0, word="", sitchType=sitch.across):
		self.row = row
		self.col = col
		self.word = word
		self.sitchType = sitchType

initGrid = [] #(row,col) order
Words = [] #(word,sitch)
assignments = [] #Array<Assignment>
Domain = {} #[word]=[(0,0),(0,1)...]list of coords it can go
Assigned = {}

def readInput(inputNum):
	with open('data/bank'+str(inputNum)+'.txt') as input_file:
		for i, line in enumerate(input_file):
			w = line.rstrip().upper()
			Words.append(w)
			Domain[w]=[]
			Assigned[w]=False
	with open('data/grid'+str(inputNum)+'.txt') as input_file:
		for i, line in enumerate(input_file):
			row = []
			line = line.rstrip()
			for character in line: 
				row.append(character)
			initGrid.append(row)

def buildGridFromAssignment():
	currGrid = copy.deepcopy(initGrid)
	for a in assignments:
		word = a.word
		if a.sitchType==sitch.across:
			wordPos = 0
			if a.col+len(word)>9:
				return False
			for i in range(a.col,a.col+len(word)):
				if currGrid[a.row][i]!='_' and currGrid[a.row][i]!=word[wordPos]:
					return False
				currGrid[a.row][i]=word[wordPos]
				wordPos+=1
		elif a.sitchType==sitch.down:
			wordPos = 0
			if a.row+len(word)>9:
				return False
			for i in range(a.row,a.row+len(word)):
				if currGrid[i][a.col]!='_' and currGrid[i][a.col]!=word[wordPos]:
					return False
				currGrid[i][a.col]=word[wordPos]
				wordPos+=1
	return currGrid

def check3x3(currGrid):
	for row in range(0,9,3):
		for col in range(0,9,3):
			letters = {}
			for r in range(row,row+3):
				for c in range(col,col+3):
					l = currGrid[r][c]
					if l != '_' and l in letters:
						return False
					if l != '_':
						letters[l]=True

	return True

def checkRows(currGrid):
	for r in range(0,9):
		letters = {}
		for c in range(0,9):
			l = currGrid[r][c]
			if l != '_' and l in letters:
				return False
			if l != '_':
				letters[l]=True
	return True

def checkCols(currGrid):
	for c in range(0,9):
		letters = {}
		for r in range(0,9):
			l = currGrid[r][c]
			if l != '_' and l in letters:
				return False
			if l != '_':
				letters[l]=True
	return True

def isConsistent():
	currGrid = buildGridFromAssignment()
	if currGrid == False:
		return False
	return (check3x3(currGrid) and checkRows(currGrid) and checkCols(currGrid))

def printSolution():
	solutionGrid = buildGridFromAssignment()
	for row in range(9):
		for col in range(9):
			print solutionGrid[row][col],
		print ''

#returns the next word variable that will be assigned a coordinate
def chooseNextVariable():
	global Words
	for word in Words:
		if Assigned[word]==False:
			return word
	return True

def populateDomain():
	for word in Domain.keys():#Possbible locations for accross
		for row in range(9):
			for col in range(10-len(word)):
				Domain[word].append((row,col))
		for col in range(9):#Possible locations for down
			for row in range(10-len(word)):
				if (row,col) not in Domain[word]:
					Domain[word].append((row,col))

def BackTrace():
	if chooseNextVariable()==True:
		return True
	word = chooseNextVariable()
	for coord in Domain[word]:
		assignment = Assignment(coord[0],coord[1],word,sitch.across)
		assignments.append(assignment)
		if isConsistent():
			Assigned[word]=True
			result = BackTrace()
			if result:
				return True
			else:
				assignments.remove(assignment)
				Assigned[word]=False
		else:
			assignments.remove(assignment)
			assignment = Assignment(coord[0],coord[1],word,sitch.down)
			assignments.append(assignment)
			if isConsistent():
				Assigned[word]=True
				result = BackTrace()
				if result:
					return True
				else:
					assignments.remove(assignment)
					Assigned[word]=False
			else:
				assignments.remove(assignment)
	return False

start_time = time.time()
readInput(2)
Words.sort(lambda x,y: cmp(len(y),len(x)))
populateDomain()
BackTrace()
printSolution()
print("Time: %s seconds" % (time.time() - start_time))