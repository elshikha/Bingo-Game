# check if there is a record with player's name
def checkPrevious(name):
    try:
        f = open(f"records/{name}.txt", "r")
        f.close()
        return True
    except:
        return False
