import random
from board import Board

class Enemy:
    def __init__(self,numofships):
        self.numofships = numofships
        self.AIboard = Board()
        self.theSpecial = 1

    def easy(self):
        special = random.randint(1,10)
        if special != 5:
            while True:
                letter = random.choice('ABCDEFGHIJ')
                number = random.randint(1,10)
                coordinates = f"{letter}{number}"
                isValid = self.shoot(coordinates)
                if isValid == True:
                    break
        else:
            if self.theSpecial > 0:
                while True:
                    letter = random.choice('ABCDEFGHIJ')
                    number = random.randint(1,10)
                    coordinates = f"{letter}{number}"
                    isValid = self.shoot(coordinates)
                    if isValid == True:
                        break
            #finish the special shot
    def medium(self):
        pass

    def hard(self):
        pass

    def shoot(self,coordinates):
        return self.AIboard.fireShotAI(coordinates)
    def placeShips(self):
        pass
    def gameOver(self):
        pass
