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

	def __init__(self, row=0, col=0, word="", sitchType=sitch.accross):
		self.row = row
		self.col = col
		self.word = word
		self.sitchType = sitchType

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
	# print currGrid
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
		return "Don't Assign"
	if (check3x3(currGrid) and checkRows(currGrid) and checkCols(currGrid)):
		return "Assign"
	else:
		return "False"

def printSolution():
	solutionGrid = buildGridFromAssignment()
	for row in range(9):
		for col in range(9):
			print solutionGrid[row][col],
		print ''

def chooseNextVariable(prev_row,prev_col):
	# if prev_row==8 and prev_col==8:
	# 	print "uh oh!"
	# 	return False
	# if prev_col < 8:
	# 	if prev_col % 3 < 2:
	# 		return (prev_row,prev_col+1)
	# 	if prev_col % 3 == 2 and prev_row % 3 < 2:
	# 		return (prev_row+1,prev_col-2)
	# 	if prev_col % 3 ==2 and prev_row % 3 == 2:
	# 		return (prev_row-2,prev_col+2)
	# return (prev_row+1,0)

	if prev_col < 8:
		return (prev_row, prev_col+1)
	return (prev_row+1,0)


def BackTrace(row,col):
	possible = False
	if len(assignments)==18:
		return True
	for word in reversed(Domain):
		valAssignment = Assignment(row,col,word,sitch.accross)
		assignments.append(valAssignment)
		if isConsistent()=="Don't Assign":
			possible=True
		if isConsistent()=="Assign":
			Domain.remove(word)
			varCoord = chooseNextVariable(row,col)
			# if varCoord == False:
			# 	return False
			result = BackTrace(varCoord[0],varCoord[1])
			trow = row
			tcol = col
			while(result=="Possible"):
				varCoord = chooseNextVariable(trow,tcol)
				trow = varCoord[0]
				tcol = varCoord[1]
				result = BackTrace(varCoord[0],varCoord[1])
			if result:
				return True
			if result == False:
				assignments.remove(valAssignment)
				Domain.append(word)
		else:
			assignments.remove(valAssignment)
			valAssignment = Assignment(row,col,word,sitch.down) #try the down version of the word
			assignments.append(valAssignment)
			if isConsistent()=="Don't Assign":
				possible=True
			if isConsistent()=="Assign":
				Domain.remove(word)
				varCoord = chooseNextVariable(row,col)
				# if varCoord == False:
				# 	return False
				result = BackTrace(varCoord[0],varCoord[1])
				trow = row
				tcol = col
				while(result=="Possible"):
					varCoord = chooseNextVariable(trow,tcol)
					trow = varCoord[0]
					tcol = varCoord[1]
					result = BackTrace(varCoord[0],varCoord[1])
				if result:
					return True
				if result == False:
					assignments.remove(valAssignment)
					Domain.append(word)
			else:
				assignments.remove(valAssignment)
	currGrid = buildGridFromAssignment()
	if currGrid[row][col]!='_' and possible:
		return "Possible"
	return False



readInput(1)
print Domain
Domain.sort(lambda x,y: cmp(len(x),len(y)))
print Domain
start_time = time.time()
print BackTrace(0,0)
printSolution()
print("Time: %s seconds" % (time.time() - start_time))
