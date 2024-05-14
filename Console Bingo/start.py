from play import generateBoard
import state as st
import os


def readFile():
    gameData = []
    fileToRead = open(os.path.abspath(f"./games/{playerName}.txt"), 'r')
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


def newOrcontinue():
    # True for continue and False for New

    idea = input('Do you want to start a new game or just continue ?\n\
            n for New and  :  c for continue  ')
    while idea.lower() != 'c' and idea.lower() != 'n':

        print('Come on Just Read Carefully')
        idea = input('Do you want to start a new game or just continue ?\n\
            n for New and  :  c for continue   ')

        if idea.lower() == 'c' or 'n':
            break

    if idea.lower() == 'c':
        return True

    elif idea.lower() == 'n':
        return False


# main code for checking if the file is exist

def start():
    global playerName

    playerName = input('Enter you Name ')
    st.setPlayerName(playerName)

    try:
        # ask new continue

        playerFile = open(os.path.abspath(f"./games/{playerName}.txt"), 'r')
        playerFile.close()

        # if user chose to start a continue game all data will be saved
        if newOrcontinue():

            playerFile = open(os.path.abspath(
                f"./games/{playerName}.txt"), 'a+')
            Data = readFile()

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

        # if user chose to start a new game all data will be removed
        else:
            playerFile = open(os.path.abspath(
                f"./games/{playerName}.txt"), 'w+')

            # as the user want to a new game size will change again
            size = int(input('Do you want the size of the matrix :\
                (Enter the number next to the choice)\n\
                            1.Default\t2.Another size '))
            if size == 1:
                st.setMatrixSize(5)
            elif size == 2:
                st.setMatrixSize(int(input('Enter the size you want: ')))
            else:
                print('unkown input the size will be default ')
                st.setMatrixSize(5)

            st.updateCompMatrix(generateBoard(st.getMatrixSize()))
            st.updatePlayerMatrix(generateBoard(st.getMatrixSize()))
            st.setPlayerScore("")
            st.setCompScore("")
            playerFile.close()

    except FileNotFoundError:
        # New Game

        playerFile = open(os.path.abspath(f"./games/{playerName}.txt"), 'a+')

        # Take the matrix size from the user

        size = int(input('Do you want the size of the matrix :\
                        (Enter the number next to the choice)\n\
                        1.Default  2.Another size '))
        if size == 1:
            st.setMatrixSize(5)

        elif size == 2:
            st.setMatrixSize(int(input('Enter the size you want: ')))
        else:
            print('unkown input the size will be default ')
            st.setMatrixSize(5)

        st.updateCompMatrix(generateBoard(st.getMatrixSize()))
        st.updatePlayerMatrix(generateBoard(st.getMatrixSize()))
        st.setPlayerScore("")
        st.setCompScore("")
        playerFile.close()
