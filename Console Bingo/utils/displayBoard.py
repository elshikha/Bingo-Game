def displayBoards(compBoard, playerBoard):
    # get the boards

    # loop over items in the matrices and print them
    print(f"computer" + " " * (5 * len(compBoard)+3) + "player")
    for rowIndex in range(len(compBoard)):
        print("|", end="")
        for item in compBoard[rowIndex]:
            print(f"{item:^5}", "", end="")
        print("||", end="")
        for item in playerBoard[rowIndex]:
            print(f"{item:^5}", "", end="")
        print("|")
