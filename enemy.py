import random
from board import Board
from battleship import Battleship

class Enemy:
    def __init__(self,numofships):
        self.numofships = numofships
        self.AIboard = Board()
        self.ammo = 1

    def easy(self):
        while True:
            letter = random.choice('ABCDEFGHIJ')
            number = random.randint(1,10)
            coordinates = f"{letter}{number}"
            isValid = self.shoot(coordinates)
            if isValid == True:
                break
        if isSpecialShot == 5:
            if self.ammo > 0:
                letters = ['A','B','C','D','E','F','G','H','I','J']
                for i in letters:
                    if letters[i] == letter:
                        letterIndex = i
                downNumber = number + 1
                upNumber = number - 1

                rightLetter = letters[letterIndex + 1]
                leftLetter = letters[letterIndex - 1]

                coordinatesDown = f"{letter}{downNumber}"
                coordinatesUp = f"{letter}{upNumber}"
                coordinatesLeft = f"{leftLetter}{number}"
                coordinatesRight = f"{rightLetter}{number}"
                self.shoot(coordinatesDown)
                self.shoot(coordinatesUp)
                self.shoot(coordinatesLeft)
                self.shoot(coordinatesRight)t
    def medium(self):
        pass

    def hard(self):
        pBoard = Battleship.p1_board.ship_board        # gets the players board
        x = 0
        y = 0
        i = 0
        alphabet = "ABCDEFGHIJ"
        letters = []
        numbers = []
        
        for row in pBoard:
            for item in row:
                x += 1
                if item != 0:
                    letters.append(alphabet[y])
                    numbers.append(str(x))
            y += 1
            x = 0
        
        while True:
            coordinates = f"{letters[i]}{numbers[i]}"
            isValid = self.shoot(coordinates)
            i += 1
            if isValid == True:
                break
    
    def shoot(self,coordinates):
        return self.AIboard.fireShotAI(coordinates)
    def placeShips(self):
        pass
    def gameOver(self):
        return self.AIboard.gameOver()
