from enum import Enum
class sitch(Enum):
	accross = 1
	down = 2

class Assignment:
	row = 0 #row of first letter
	col = 0 #col of first letter
	word = ""
	sitchType = sitch.accross

initGrid = [] #(row,col) order
Domain = []
assignment = [] #(string, (upperx, uppery), sitch)



def readInput(inputNum):
	with open('data/bank'+str(inputNum)+'.txt') as input_file:
		for i, line in enumerate(input_file):
			Domain.append(line.rstrip())
	with open('data/grid'+str(inputNum)+'.txt') as input_file:
		for i, line in enumerate(input_file):
			row = []
			line = line.rstrip()
			for character in line: 
				row.append(character)
			initGrid.append(row)


def buildGridFromAssignment():
	currGrid = []
	for a in assignment:
		word = a.word
		if a.sitchType==sitch.accross:
			wordPos = 0
			for i in range(a.col,a.col+len(word)-1):
				if currGrid[a.row][i]!='_' and currGrid[a.row][i]!=word[wordPos]:
					return False
				currGrid[a.row][i]=word[wordPos]
				wordPos+=1
		elif a.sitchType==sitch.down:
			wordPos = 0
			for i in range(a.row,a.row+len(word)-1):
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
					if l != '_' and letters.contains():
						return False
					if l!= '_':
						letters[l]=True
	return True

def checkRows(currGrid):

def checkCols(currGrid):


def isConsistent():
	currGrid = buildGridFromAssignment
	if currGrid == False:
		return False
	return (check3x3(currGrid) and checkRows(currGrid) and checkCols(currGrid))



def chooseNextVariable(prev_row,prev_col):
	if prev_col < 8:
		return (prev_row, prev_col+1)
	return (prev_row+1,0)

def BackTrace():


readInput(1)
Backtrace()
