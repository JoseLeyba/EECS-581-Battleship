import random

from board import Board
from ship import Ship

class Enemy:
    def __init__(self,numofships):
        self.numofships = numofships            #number of ships
        self.AIboard = Board()

    def easy(self):
        while True:
            letter = random.choice('ABCDEFGHIJ')
            number = random.randint(1,10)
            coordinates = f"{letter}{number}"
            isValid = self.shoot(coordinates)
            if isValid == True:
                break
    
    def medium(self):
        pass

    # hard difficulty
    def hard(self):
        pass

    def shoot(self,coordinates):
        return self.AIboard.fireShotAI(coordinates)

    def placeShips(self):
        pass
