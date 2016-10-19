from enum import Enum
import time
import copy

class sitch(Enum):
	accross = 1
	down = 2

class Assignment:
	row = 0 #row of first letter
	col = 0 #col of first letter
	word = ""
	sitchType = sitch.accross
	shiftBack = 0

	def __init__(self, row=0, col=0, word="", sitchType=sitch.accross,shiftBack=0):
		self.row = row
		self.col = col
		self.word = word
		self.sitchType = sitchType
		self.shiftBack = shiftBack

initGrid = [] #(row,col) order
Domain = [] #(word,sitch)
assignments = [] #Array<Assignment>
Domains = []



def readInput(inputNum):
	with open('data/bank'+str(inputNum)+'.txt') as input_file:
		for i, line in enumerate(input_file):
			Domain.append(line.rstrip().upper())
	with open('data/grid'+str(inputNum)+'.txt') as input_file:
		for i, line in enumerate(input_file):
			row = []
			line = line.rstrip()
			for character in line: 
				row.append(character)
			initGrid.append(row)

def buildBlankGrid():
	currGrid = []
	for i in range(9):
		gridrow = []
		for j in range(9):
			gridrow.append('_')
		currGrid.append(gridrow)
	return currGrid

def buildGridFromAssignment():
	currGrid = copy.deepcopy(initGrid)
	# currGrid = buildBlankGrid()
	for a in assignments:
		word = a.word
		if a.sitchType==sitch.accross:
			wordPos = 0
			col = a.col
			for i in range(col,col+len(word)):
				currGrid[a.row][i]=word[wordPos]
				wordPos+=1
		elif a.sitchType==sitch.down:
			wordPos = 0
			row = a.row
			for i in range(row,row+len(word)):
				currGrid[i][a.col]=word[wordPos]
				wordPos+=1
	print currGrid
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

#returns the next blank space
def chooseNextVariable(prev_row,prev_col):
	currGrid = buildGridFromAssignment()
	for i in range(9):
		for j in range(9):
			if currGrid[i][j]=='_':
				print (i,j)
				return (i,j)
	return True


def BackTrace(row,col):
	currGrid = buildGridFromAssignment()
	if len(assignments)>17:
		return True
	for word in reversed(Domain):
		shifts = []
		for shift in range(len(word)):
			tempCol = col - shift
			if tempCol >= 0 and tempCol + len(word) <= 9:
				shouldAdd = True
				wordPos = 0
				for c in range(tempCol,tempCol+len(word)):
					if currGrid[row][c]!='_' and currGrid[row][c]!=word[wordPos]:
						shouldAdd = False
						break
					wordPos+=1
				if shouldAdd:
					valAssignment = Assignment(row,tempCol,word,sitch.accross)
					shifts.append(valAssignment)


			tempRow = row - shift
			if tempRow >= 0 and tempRow + len(word) <= 9:
				shouldAdd = True
				wordPos = 0
				for r in range(tempRow,tempRow+len(word)):
					if currGrid[r][col]!='_' and currGrid[r][col]!=word[wordPos]:
						shouldAdd = False
						break
					wordPos+=1
				if shouldAdd:
					valAssignment = Assignment(tempRow,col,word,sitch.down)
					shifts.append(valAssignment)
		for assignment in shifts:
			assignments.append(assignment)
			if isConsistent():
				Domain.remove(word)
				print row, col
				varCoord = chooseNextVariable(row,col)
				print varCoord
				if varCoord == True:
					return True
				result = BackTrace(varCoord[0],varCoord[1])
				if result:
					return True
				if result == False:
					assignments.remove(assignment)
					Domain.append(word)
			else:
				assignments.remove(assignment)
	return False



readInput(1)
print Domain
Domain.sort(lambda x,y: cmp(len(x),len(y)))
print Domain
start_time = time.time()
print BackTrace(0,0)
printSolution()
print("Time: %s seconds" % (time.time() - start_time))
