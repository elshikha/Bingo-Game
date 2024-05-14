# This module holds and manages the program's state

playerName = ""
playerMatrix = []
compMatrix = []
playerScore = ""
compScore = ""
matrixSize = 5
lastChosenNum = None
lNumPosInCBoard = {}
lNumPosInPBoard = {}
turn = "computer"


def setPlayerName(name):
    global playerName
    playerName = name


def getPlayerName():
    return playerName

# return player's board matrix


def getPlayerMatrix():
    return playerMatrix

# return computer's board matrix


def getCompMatrix():
    return compMatrix

# takes a matrix as an arg. and
# set the player matrix variable to this new value


def updatePlayerMatrix(matrix):
    global playerMatrix
    playerMatrix = matrix

# takes a matrix as an arg. and
# set the computer matrix variable to this new value


def updateCompMatrix(matrix):
    global compMatrix
    compMatrix = matrix

# set the board size to a new value


def setMatrixSize(newSize):
    global matrixSize
    matrixSize = newSize


def getMatrixSize(): return matrixSize


def getPlayerScore():
    return playerScore


def setPlayerScore(score):
    global playerScore
    playerScore = score


def getCompScore():
    return compScore


def setCompScore(score):
    global compScore
    compScore = score


def increasePlayerScore():
    global playerScore
    if playerScore == "":
        playerScore += "B"
    elif playerScore == "B":
        playerScore += "I"
    elif playerScore == "BI":
        playerScore += "N"
    elif playerScore == "BIN":
        playerScore += "G"
    elif playerScore == "BING":
        playerScore += "O"


def increaseCompScore():
    global compScore
    if compScore == "":
        compScore += "B"
    elif compScore == "B":
        compScore += "I"
    elif compScore == "BI":
        compScore += "N"
    elif compScore == "BIN":
        compScore += "G"
    elif compScore == "BING":
        compScore += "O"


def setlNumPosInCBoard(n):
    global lNumPosInCBoard
    lNumPosInCBoard = n


def setlNumPosInPBoard(n):
    global lNumPosInPBoard
    lNumPosInPBoard = n


def getLastChosenNumber():
    return lastChosenNum


def setLastChosenNumber(n):
    global lastChosenNum
    lastChosenNum = n


def getlNumPosInCBoard():
    return lNumPosInCBoard


def getlNumPosInPBoard():
    return lNumPosInPBoard


def getTurn():
    return turn


def nextTurn():
    global turn
    if (turn == "computer"):
        turn = playerName
    else:
        turn = "computer"
