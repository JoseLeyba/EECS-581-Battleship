from board import Board 
from ship import Ship 

class Battleship:
    def __init__(self):
        self.p1_board = Board()  # Player 1's board
        self.p2_board = Board()  # Player 2's board 
        self.p1_name = ''  # Player 1's name 
        self.p2_name = ''  # Player 2's name
        self.num_ships = 0  # number of ships each player gets 

    def populateBoard(self, board):  # creates the ships and prompts user for placement coordinates 
        pass

    def fireShot(self, board):  # prompts user for coordinate and fires shot at opponents board
        pass

    def playGame(self):  # handles turn taking and prompting users for input
        pass

    def run(self):  # called by driver script to run the game
        self.playGame()
