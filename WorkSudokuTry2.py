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


	def __init__(self, row=0, col=0, word="", sitchType=sitch.across,shiftBack=0):
		self.row = row
		self.col = col
		self.word = word
		self.sitchType = sitchType
		self.shiftBack = shiftBack

initGrid = [] #(row,col) order
Words = [] #(word,sitch)
assignments = [] #Array<Assignment>


values = [] #[x][y]: value
lettersAvailable = []

def readInput(inputNum):
	with open('data/bank'+str(inputNum)+'.txt') as input_file:
		for i, line in enumerate(input_file):
			Words.append(line.rstrip().upper())
	with open('data/grid'+str(inputNum)+'.txt') as input_file:
		for i, line in enumerate(input_file):
			row = []
			line = line.rstrip()
			for character in line: 
				row.append(character)
			initGrid.append(row)

def initValues():
	global values
	for i in range(9):
		valrow = []
		for j in range(9):
			valrow.append(0)
		values.append(valrow)

def updateValuesFromGrid():
	global values
	currGrid=buildGridFromAssignment()
	# print currGrid
	initValues()
	rowvals=[]
	colvals=[]
	squarevals=[]
	rowcounts=[]
	colcounts=[]
	squarecounts=[]

	#update row values
	for i in range(9):
		rowcount = 0
		letters = {}
		for j in range(9):
			l = currGrid[i][j]
			if l !='_':
				if l not in letters:
					rowcount+=1
				letters[l]=True
		rowvals.append(letters.keys())
		rowcounts.append(rowcount)
	#update col values
	for c in range(9):
		colcount = 0
		letters = {}
		for r in range(9):
			l = currGrid[r][c]
			if l!='_':
				if l not in letters:
					colcount+=1
				letters[l]=True
		colvals.append(letters.keys())
		colcounts.append(colcount)

	#update square values
	for row in range(0,9,3):
		for col in range(0,9,3):
			squarecount = 0
			letters={}
			for r in range(row,row+3):
				for c in range(col,col+3):
					l = currGrid[r][c]
					if l!='_':
						if l not in letters:
							squarecount+=1
						letters[l]=True
			squarevals.append(letters.keys())
			squarecounts.append(squarecount)

	#TODO: now update values for each coordinate using rowvals, colvals and squarevals
	result = True
	for r in range(9):
		for c in range(9):
			# values[r][c] = len(set(squarevals[3*int(r/3)+int(c/3)] + rowvals[r] + colvals[c]))
			values[r][c] = squarecounts[3*int(r/3)+int(c/3)] + rowcounts[r] + colcounts[c]
			if currGrid[r][c]=='_':
				# print "numletters available: ",lettersAvailable
				# print "r: ",r,"c: ",c,set(squarevals[3*int(r/3)+int(c/3)] + rowvals[r] + colvals[c])
				if len(list(set(lettersAvailable) - set(squarevals[3*int(r/3)+int(c/3)] + rowvals[r] + colvals[c]))) < 1:
					# print "aaaaaaaah"
					result = False
	# print values
	return result

def buildGridFromAssignment():
	currGrid = copy.deepcopy(initGrid)
	for a in assignments:
		word = a.word
		if a.sitchType==sitch.across:
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
	updateValuesFromGrid()
	maxVal = 0
	maxCoordR = -1
	maxCoordC = -1
	# #TODO: find the blank coordinate with the maximum value from values and return that coordinate because this means it is the least constraining

	currGrid = buildGridFromAssignment()
	for i in range(9):
		for j in range(9):
			if currGrid[i][j]=='_' and values[i][j] > maxVal:
				maxVal = values[i][j]
				maxCoordR=i
				maxCoordC=j
	if maxCoordC==-1:
		return True
	return (maxCoordR,maxCoordC)

def fillnumAvailableLetters():
	global lettersAvailable
	lettersAvailable=[]
	letters = {}
	assignWords = [] #list of all currently used words
	for a in assignments:
		assignWords.append(a.word)
	availableWords = list(set(Words)-set(assignWords))
	for word in availableWords:
		for l in word:
			if l not in letters:
				lettersAvailable.append(l)
			letters[l]=True
	print "numwords: ",len(availableWords)
	print "numletters free: ",len(lettersAvailable)

def forwardCheck():
	fillnumAvailableLetters()
	return updateValuesFromGrid()

def canPlace(word):
	for row in range(9):
		for col in range(0,10-len(word),1):
			tempAssign = Assignment(row,col,word,sitch.across)
			assignments.append(tempAssign)
			if isConsistent():
				assignments.remove(tempAssign)
				return True
			assignments.remove(tempAssign)
	for col in range(9):
		for row in range(0,10-len(word),1):
			tempAssign = Assignment(row,col,word,sitch.down)
			assignments.append(tempAssign)
			if isConsistent():
				assignments.remove(tempAssign)
				return True
			assignments.remove(tempAssign)
	print "False"
	print "Falseroo"
	return False

def BackTrace(row,col):
	global Words
	print len(assignments)
	currGrid = buildGridFromAssignment()
	if len(assignments)>18:
		return True
	wordsCopy = copy.deepcopy(Words)
	wordsCopy.sort(lambda x,y: cmp(len(x),len(y)))
	for word in reversed(wordsCopy):
		if canPlace(word) == False:
			return False
		print "can place ",word
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
					valAssignment = Assignment(row,tempCol,word,sitch.across)
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
				Words.remove(word)
				varCoord = chooseNextVariable(row,col)
				if varCoord == True:
					return True
				result = BackTrace(varCoord[0],varCoord[1])
				if result:
					return True
				if result == False:
					assignments.remove(assignment)
					Words.append(word)
					Words.sort(lambda x,y: cmp(len(x),len(y)))
			else:
				assignments.remove(assignment)
	return False



readInput(2)
print Words
Words.sort(lambda x,y: cmp(len(x),len(y)))
print Words
start_time = time.time()
print BackTrace(0,0)
printSolution()
print("Time: %s seconds" % (time.time() - start_time))
