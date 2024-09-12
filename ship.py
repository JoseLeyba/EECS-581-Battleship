''' This class represents a ship placed on a battleship board '''
class Ship:
    def __init__(self, length):
        self.length = length  # single integer 1-5
        self.coordinates = []  # list of coordinates; ex: ['A1', 'A2', 'A3']
        self.hits = [False] * length  # a bool for each coordinate representing a hit

    def addCoordinates(self, start, end):  # populate self.coordinates based on start and end positions
        letter_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        self.coordinates.append(start)
        if self.length == 2:
            self.coordinates.append(end)
        else:
            start_list = list(start)
            end_list = list(end)
            if len(end_list) == 3:
                end_list.pop()
                end_list[1] = str(end_list[1]) + str(end_list[2]) 
            if start_list[0] == end_list[0]:
                for i in range(int(end_list[1]) - int(start_list[1])):
                    self.coordinates.append(str(start_list[0]) + str(i + int(start_list[1]) + 1))
            else:
                i = 0
                while start_list[0] != letter_list[i]:
                    i += 1
                while end_list[0] != letter_list[i + 1]:
                    self.coordinates.append(str(letter_list[i + 1]) + str(start_list[1]))
                    i += 1
                self.coordinates.append(end)

    def addHit(self, coordinate):  # called by the board if a ship is hit; should update bool in hits list
        for i in self.coordinates:
            if i == coordinate:
                self.hits[self.coordinates.index(i)] = True

    def isSunk(self):  # returns true if all coordinates of a ship have been hit 
        return all(i == True for i in self.hits)
    
