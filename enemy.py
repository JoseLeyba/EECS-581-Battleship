'''
Authors: Alexandra, Sophia, Eli, Jose, and Riley
Date: 09/22/2024
Last modified: 09/29/2024
Purpose: AI class
'''
import random
from board import Board
from ship import Ship

class Enemy:
    #When initializing we store all the following stuff to be used in their respective difficulty
    def __init__(self,numofships, player_board):
        self.numofships = numofships
        #Creates an AI board
        self.AIboard = Board()
        #For the AI special shot for easy
        self.ammo = 1
        #To use on medium to check for hits and hard to know where to shoot at
        self.player_board = player_board
        #These are all needed for medium, possible moves is a list of all available moves, hits are places where it has hit before, and potential targets will store the adjacent cells after a hit as a queue
        self.possible_moves = [f"{row}{col}" for row in "ABCDEFGHIJ" for col in range(1, 11)]
        self.hits = []
        #Used on medium to store adjacent spots after a hit
        self.potential_targets = []
        #Places the ships immediately when initializing
        self.ships = self.placeShips()



    def easy(self):
        isSpecialShot = random.randint(1,10)                                            #Randomly determine is the shot will be a special shot
        while True:
            letter = random.choice('ABCDEFGHIJ')                                        #Randomly selects a letter (A-J) for the coordinates
            number = random.randint(1,10)                                               #Randomly selects a number (1-10) for the coordinates
            coordinates = f"{letter}{number}"                                           #Combines the random letter and number to make the coordinate
            isValid = self.shoot(coordinates)                                           #Attempts to shoot at the player's board
            if isValid == True:                                                         #Leaves the while loop if the attempted shot was valid
                break
        if isSpecialShot == 5:                                                          #It'll be a special shot if the randomly selected number is 5
            if self.ammo > 0:                                                           #Checks if there is ammo for a special shot
                letters = ['A','B','C','D','E','F','G','H','I','J']                     #List of the possible letters
                letterIndex = letters.index(letter)                                     #Gets the index of the letter for the attempted shot 
                downNumber = number + 1                                                 #Gets the number for shot below 
                upNumber = number - 1                                                   #Gets the number for the shot above
                rightLetter = None                                                      #Sets the shot to the right as None initially
                leftLetter = None                                                       #Sets the shot to the left as None initially
                if letterIndex + 1 < len(letters):                                      #Checks if the right shot is in the bounds 
                    rightLetter = letters[letterIndex + 1]                              #If it is it gets the letter for the shot to the right
                if letterIndex - 1 >= 0:                                                #Checks if the lefts shot is in the bounds
                    leftLetter = letters[letterIndex - 1]                               #If it is it getsthe letter for the shot to the left
                coordinatesLeft = f"{leftLetter}{number}" if leftLetter else None       #Combines to get a coordinate for the left if the leftLetter is not None
                coordinatesRight = f"{rightLetter}{number}" if rightLetter else None    #Combines to get a coordinate for the right if the rightLetter is not None

                coordinatesDown = f"{letter}{downNumber}"                               #Combines to get the coordinate for the down
                coordinatesUp = f"{letter}{upNumber}"                                   #Combines to get the coordinate for the up

                self.shoot(coordinatesDown)                                             #Attempts to shot below
                self.shoot(coordinatesUp)                                               #Attempts to shot above
                if coordinatesLeft:                                                     #If there is a left coordinate then it'll attempt to shoot
                    self.shoot(coordinatesLeft)
                if coordinatesRight:                                                    #If there is a right coordinate it'll attempt to shoot
                    self.shoot(coordinatesRight)
                self.ammo -= 1                                                          #Subtracts ammo by 1



    #When the difficulty is medium, shoots randomly until hitting a ship and then it hits in adjacent spaces until a ship has been sunk
    def medium(self):
        #Loops until a successful shoot has been done
        while True:
            #If you hit a ship before and haven't sunk it then shooting on your adjacent spot is your next move
            if self.potential_targets:
                move = self.potential_targets.pop(0)
            #If not, then try shooting on a random position
            else:
                letter = random.choice('ABCDEFGHIJ')
                number = random.randint(1,10)
                move = f"{letter}{number}"
            result = self.shoot(move)
            #If shot was valid go to processHit
            if result == True:
                self.processHit(move)
                break
            #If not continue looping
            if result == False:
                continue

    #This is for the medium difficulty to see if he hit a ship or not
    def processHit(self, coordinate):
        #First store the shot coordinate in parts
        letter, col = coordinate[0], coordinate[1:]
        col = int(col) 
        #Gets the numerical value using the coordinate map dictionary
        xy = self.player_board.coordinate_map[coordinate]
        #If the board at that space is an X or a # then it was a hit
        if self.player_board.shot_board[xy[0]][xy[1]] == "X" or self.player_board.shot_board[xy[0]][xy[1]] == "#":
            #Will check on all adjacent spots if it is a valid target or not then append it to the list of the potential targets if it is
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
        #After that, if the hit sunk a ship then we reset the list to shoot randomly again
        if self.player_board.shot_board[xy[0]][xy[1]] == "#":
            self.potential_targets = []


    #Checks if the target is valid
    def isValidTarget(self, move):
        #Gets the numerical value using the coordinate map dictionary
        xy = self.player_board.coordinate_map[move]
        #Checks for the shot board if it hasn't been shot before, if it hasn't then return true
        if self.player_board.shot_board[xy[0]][xy[1]] is None:
            return True
        #Else return false
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
