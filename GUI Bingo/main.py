import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox)

import utils.state as st

from utils.generateBoard import generateBoard
from utils.checkPrevious import checkPrevious
from utils.saveGame import saveGame
from utils.checkwin import checkWin


class PrimaryButton(QPushButton):

    sizes = {"s": 15, "m": 35}

    def __init__(self, text, size="m"):
        super(QPushButton, self).__init__()

        self.size = size
        self.setText(text)
        self.setStyleSheet(f"""
        QPushButton{{
            background:#1d9bf0;
            padding:{PrimaryButton.sizes[self.size] }px {PrimaryButton.sizes[size]*1.5}px;
            max-width:{PrimaryButton.sizes[self.size] * 13}px;
            color:#eee;
            border-radius:{PrimaryButton.sizes[self.size]*1.2}px;
            font-size:{PrimaryButton.sizes[self.size]}px;
            max-height:45px;
        }}
        QPushButton:hover{{
            background:#49aff3;
        }}
        """)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))


class MatItem(QPushButton):
    def __init__(self, num, callbacks=[], isClickable=True, window=None):

        if window != None:
            super(QPushButton, self).__init__(window)
        else:
            super(QPushButton, self).__init__()

        self.isClickable = isClickable
        self.callbacks = callbacks
        if num != "X":
            self.setEnabled(self.isClickable)
            self.clicked.connect(self.onClick)

        self.setText(str(num))
        self.color = "#ECE8DD"
        self.bgColor = "#0d95e8"

        if (num == "X"):
            self.color = "#282828"

        if not (self.isClickable):
            self.bgColor = "red"

        style = f"""
        MatItem{{
            color:{self.color};
            background-color:{self.bgColor};
            border-radius:5px;
            font-size:20px;
            font-weight:700;
            min-height:75px;
            width:75px;
        }}

        """
        if self.isClickable and num != "X":
            self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            style += """:hover{color:#282828}"""

        self.setStyleSheet(style)

    def onClick(self):
        for fun in self.callbacks:
            if (st.getCompScore() != "BINGO" and st.getPlayerScore() != "BINGO"):
                fun(self.text())


