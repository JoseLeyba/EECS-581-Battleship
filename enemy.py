
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
        self.ships = self.placeShips()



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
                self.ammo -= 1



    def medium(self):
        while True:
            if self.potential_targets:
                move = self.potential_targets.pop(0)
            else:
                letter = random.choice('ABCDEFGHIJ')
                number = random.randint(1,10)
                move = f"{letter}{number}"
            result = self.shoot(move)
            if result == True:
                self.processHit(move)
                break
            if result == False:
                continue


    def processHit(self, coordinate):
        letter, col = coordinate[0], coordinate[1:]
        col = int(col) 
        xy = self.player_board.coordinate_map[coordinate]
        if self.player_board.shot_board[xy[0]][xy[1]] == "X" or self.player_board.shot_board[xy[0]][xy[1]] == "#":
            if letter > 'A':
                adjacent_move = f"{chr(ord(letter) - 1)}{col}"
                if self.isValidTarget(adjacent_move):
                    self.potential_targets.append(adjacent_move)
            if letter < 'J':
                adjacent_move = f"{chr(ord(letter) + 1)}{col}"
                if self.isValidTarget(adjacent_move):
                    self.potential_targets.append(adjacent_move)
            if col > 1:
                adjacent_move = f"{letter}{col - 1}"
                if self.isValidTarget(adjacent_move):
                    self.potential_targets.append(adjacent_move)
            if col < 10:
                adjacent_move = f"{letter}{col + 1}"
                if self.isValidTarget(adjacent_move):
                    self.potential_targets.append(adjacent_move)

        if self.player_board.shot_board[xy[0]][xy[1]] == "#":
            self.potential_targets = []



    def isValidTarget(self, move):
        """
        Check if the move is a valid target (i.e., it hasn't been shot yet).
        """
        xy = self.player_board.coordinate_map[move]
        if self.player_board.shot_board[xy[0]][xy[1]] is None:  # Not already shot
            return True
        return False




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
