
from board import Board 
from ship import Ship 
from enemy import Enemy
class Battleship:
    def __init__(self):
        self.p1_board = Board()  # Player 1's board
        self.p2_board = Board()  # Player 2's board 
        self.AI = None #AI's
        self.p1_name = ''  # Player 1's name 
        self.p2_name = ''  # Player 2's name
        self.num_ships = 0  # number of ships each player gets 
        self.choice = 0 #user's choice if they want to use AI or multiplayer
        self.difficulty = 0 #difficulty of the AI opponent

    def populateBoard(self, board):  # creates the ships and prompts user for placement coordinates 
        for ship_size in range(1, self.num_ships + 1):
            # create a new ship with the appropriate size
            ship = Ship(ship_size)

            while True:
                # asks user for start and end coordinates to place the ship
                start = input(f"Enter the starting coordinate for your {ship_size}-length ship (e.g. A1): ").upper()
                end = input(f"Enter the ending coordinate for your {ship_size}-length ship (e.g. A{ship_size}): ").upper()

                # try and see if the ship can be placed on the board
                if board.placeShip(ship, start, end):
                    board.ships.append(ship)  # add the ship to the board's ship list if placed successfully
                    board.showBoard()  # show the board after each successful placement
                    break
                else:
                    # if unsuccessful, ask for new coordinates
                    print("Invalid placement. Please try again.")

    def fireShot(self, board):  # prompts user for coordinate and fires shot at opponent's board
        while True:
            # asks the player for a coordinate to fire a shot
            print()
            coordinate = input(f"Enter coordinates to fire (e.g., A1): ").upper()

            # fire the shot and check if it's successful
            if board.fireShot(coordinate):
                # show upadted board after the successful shot
                print()
                board.showBoardForOpponent()
                print()
                break
            else:
                # if shot is invalid or has already been fired, ask for a new coordinate
                print("Invalid shot or already fired at this coordinate. Try again")

    def playGame(self):  # handles turn taking and prompting users for input
        print("Welcome to the game!")
        print("1. Multiplayer")
        print("2. Play against AI opponent")
        while True:
            i = input("Enter a choice: ")
            if i.isdigit() == True:
                i = int(i)
                if i == 1 or i == 2:
                    # Get number of ships for each player
                    self.choice = i
                    break
            else:
                print("Invalid Input")
        if self.choice == 2:
            print("Choose difficulty level")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            while True:
                i = input("Enter a choice: ")
                if i.isdigit() == True:
                    i = int(i)
                    if i >= 1 and i <= 3 :
                        # Get number of ships for each player
                        self.difficulty = i
                        break
                else:
                    print("Invalid Input")
        if self.choice == 1:
            # Get player names
            self.p1_name = input("Enter Player 1's name: ")
            self.p2_name = input("Enter Player 2's name: ")
        else:
            self.p1_name = input("Enter Player's name: ")
            self.p2_name = 'AI Opponent'
        while True:
            i = input("Enter the number of ships for each player: ")
            if i.isdigit() == True:
                i = int(i)
                if i >= 1 and i <= 5:
                    # Get number of ships for each player
                    self.num_ships = i
                    break
            else:
                print("Invalid Input")
        
        # Player 1 places their ships
        print(f"{self.p1_name}, it's time to place your ships!")
        self.populateBoard(self.p1_board)
        print("\n" * 100)  # Clear screen
        if self.choice == 1:
            # Player 2 places their ships
            print(f"{self.p2_name}, it's time to place your ships!")
            self.populateBoard(self.p2_board)
            print("\n" * 100)  # Clear screen
        else:
            self.AI = Enemy(self.num_ships, self.p1_board)
        current_player = 1  # Start with Player 1
        if self.choice == 1:
            # Main game loop
            while True:
                if current_player == 1:
                    print(f"{self.p1_name}'s turn!")

                    # Display boards for Player 1
                    print("Your board:", '\n')
                    self.p1_board.showBoard()
                    print("\n" + "Opponent's board:", '\n')
                    self.p2_board.showBoardForOpponent()
                    
                    # Player 1 takes a shot on player 2's board
                    self.fireShot(self.p2_board)

                    # Check if Player 1 has won
                    if self.p2_board.gameOver():
                        print(f"{self.p1_name} wins!")
                        break

                    current_player = 2  # Switch to Player 2

                else:
                    print(f"{self.p2_name}'s turn!", '\n')

                    # Display boards for Player 2
                    print("Your board:", '\n')
                    self.p2_board.showBoard()
                    print("\n" + "Opponent's board:", '\n')
                    self.p1_board.showBoardForOpponent()

                    # Player 2 takes a shot on player 1's board
                    self.fireShot(self.p1_board)

                    # Check if Player 2 has won
                    if self.p1_board.gameOver():
                        print(f"{self.p2_name} wins!")
                        break

                    current_player = 1  # Switch back to Player 1
                
                # End of turn actions
                print()
                input("Press Enter to finish your turn...")
                print("\n" * 100)  # Clear screen
                input("Press Enter to start your turn...")
                print("\n" * 100)  # Clear screen
        else:
            while True:
                if current_player == 1:
                    print(f"{self.p1_name}'s turn!")

                    # Display boards for Player 1
                    print("Your board:", '\n')
                    self.p1_board.showBoard()
                    print("\n" + "Opponent's board:", '\n')
                    self.AI.AIboard.showBoardForOpponent()
                    
                    # Player 1 takes a shot on player 2's board
                    self.fireShot(self.AI.AIboard)

                    # Check if Player 1 has won
                    if self.AI.gameOver():
                        print(f"{self.p1_name} wins!")
                        break

                    current_player = 2  # Switch to Player 2
                    current_player = 2
                else:
                    if self.difficulty == 1:
                        self.AI.easy()
                    elif self.difficulty == 2:
                        self.AI.medium()
                    else:
                        self.AI.hard()
                    # Check if Player 2 has won
                    if self.p1_board.gameOver():
                        print(f"{self.p2_name} wins!")
                        break
                    current_player = 1

    def run(self):  # called by driver script to run the game
        self.playGame()
