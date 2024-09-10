from board import Board
from ship import Ship

if __name__ == "__main__":
    board = Board()  # create a game instance
    ship = Ship(5)
    
    print(board.placeShip(ship, "A1", "A5"))
    print(board.placeShip(ship, "A1", "B1"))
    print(board.placeShip(ship, "A1", "B2"))
