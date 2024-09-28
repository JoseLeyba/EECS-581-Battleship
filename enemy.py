import random
from board import Board
from ship import Ship

class Enemy:
    def __init__(self,numofships):
        self.numofships = numofships
        self.AIboard = Board()
        self.ammo = 1
        #These are all needed for medium, possible moves is a list of all available moves, hits are places where it has hit before, and potential targets will store the adjacent cells after a hit as a queue
        self.possible_moves = [f"{row}{col}" for row in "ABCDEFGHIJ" for col in range(1, 11)]
        self.hits = [] 
        self.potential_targets = [] 
        
    def easy(self):
        isSpecialShot = random.randint(1,10)
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
                rightLetter = None
                leftLetter = None
                if letterIndex + 1 < len(letters):
                    rightLetter = letters[letterIndex + 1]
                if letterIndex - 1 >= 0:
                    leftLetter = letters[letterIndex - 1]
                coordinatesLeft = f"{leftLetter}{number}" if leftLetter else None
                coordinatesRight = f"{rightLetter}{number}" if rightLetter else None

                coordinatesDown = f"{letter}{downNumber}"
                coordinatesUp = f"{letter}{upNumber}"
    
                self.shoot(coordinatesDown)
                self.shoot(coordinatesUp)
                if coordinatesLeft:
                    self.shoot(coordinatesLeft)
                if coordinatesRight:
                    self.shoot(coordinatesRight)
    def medium(self):
        if self.potential_targets:
            move = self.potential_targets.pop(0)
        else:
            move = random.choice(self.possible_moves)
            self.possible_moves.remove(move)
        isValid = self.shoot(move)
        if isValid:
            self.processHit(move)  

    def processHit(self, coordinate):
        row, col = coordinate[0], int(coordinate[1:])
        adjacent = [
            f"{chr(ord(row) - 1)}{col}" if row > 'A' else None, 
            f"{chr(ord(row) + 1)}{col}" if row < 'J' else None,  
            f"{row}{col - 1}" if col > 1 else None,              
            f"{row}{col + 1}" if col < 10 else None             
        ]

        valid_adjacent = [coord for coord in adjacent if coord and coord in self.possible_moves]
        self.potential_targets.extend(valid_adjacent)
        self.possible_moves = [move for move in self.possible_moves if move not in valid_adjacent] 
        
    def hard(self):
        from battleship import Battleship
        pBoard = Battleship.p1_board.ship_board        # gets the players board
        x = 0
        y = 0
        i = 0
        alphabet = "ABCDEFGHIJ"
        letters = []
        numbers = []

        # for loop that reads the board for all ships
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
        shipLength = self.numofships
        directions = ["up", "down","left","right"]
        letters = ['A','B','C','D','E','F','G','H','I','J']
        
        while shipLength != 0:
            placed = False
            ship = Ship(shipLength)
            while not placed:
                direction = random.choice(directions)
                startCol = random.choice(letters)
                startRow = random.randint(1,10)
                length = shipLength - 1

                if direction == "up":
                    endCol = startCol
                    endRow = startRow - length
                    if endRow < 1:
                        continue

                elif direction == "down":
                    endCol = startCol
                    endRow = startRow + length
                    if endRow > 10:
                        continue

                elif direction == "right":
                    letterIndex = letters.index(startCol)
                    if letterIndex + length >= len(letters):
                        continue
                    endCol = letters[letterIndex + length]
                    endRow = startRow

                elif direction == "left":
                    letterIndex = letters.index(startCol)
                    if letterIndex - length < 0:
                        continue
                    endCol = letters[letterIndex - length]
                    endRow = startRow
                    
                start = f"{startCol}{startRow}"
                end = f"{endCol}{endRow}"
                isValid = self.AIboard.placeShip(ship, start, end)
                if isValid:
                    self.AIboard.ships.append(ship)
                    placed = True
            shipLength -= 1
        print(self.AIboard.ships)
        print(self.AIboard.ship_board)
        print(self.AIboard.shot_board)
        pass
    def gameOver(self):
        return self.AIboard.gameOver()
