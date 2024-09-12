''' This class represents a ship placed on a battleship board '''
class Ship:
    def __init__(self, length):
        self.length = length  # single integer 1-5
        self.coordinates = []  # list of coordinates; ex: ['A1', 'A2', 'A3']
        self.hits = [False] * length  # a bool for each coordinate representing a hit

    def addCoordinates(self, coordintates):  # populate self.coordinates based on start and end positions
        self.coordinates = coordintates

    def addHit(self, coordinate):  # called by the board if a ship is hit; should update bool in hits list
        for i in self.coordinates:
            if i == coordinate:
                self.hits[self.coordinates.index(i)] = True

    def isSunk(self):  # returns true if all coordinates of a ship have been hit 
        return all(i == True for i in self.hits)
    
