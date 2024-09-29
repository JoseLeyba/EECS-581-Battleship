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
        coordinates_list = []                                  # list that saves the coordinates of the player's ships 
        for ship in self.player_board.ships:                   # loop that scans the player's ship coordinates
            coordinates_list.extend(ship.coordinates)          # adds coordinates to coordinates_list

        for coord in coordinates_list:                         # loop looks at every coordinate in list 
            isValid = self.shoot(coord)                        # AI's shoot behavior that fires at coordinate
            if isValid:
                break  # Stop after a successful hit




    def shoot(self, coordinates):
        result = self.player_board.fireShotAI(coordinates)      #Call the fireShotAI method on the player's board to fire at the specified coordinate
        return result                                           #This function will return True or False depending on if the location is valid




    def placeShips(self): #Places the ships of the AI enemy
        #Sets the ship length to the number of ships enemy has
        shipLength = self.numofships
        #Possible directions for the ship to go
        directions = ["up", "down","left","right"]
        #Possible letters for the ship to be placed
        letters = ['A','B','C','D','E','F','G','H','I','J']

        #Loop that keeps going as long as the ship length is not 0
        while shipLength != 0:
            #sets placed to false
            placed = False
            #Creates a new ship with the current length
            ship = Ship(shipLength)
            #Loop until a ship has been placed
            while not placed:
                #randomly chooses a direction
                direction = random.choice(directions)
                #randomly chooses a letter in letters for the column
                startCol = random.choice(letters)
                #randomly chooses a number from 1 to 10 for the row
                startRow = random.randint(1,10)
                #length of the ship minus 1
                length = shipLength - 1

                #Checks if the direction is up
                if direction == "up":
                    #Calculates the end column and row for the ship
                    #sets endCol to startCol
                    endCol = startCol
                    #sets endRow to startRow - length
                    endRow = startRow - length
                    #checks if endRow is less than 1
                    if endRow < 1:
                        #if endRow is less then 1 it skips to the next iteration of the loop
                        continue

                #Checks if the direction is down
                elif direction == "down":
                    #Calculates the end column and row for the ship
                    #sets endCol to startCol
                    endCol = startCol
                    #sets endRow to startRow + length
                    endRow = startRow + length
                    #checks if endrow is greater than 10 
                    if endRow > 10:
                        #if endRow is greater than 10 it skips to the next iteration of the loop
                        continue

                #Checks if the direction is right
                elif direction == "right":
                    #finds the index of the starting column
                    letterIndex = letters.index(startCol)
                    #checks if the ending column is out of bounds
                    if letterIndex + length >= len(letters):
                        #if it is out of bounds it skips to the next iteration of the loop
                        continue
                    #Calculates the end column and row for the ship
                    #sets endCol to letters[letterIndex + length]
                    endCol = letters[letterIndex + length]
                    #sets endRow to startRow
                    endRow = startRow

                #Checks if the direction is left
                elif direction == "left":
                    #finds the index of the starting column
                    letterIndex = letters.index(startCol)
                    #checks if the ending column is out of bounds
                    if letterIndex - length < 0:
                        #if it is out of bounds it skips to the next iteration of the loop
                        continue
                    #Calculates the end column and row for the ship
                    #sets endCol to letters[letterIndex - length]
                    endCol = letters[letterIndex - length]
                    #sets endRow to startRow
                    endRow = startRow

                #sets the starting and ending coordinates for the ship
                #starting coordinates
                start = f"{startCol}{startRow}"
                #ending coordinates
                end = f"{endCol}{endRow}"
                #trys to place the ship on the board
                isValid = self.AIboard.placeShip(ship, start, end)
                #checks if the ship was successfully placed
                if isValid:
                    #Add the ship to the board's list of ships
                    self.AIboard.ships.append(ship)
                    #sets placed to True
                    placed = True
            #subtracts 1 from shipLength
            shipLength -= 1




    def gameOver(self):
        return self.AIboard.gameOver()
