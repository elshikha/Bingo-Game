from saveGame import saveGame
import state as st
import time
from utils.displayBoard import displayBoards
import random

# takes a number
# and return a square matrix of this size
# all elements are random


def generateBoard(boardSize):
    boardSizeSquared = int(boardSize)**2
    matrix = []
    generated_numbers = set()
    for i in range(int(boardSize)):
        row = []
        for j in range(int(boardSize)):
            while True:
                number = random.randint(1, boardSizeSquared)
                if number not in generated_numbers:
                    generated_numbers.add(number)
                    break
            row.append(number)
        matrix.append(row)
    return matrix


def play():
    numberOfPlays = 1
    while True:
        compBoard = st.getCompMatrix()
        playerBoard = st.getPlayerMatrix()
        size = st.getMatrixSize()

        # ##################################################
        # print the boards and the scores to the console ###
        # ##################################################
        displayBoards(compBoard, playerBoard)
        saveGame()

        def printScores():
            print("computer score:", st.getCompScore())
            print("player score:", st.getPlayerScore())
            print("="*30)
        printScores()

        # ##################################################
        # check if the computer or the player won ##########
        # ##################################################

        if st.getCompScore() == st.getPlayerScore() == "BINGO":
            print("Draw")
            wish = input("Start a new game? (y/n)")
            if (wish == "n"):
                return 0
            else:
                return 1

        elif st.getCompScore() == "BINGO":
            print("HAHAHA LOST YA 7abeby")
            wish = input("Start a new game? (y/n)")
            if (wish == "n"):
                return 0
            elif wish == "y":
                return 1
            else:
                print("unexpected input, the game will terminate")
                return 0

        elif st.getPlayerScore() == "BINGO":
            print("3ash ya wala!")
            wish = input("Start a new game? (y/n)")
            if (wish == "n"):
                return 0
            else:
                return 1

        # ##################################################
        # Player's turn ####################################
        # ##################################################

        if (numberOfPlays % 2 == 0):
            # take input from the user and validate it

            # Keeps asking the user for a number until he enters a valid one
            # returns the number unless the user wants to exit
            # in that case returns false
            def getValidInput():
                max = size ** 2

                while True:
                    element = input("Choose a number: ")

                    # check if not number
                    try:
                        element = int(element)
                    except:
                        print(f'Invalid input ')
                        continue

                    if int(element) == -1:
                        wish = input("are you sure you want to exit: (y/n) ")
                        if wish == "y":
                            return False
                        elif wish == "n":
                            continue

                    if (int(element) not in range(1, max+1)):
                        print(
                            f'the number must be in less than {max} and greater than 0')
                        continue

                    remaining = []
                    for row in compBoard:
                        for e in row:
                            if e != "X":
                                remaining.append(e)

                    if int(element) not in remaining:
                        print("Number was chosen before ")
                        continue

                    return int(element)

            n = getValidInput()

            # if getValidInput returned false then the user want to exit
            if (n == False):
                return 0

        # ##################################################
        # computer's turn ##################################
        # ##################################################
        else:
            print("wait the computer is choseing a number...")
            time.sleep(1.4)

            # choose a number based on which row/col/diagonal is the closest to be completed
            compRowsProgress = []
            compColsProgress = []
            for i in range(len(compBoard)):
                row = compBoard[i]
                compRowsProgress.append(0)
                for item in row:
                    if item == "X":
                        compRowsProgress[i] += 1
                if compRowsProgress[i] == size:
                    compRowsProgress[i] = 0
            for col in range(len(compBoard)):
                compColsProgress.append(0)
                for row in range(len(compBoard)):
                    item = compBoard[row][col]
                    if item == "X":
                        compColsProgress[col] += 1
                if compColsProgress[col] == size:
                    compColsProgress[col] = 0

            # main diagonal progress
            mainDiagonalProgress = 0
            if size % 2 != 0:
                for i in range(size):
                    if compBoard[i][i] == "X":
                        mainDiagonalProgress += 1
                if mainDiagonalProgress == size:
                    mainDiagonalProgress = 0
            # secondary diagonal progress
            secondaryDiagonalProgress = 0
            if size % 2 != 0:
                for i in range(size):
                    if compBoard[size-1-i][i] == "X":
                        secondaryDiagonalProgress += 1
                if secondaryDiagonalProgress == size:
                    secondaryDiagonalProgress = 0

            maxRow = max(compRowsProgress)
            rowIndex = compRowsProgress.index(maxRow)
            maxCol = max(compColsProgress)
            colIndex = compColsProgress.index(maxCol)
            maxDiagonal = max(mainDiagonalProgress, secondaryDiagonalProgress)
            maxRowCol = max(maxCol, maxRow)

            if (maxRowCol > maxDiagonal):
                if maxRow >= maxCol:
                    for element in compBoard[rowIndex]:
                        if element != "X":
                            n = element
                            break
                else:
                    for j in range(size):
                        element = compBoard[j][colIndex]
                        if element != "X":
                            n = element
                            break
            else:
                if (mainDiagonalProgress >= secondaryDiagonalProgress):
                    for i in range(size):
                        if compBoard[i][i] != "X":
                            n = compBoard[i][i]
                            break
                else:
                    for i in range(size):
                        if compBoard[size-1-i][i] != "X":
                            n = compBoard[size-1-i][i]
                            break

            print(f"Computer chose: {n}")

        # ##################################################
        # cross the number from the matrices and update them
        # ##################################################

        numPosInCBoard = {}
        numPosInPBoard = {}

        for row in range(size):
            for col in range(size):
                if compBoard[row][col] == n:
                    numPosInCBoard = {"row": row, "col": col}
                    compBoard[row][col] = "X"
                if playerBoard[row][col] == n:
                    numPosInPBoard = {"row": row, "col": col}
                    playerBoard[row][col] = "X"

        st.updateCompMatrix(compBoard)
        st.updatePlayerMatrix(playerBoard)

        # ##################################################
        # check if crossing this num completed       #######
        # a row / col / diagonal in computer's board #######
        # ##################################################

        # numPosInCBoard is the position of the recently removed number in computer's matrix
        # numPosInPBoard is the position of the recently removed number in player's matrix

        # checking the row
        for i in range(size):
            if st.getCompMatrix()[numPosInCBoard["row"]][i] != "X":
                break
        else:
            st.increaseCompScore()

        # checking the col
        for j in range(size):
            if st.getCompMatrix()[j][numPosInCBoard["col"]] != "X":
                break
        else:
            st.increaseCompScore()

        # checking the diagonals (only if the board size is odd)
        if size % 2 != 0:
            # checking if the number removed used to exist in the main diagonal
            if (numPosInCBoard["row"] == numPosInCBoard["col"]):
                for k in range(size):
                    if st.getCompMatrix()[k][k] != "X":
                        break
                else:
                    st.increaseCompScore()
            # checking if the number removed used to exist in the secondary diagonal
            if (numPosInCBoard["row"] + numPosInCBoard["col"] == size-1):
                for k in range(size):
                    if st.getCompMatrix()[k][size-1-k] != "X":
                        break
                else:
                    st.increaseCompScore()

        # ##################################################
        # check if crossing this num completed       #######
        # a row / col / diagonal in player's board #######
        # ##################################################

                # checking the row
        for i in range(size):
            if st.getPlayerMatrix()[numPosInPBoard["row"]][i] != "X":
                break
        else:
            st.increasePlayerScore()

        # checking the row
        for j in range(size):
            if st.getPlayerMatrix()[j][numPosInPBoard["col"]] != "X":
                break
        else:
            st.increasePlayerScore()
        # checking the diagonals (only if size is odd)
        if size % 2 != 0:
            # checking if the number removed used to exist in the main diagonal
            if (numPosInPBoard["row"] == numPosInPBoard["col"]):
                for k in range(size):
                    if st.getPlayerMatrix()[k][k] != "X":
                        break
                else:
                    st.increasePlayerScore()
            # checking if the number removed used to exist in the secondary diagonal
            if (numPosInPBoard["row"] + numPosInPBoard["col"] == size-1):
                for k in range(size):
                    if st.getPlayerMatrix()[k][size-1-k] != "X":
                        break
                else:
                    st.increasePlayerScore()

        numberOfPlays += 1
