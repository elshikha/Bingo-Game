
import sys
from play import play
from start import start
import time

while True:

    start()
    if (play() == 0):
        print("Thank You For Playing With Me :)  ")
        time.sleep(2)
        break
