import utils.state as st
# ##################################################
# check if the computer or the player won ##########
# ##################################################


def checkWin():
    if st.getCompScore() == st.getPlayerScore() and st.getPlayerScore() == "BINGO":

        return 0

    elif st.getCompScore() == "BINGO":
        return 1

    elif st.getPlayerScore() == "BINGO":
        return 2
