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

        self.p1_name = input("Enter Player 1's name: ")
        self.p2_name = input("Enter Player 2's name: ")

        self.num_ships = int(input("Enter the number of ships for each player: "))

        print(f"{self.p1_name}, it's time to place your ships!")
        self.populateBoard(self.p1_board)
        print("\n" * 100)
        
        print(f"{self.p2_name}, it's time to place your ships!")
        self.populateBoard(self.p2_board)
        print("\n" * 100)

        current_player = 1

        while True:

            if current_player == 1:
                print(f"{self.p1_name}'s turn!")

                print("Your board:", '\n')
                self.p1_board.showBoard()
                print("\n" + "Opponent's board:", '\n')
                self.p2_board.showBoardForOpponent()
                
                self.fireShot(self.p2_board)

                if self.p2_board.gameOver():
                    print(f"{self.p1_name} wins!")
                    break

                current_player = 2

            else:
                print(f"{self.p2_name}'s turn!", '\n')

                print("Your board:", '\n')
                self.p2_board.showBoard()
                print("\n" + "Opponent's board:", '\n')
                self.p1_board.showBoardForOpponent()

                self.fireShot(self.p1_board)

                if self.p1_board.gameOver():
                    print(f"{self.p2_name} wins!")
                    break

                current_player = 1
            
            print()
            input("Press Enter to finish your turn...")
            print("\n" * 100)
            input("Press Enter to start your turn...")
            print("\n" * 100)


    def run(self):  # called by driver script to run the game
        self.playGame()
