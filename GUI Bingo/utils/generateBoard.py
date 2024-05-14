import random


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
