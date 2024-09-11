''' This class represents the board of a battleship player '''
class Board:
    def __init__(self):
        self.ships = []  # holds the ship objects placed on the board 
        self.ship_board = [[0] * 10 for _ in range(10)]  # records the ship locations on the board; initialized to 0
        self.shot_board = [[None] * 10 for _ in range(10)]  # records the opponents shots at the board; initialized to None
        self.coordinate_map = {  # maps the coordinates in string form to an index
            'A1': (0, 0), 'A2': (1, 0), 'A3': (2, 0), 'A4': (3, 0), 'A5': (4, 0),
            'A6': (5, 0), 'A7': (6, 0), 'A8': (7, 0), 'A9': (8, 0), 'A10': (9, 0),
            'B1': (0, 1), 'B2': (1, 1), 'B3': (2, 1), 'B4': (3, 1), 'B5': (4, 1),
            'B6': (5, 1), 'B7': (6, 1), 'B8': (7, 1), 'B9': (8, 1), 'B10': (9, 1),
            'C1': (0, 2), 'C2': (1, 2), 'C3': (2, 2), 'C4': (3, 2), 'C5': (4, 2),
            'C6': (5, 2), 'C7': (6, 2), 'C8': (7, 2), 'C9': (8, 2), 'C10': (9, 2),
            'D1': (0, 3), 'D2': (1, 3), 'D3': (2, 3), 'D4': (3, 3), 'D5': (4, 3),
            'D6': (5, 3), 'D7': (6, 3), 'D8': (7, 3), 'D9': (8, 3), 'D10': (9, 3),
            'E1': (0, 4), 'E2': (1, 4), 'E3': (2, 4), 'E4': (3, 4), 'E5': (4, 4),
            'E6': (5, 4), 'E7': (6, 4), 'E8': (7, 4), 'E9': (8, 4), 'E10': (9, 4),
            'F1': (0, 5), 'F2': (1, 5), 'F3': (2, 5), 'F4': (3, 5), 'F5': (4, 5),
            'F6': (5, 5), 'F7': (6, 5), 'F8': (7, 5), 'F9': (8, 5), 'F10': (9, 5),
            'G1': (0, 6), 'G2': (1, 6), 'G3': (2, 6), 'G4': (3, 6), 'G5': (4, 6),
            'G6': (5, 6), 'G7': (6, 6), 'G8': (7, 6), 'G9': (8, 6), 'G10': (9, 6),
            'H1': (0, 7), 'H2': (1, 7), 'H3': (2, 7), 'H4': (3, 7), 'H5': (4, 7),
            'H6': (5, 7), 'H7': (6, 7), 'H8': (7, 7), 'H9': (8, 7), 'H10': (9, 7),
            'I1': (0, 8), 'I2': (1, 8), 'I3': (2, 8), 'I4': (3, 8), 'I5': (4, 8),
            'I6': (5, 8), 'I7': (6, 8), 'I8': (7, 8), 'I9': (8, 8), 'I10': (9, 8),
            'J1': (0, 9), 'J2': (1, 9), 'J3': (2, 9), 'J4': (3, 9), 'J5': (4, 9),
            'J6': (5, 9), 'J7': (6, 9), 'J8': (7, 9), 'J9': (8, 9), 'J10': (9, 9),
        }
        self.key = [
            'Key:',
            '~ = water',
            'O = miss',
            'X = hit',
            '# = sunk',
            '1-5 = ships'
        ]

    def placeShip(self, ship, start, end):  # takes a ship object and attempts to place on board
        # Get coordinates
        coordinates = self.validateAndGetPlacement(ship, start, end)

        # Check if ship can be placed where specified
        if not coordinates:
            return False # return false if ship can not be placed on coordinates

        # Update ship board
        for coordinate in coordinates:
            xyCoordinate = self.coordinate_map[coordinate]
            self.ship_board[xyCoordinate[0]][xyCoordinate[1]] = ship.length

        # Add coordinates to ship
        ship.addCoordinates(start, end)

        # Return true if valid coordinates given
        return True

    def validateAndGetPlacement(self, ship, start, end):  # checks if a ship can be placed at given coordinates
        startLetter = start[:1]
        startNumber = int(start[1:])
        endLetter = end[:1]
        endNumber = int(end[1:])

        # Check if either coordinate is out of bounds
        if (start not in self.coordinate_map or end not in self.coordinate_map):
            return False

        # Stores the selected coordinates
        coordinates = []

        # Check if coordinates represent a row or a column
        if (startNumber==endNumber): # is a row
            # Get row coordinates including and inbetween start and end coordinates
            coordinates = [k for k, v in self.coordinate_map.items() if (int(k[1:])==startNumber and startLetter <= k[:1] <= endLetter)]
        elif (startLetter==endLetter): # is a column
            # Get column coordinates including and inbetween start and end coordinates
            coordinates = [k for k, v in self.coordinate_map.items() if (k.startswith(startLetter) and startNumber <= int(k[1:]) <= endNumber)]
        else:
            return False # Invalid placement

        # Check if ship length matches inputted coordinates
        if (len(coordinates) != ship.length):
            return False

        # Check if ship already in ship_board coordinates
        for ship in self.ships:
            for coordinate in coordinates:
                if (coordinate in ship.coordinates):
                    return False

        # Return valid placement
        return coordinates

    def fireShot(self, coordinate):  # fires an opponents shot on board; returns true if valid shot
        # Check if coordinate is out of bounds
        if (coordinate not in self.coordinate_map):
            return False

        # Get coordinates
        xyCoordinates = self.coordinate_map[coordinate]

        # Checks if shot has already been fired on coordinate
        if (self.shot_board[xyCoordinates[0]][xyCoordinates[1]] != None):
            return False

        # Record ship that was hit
        hitShip = None

        # Check if ship was hit and sunk
        for ship in self.ships:
            for shipCoordinate in ship.coordinates:
                if shipCoordinate == coordinate:
                    hitShip = ship
                    hitShip.addHit(coordinate)

        # Updates shotboard with correct character and print message if miss, hit, or sunk
        if (hitShip == None):
            # Update shot coordinate to miss
            self.shot_board[xyCoordinates[0]][xyCoordinates[1]] = "O"

            print("Shot has been missed")
        elif (not hitShip.isSunk()):
            # Update shot coordinate to hit
            self.shot_board[xyCoordinates[0]][xyCoordinates[1]] = "X"

            print("Ship has been hit!")
        else:
            # Update every position in ship to sunk
            for shipCoordinate in hitShip.coordinates:
                shipXYCoordinates = self.coordinate_map[shipCoordinate]
                self.shot_board[shipXYCoordinates[0]][shipXYCoordinates[1]] = "#"

            print("Ship has been sunk!")
        
        # Return true if shot successfully fired
        return True

    def gameOver(self):  # returns true if every ship has sunk 
        pass

    def showBoard(self):  # shows the player's ships and opponent's fire marks
        # retrieve the amount of ships remaining
        ships_remaining = sum([0 if ship.isSunk() else 1 for ship in self.ships])

        display_board = [  # combine the ship board and shot board
            [  # uses shot if exists for a spot; otherwise uses ship board
                self.shot_board[i][j] if self.shot_board[i][j] is not None else self.ship_board[i][j] 
                for j in range(len(self.ship_board[0]))
            ]
            for i in range(len(self.ship_board))
        ]

        display_board = [  # format the board to be displayed
            ['~' if char == 0 else char for char in row]  # replace empty spots with water
            for row in display_board
        ]

        print("     A B C D E F G H I J\n")  # print the column headers

        for row in range(0, len(display_board)):  
            rowstring = f'{str(row+1).rjust(2)}   '  # display the row number
            rowstring += f'{" ".join(map(str, display_board[row]))}'  # display the row contents
            if row < len(self.key): 
                rowstring += f'   {self.key[row]}'  # display the character keys
            elif row == 7:
                rowstring += "   Ships remaining:"  # display ships remaining header
            elif row == 8:
                rowstring += f'   {ships_remaining}/{len(self.ships)}'  # display the amount of ships remaining
            print(rowstring)  # print the row


    def showBoardForOpponent(self):  # shows the hits/misses to opponent    
        # retrieve the amount of ships remaining
        ships_remaining = sum([0 if ship.isSunk() else 1 for ship in self.ships])

        display_board = [  # format the board to be displayed
            ['~' if char == None else char for char in row]  # replace empty spots with water
            for row in self.shot_board
        ]

        print("     A B C D E F G H I J\n")  # print the column headers

        for row in range(0, len(display_board)):  # iterate throught rows in the board  
            rowstring = f'{str(row+1).rjust(2)}   '  # display the row number
            rowstring += f'{" ".join(map(str, display_board[row]))}'  # display the row contents
            if row < len(self.key) - 1:   
                rowstring += f'   {self.key[row]}'  # display the character keys
            elif row == 6:
                rowstring += "   Ships remaining:"  # display ships remaining header
            elif row == 7:
                rowstring += f'   {ships_remaining}/{len(self.ships)}'  # display the amount of ships remaining
            print(rowstring)  # print the row
