'''
Authors: Alexandra, Sophia, Eli, Jose, and Riley
Other Authors: Group 4
Date: 09/09/2024
Last modified: 09/29/2024
Purpose: Battleship Class
'''
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
        self.p1_ammo = 1
        self.p2_ammo = 1

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

    def fireShot(self, board, player):
        # Set player-specific variables
        if player == "player1":
            ammo = self.p1_ammo
        elif player == "player2":
            ammo = self.p2_ammo
        else:
            print("Invalid player")
            return

        # Ensure the player has ammo
        if ammo <= 0:
            print("No ammo left!")
            return

        # Main loop to prompt the player for coordinates until a valid shot is fired
        while True:
            print()

            # Ask if the player wants to use a special shot
            special = input("Enter 1 if you want to use a special shot, otherwise press Enter: ")

            # Ask for the coordinates
            coordinate = input(f"Enter coordinates to fire (e.g., A1): ").upper()
            if len(coordinate) < 2 or not coordinate[0].isalpha() or not coordinate[1:].isdigit():
                print("Invalid input. Please enter a valid coordinate (e.g., A1).")
                continue
            # Extract the letter (column) and number (row) from the coordinate
            letter = coordinate[0]  # Assuming the first part is a letter
            number = int(coordinate[1:])  # Assuming the second part is the number

            # Attempt to fire the shot at the given coordinate
            if board.fireShot(coordinate):
                if special == "1" and ammo > 0:
                    # Handle the special shot if ammo is available
                    letters = ['A','B','C','D','E','F','G','H','I','J']
                    letterIndex = letters.index(letter)
                    downNumber = number + 1
                    upNumber = number - 1
                    rightLetter = None
                    leftLetter = None
                    
                    # Calculate adjacent coordinates
                    if letterIndex + 1 < len(letters):
                        rightLetter = letters[letterIndex + 1]
                    if letterIndex - 1 >= 0:
                        leftLetter = letters[letterIndex - 1]
                    
                    coordinatesLeft = f"{leftLetter}{number}" if leftLetter else None
                    coordinatesRight = f"{rightLetter}{number}" if rightLetter else None
                    coordinatesDown = f"{letter}{downNumber}"
                    coordinatesUp = f"{letter}{upNumber}"

                    # Fire shots at adjacent coordinates
                    board.fireShot(coordinatesDown)
                    board.fireShot(coordinatesUp)
                    if coordinatesLeft:
                        board.fireShot(coordinatesLeft)
                    if coordinatesRight:
                        board.fireShot(coordinatesRight)

                    # Deduct ammo for special shot
                    ammo -= 1
                    print("Special shot fired!")
                else:
                    print("Regular shot fired!")

                # Show the updated board
                print()
                board.showBoardForOpponent()
                print()
                
                # Deduct ammo for the player after a successful shot
                if player == "player1":
                    self.p1_ammo = ammo
                else:
                    self.p2_ammo = ammo
                
                break
            else:
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
                    self.fireShot(self.p2_board,"player1")

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
                    self.fireShot(self.p1_board,"player2")

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
                    self.fireShot(self.AI.AIboard,"player1")

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