class MyWindow(QMainWindow):

    # static property
    currentFrame = None

    def __init__(self):
        super(MyWindow, self).__init__()

        self.setWindowTitle("Bingooo")
        self.setGeometry(100, 100, 1600, 900)

        self.setStyleSheet(
            """MyWindow{background-color:#282828;color:#eee;}""")

        self.mainGrid = QGridLayout()

    def updateWindow(self):
        wid = QWidget()
        wid.setLayout(self.mainGrid)
        self.setCentralWidget(wid)

    # each Frame should update the self.mainGrid layout with it's content
    def switchFrames(self, frame):

        # reset the grid
        self.mainGrid = QGridLayout()
        MyWindow.currentFrame = frame
        frame()

        # add to the window
        wid = QWidget()
        wid.setLayout(self.mainGrid)
        self.setCentralWidget(wid)

    def Frame_welcome(self):

        # welcome label
        welcome = QLabel("Welcome to")
        welcome.setStyleSheet(
            """font-size:70px;color:#bbb;""")
        welcome.setAlignment(QtCore.Qt.AlignCenter)

        # logo
        logo = QLabel("Bingoo")
        logo.setStyleSheet("""font-size:70px;color:#eee;""")
        logo.setAlignment(QtCore.Qt.AlignCenter)

        # wrapper for the logo and the welcome label
        welcomeWrapper = QWidget()
        welcomeWrapperLayout = QVBoxLayout()
        welcomeWrapperLayout.addWidget(welcome)
        welcomeWrapperLayout.addWidget(logo)
        welcomeWrapper.setLayout(welcomeWrapperLayout)
        welcomeWrapper.setStyleSheet("""max-height:250px""")
        self.mainGrid.addWidget(welcomeWrapper, 0, 0)

        # btn
        btn = PrimaryButton("Start")
        btn.clicked.connect(lambda: self.switchFrames(self.Frame_startGame))

        self.mainGrid.addWidget(btn, 1, 0)

    def Frame_getInput(self, labelText, btnText, callBack=None):
        self.mainGrid = QGridLayout()
        text = QLabel(labelText)
        text.setStyleSheet("""
            font-size:24px;
            color:#eee;
            max-height:30px;
            margin:0;
        """)
        text.setAlignment(QtCore.Qt.AlignCenter)

        textField = QtWidgets.QLineEdit()
        textField.setStyleSheet("max-height:30px;margin:0")
        enterBtn = PrimaryButton(btnText)

        myWrapperLayout = QVBoxLayout()
        myWrapper = QLabel()
        myWrapperLayout.addWidget(text)
        myWrapperLayout.addWidget(textField)

        myWrapperLayout.addWidget(enterBtn)
        myWrapper.setAlignment(QtCore.Qt.AlignCenter)
        myWrapper.setStyleSheet("max-width:600px;max-height:600px")
        myWrapper.setLayout(myWrapperLayout)

        def onClick():
            if callBack != None:
                callBack(textField.text())

        enterBtn.clicked.connect(onClick)

        self.mainGrid.addWidget(myWrapper, 1, 1, 3, 1)
        self.updateWindow()

    def Frame_askYesNo(self, labelText, btn1, callback1, btn2, callback2):
        label = QLabel(labelText)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("""
                    color:#eee;
                    font-size:20px;
                """)

        btn1 = PrimaryButton(btn1, "s")
        btn2 = PrimaryButton(btn2, "s")

        btn1.clicked.connect(callback1)
        btn2.clicked.connect(callback2)

        btnsWrapperLayout = QHBoxLayout()
        btnsWrapperLayout.addWidget(btn1)
        btnsWrapperLayout.addWidget(btn2)
        btnsWrapper = QLabel()
        btnsWrapper.setLayout(btnsWrapperLayout)

        newOrConinueLayout = QVBoxLayout()
        newOrConinueLayout.addWidget(label)
        newOrConinueLayout.addWidget(btnsWrapper)

        newOrConinueWrapper = QWidget()
        self.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding))
        newOrConinueWrapper.setLayout(newOrConinueLayout)

        self.mainGrid = QGridLayout()
        self.mainGrid.addWidget(newOrConinueWrapper, 0, 0)
        self.updateWindow()

    def Frame_startGame(self):

        self.setGeometry(100, 100, 600, 600)

        # Check previous & new/continue

        def askForSize():
            def _ (s):
                isValidSize = True
                try:
                    x = int(s)
                    if x < 5:
                        isValidSize = False
                except:
                    isValidSize = False

                if not isValidSize:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Invalid size")
                    msg.setText("Invalid size, size is set to default 5")
                    msg.exec_()
                    s = 5

                st.setMatrixSize(int(s))
                st.updateCompMatrix(generateBoard(st.getMatrixSize()))
                st.updatePlayerMatrix(generateBoard(st.getMatrixSize()))
                st.setPlayerScore("")
                st.setCompScore("")
                self.switchFrames(self.Frame_game)

            self.Frame_getInput(
                "What board size do you want?", "Let's gooo",
                _
            )

        def enterBtnOnClick(name):
            st.setPlayerName(name)

            # check if there is a record with the user's name

            isNew = checkPrevious(name)

            def newGame():
                # REMOVE ALL DATA IN THE FILE IF IT EXIST OR CREATE A NEW ONE
                playerFile = open(f"./records/{name}.txt", 'w')
                playerFile.close()

                def defaultSize():

                    st.setMatrixSize(5)

                    st.updateCompMatrix(generateBoard(st.getMatrixSize()))
                    st.updatePlayerMatrix(generateBoard(st.getMatrixSize()))
                    st.setPlayerScore("")
                    st.setCompScore("")
                    # SWITCH TO THE NEXT FRAME
                    self.switchFrames(self.Frame_game)

                # ASK IF WANT TO SPECIFY A SIZE OR STICK WITH THE DEFAULT ONE
                self.Frame_askYesNo(
                    "Do you want the default size or another one? ", "Default", defaultSize, "Another", askForSize)

            # ################################
            # There is a record with this name
            if isNew:

                # read the record of the previous game and
                # extract the data from the recode
                # update the state with the extracted data
                def continueGame():

                    def readRecord():
                        gameData = []
                        fileToRead = open(f"./records/{name}.txt", 'r')
                        # open file with the user name
                        for i in range(5):

                            # save data in a list
                            # in the list:the first element is the matrix size
                            #             the second element is the user matrix
                            #             the 3th element is the computer matix
                            #             the 4th element is the user data
                            #             the 5th element is the computer data

                            gameData.append(fileToRead.readline().strip('\n'))
                        return gameData

                    playerFile = open(f"./records/{name}.txt", 'a+')
                    Data = readRecord()

                    playerMatrix = [Data[1].split(' ')[i:i+int(Data[0])]
                                    for i in range(0, len(Data[1].split(' ')), int(Data[0]))]

                    for i in range(int(Data[0])):
                        for j in range(int(Data[0])):
                            e = playerMatrix[i][j]
                            if e != "X":
                                playerMatrix[i][j] = int(e)

                    computerMatrix = [Data[2].split(
                        ' ')[i:i+int(Data[0])] for i in range(0, len(Data[2].split(' ')), int(Data[0]))]

                    for i in range(int(Data[0])):
                        for j in range(int(Data[0])):
                            e = computerMatrix[i][j]
                            if e != "X":
                                computerMatrix[i][j] = int(e)

                    st.updateCompMatrix(computerMatrix)
                    st.updatePlayerMatrix(playerMatrix)
                    st.setPlayerScore(Data[3])
                    st.setCompScore(Data[4])
                    st.setMatrixSize(int(Data[0]))
                    playerFile.close()

                    self.switchFrames(self.Frame_game)

                #  IF THERE IS AN EXISTING RECORD WITH THIS NAME, ASK IF NEW OR CONTINUE
                self.Frame_askYesNo("Do you want to start a new game or continue? ",
                                    "New", newGame,
                                    "Continue", continueGame)

                # This is the first time he plays
            else:
                newGame()

        # ASK THE USER FOR HIS NAME
        self.Frame_getInput("Please Enter Your Name:", "Play", enterBtnOnClick)

    def Frame_game(self):

        compScore = QLabel(f"Computer: {st.getCompScore()}")
        playerScore = QLabel(f"Player: {st.getPlayerScore()}")
        lastChosenLabel = QLabel(f"")
        if (st.getLastChosenNumber() != None):
            lastChosenLabel.setText(
                f"{st.getTurn()} choosed {st.getLastChosenNumber()}")

        lastChosenLabel.setStyleSheet("color:#eee;font-size:20px;")
        compScore.setStyleSheet("font-size:20px;color:#eee")
        playerScore.setStyleSheet("font-size:20px;color:#eee")

        self.mainGrid.addWidget(compScore, 0, 0, 1, 1)
        self.mainGrid.addWidget(playerScore, 0, 6, 1, 1)
        self.mainGrid.addWidget(lastChosenLabel, 1, 0, 1, 6)
        self.mainGrid.setHorizontalSpacing(50)

        compBoardLayout = QGridLayout()
        playerBoardLayout = QGridLayout()

        # Get data from state
        compMat = st.getCompMatrix()
        playerMat = st.getPlayerMatrix()
        size = st.getMatrixSize()

        saveGame()

        def msgBox(text):
            msg = QMessageBox()
            msg.setText(text)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            def onclick(i):
                if i.text() == "OK":
                    self.switchFrames(self.Frame_startGame)
                else:
                    quit()

            msg.buttonClicked.connect(onclick)
            msg.exec_()

        def computerTurn(*args):
            import time
            time.sleep(.2)

            # choose a number based on which row/col/diagonal is the closest to be completed
            compRowsProgress = []
            compColsProgress = []

            if (st.getCompScore() == "BINGO" or st.getPlayerScore == "BINGO"):
                return

            compBoard = st.getCompMatrix()
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

            crossNum(n)

        def crossNum(n):

            for row in range(size):
                for col in range(size):
                    if compMat[row][col] == int(n):
                        st.setlNumPosInCBoard({"row": row, "col": col})
                        compMat[row][col] = "X"
                    if playerMat[row][col] == int(n):
                        st.setlNumPosInPBoard({"row": row, "col": col})
                        playerMat[row][col] = "X"

            checkCompletion()

            st.setLastChosenNumber(n)
            st.nextTurn()
            st.updateCompMatrix(compMat)
            st.updatePlayerMatrix(playerMat)

            self.switchFrames(self.Frame_game)
            self.updateWindow()

        def checkCompletion():
            # ##################################################
            # check if crossing this num completed       #######
            # a row / col / diagonal in computer's board #######
            # ##################################################

            # numPosInCBoard is the position of the recently removed number in computer's matrix
            # numPosInPBoard is the position of the recently removed number in player's matrix

            numPosInCBoard = st.getlNumPosInCBoard()
            numPosInPBoard = st.getlNumPosInPBoard()

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
        # ##################################################
        # Display the boards on the grids ##################
        # ##################################################

        for i in range(size):
            for j in range(size):
                compBoardLayout.addWidget(
                    MatItem(f"{compMat[i][j]}", [crossNum, computerTurn], False), i, j)
                playerBoardLayout.addWidget(
                    MatItem(f"{playerMat[i][j]}", [crossNum, computerTurn]), i, j)

        compBoard = QWidget()
        compBoard.setLayout(compBoardLayout)
        playerBoard = QWidget()
        playerBoard.setLayout(playerBoardLayout)

        self.mainGrid.addWidget(compBoard, 2, 0, 10, 5)
        self.mainGrid.addWidget(playerBoard, 2, 6, 10, 5)

        self.updateWindow()

        if checkWin() != None:
            if checkWin() == 0:
                msgBox("draw, lets settle this up with another game ;)")
            elif checkWin() == 1:
                msgBox("lost, wanna lose again? ;)")
            elif checkWin() == 2:
                msgBox("won, wanna play again? ;)")
            return


app = QApplication(sys.argv)


def quit():
    app.quit()


win = MyWindow()
win.show()
win.switchFrames(win.Frame_welcome)
win.setWindowIcon(QIcon("icon.jpg"))

sys.exit(app.exec_())
