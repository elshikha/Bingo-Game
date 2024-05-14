import utils.state as st


def saveGame():
    compMatrix = st.getCompMatrix()
    playerName = st.getPlayerName()
    playerMatrix = st.getPlayerMatrix()
    matrixSize = st.getMatrixSize()
    playerScore = st.getPlayerScore()
    compScore = st.getCompScore()

    # open file({playerName}.txt) write mode
    # write size
    dataToSave = []
    dataToSave.append(str(matrixSize)+'\n')
    playerMat = ''
    compMat = ''

    # write player matrix
    for row in playerMatrix:
        for element in row:
            playerMat += str(element)+' '

    dataToSave.append(playerMat.strip(" ")+'\n')

    # write computer matrix
    for row in compMatrix:
        for element in row:
            compMat += str(element)+' '

    dataToSave.append(compMat.strip(" ")+'\n')

    # write player score
    dataToSave.append(playerScore+'\n')
    # write computer score
    dataToSave.append(compScore+'\n')

    # save the data in the file
    playerFile = open(f"./records/{playerName}.txt", 'w')
    playerFile.writelines(dataToSave)
    playerFile.close()
