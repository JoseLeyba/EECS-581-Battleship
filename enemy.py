import random
from board import Board
from ship import Ship

class Enemy:
    def __init__(self,numofships, player_board):
        self.numofships = numofships
        self.AIboard = Board()
        self.ammo = 1
        self.player_board = player_board
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
                letterIndex = letters.index(letter)
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
        while True:
            if self.potential_targets:
                move = self.potential_targets.pop(0)
            else:
                move = random.choice(self.possible_moves)
                self.possible_moves.remove(move)
            result = self.shoot(move)
            if result is None:
                continue  # Invalid shot, try again
            if move in self.possible_moves:
                self.possible_moves.remove(move)
            if result:
                # Hit
                self.processHit(move)
            break  # End turn after a valid shot

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
        coordinates_list = []
        for ship in self.player_board.ships:
            coordinates_list.extend(ship.coordinates)
        
        for coord in coordinates_list:
            isValid = self.shoot(coord)
            if isValid:
                break  # Stop after a successful hit
        
        def shoot(self, coordinates):
            result = self.player_board.fireShotAI(coordinates)
            if result is None:
                return None
            else:
                return result
        
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
