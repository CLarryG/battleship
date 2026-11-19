from board_functions import initialise_board, create_battleships, place_battleships

def attack(coordinates, board, battleships):
    """
    Process an attack at the specified coordinates on the board.

    Parameters:
    - coordinates (tuple): The (x, y) coordinates for the attack.
    - board (list of lists): The game board where the attack is made.
    - battleships (dict): Dictionary containing battleship names and their remaining sizes.

    Returns:
    - bool: True if the attack is a hit, False if it's a miss.
    """
    x, y = coordinates
    if board[x][y] is not None:
        battleship_hit(board, battleships, board[x][y])
        return True
    else:
        board[x][y] = "Miss"
        return False

def battleship_hit(board, battleships, ship_name):
    """
    Process a battleship hit, updating the board and battleships dictionary.

    Parameters:
    - board (list of lists): The game board.
    - battleships (dict): Dictionary containing battleship names and their remaining sizes.
    - ship_name (str): The name of the battleship that was hit.
    """
    for row in board:
        for i, cell in enumerate(row):
            if cell == ship_name:
                row[i] = "Hit"
                battleships[ship_name] -= 1
                if battleships[ship_name] == 0:
                    print(f"You sunk the {ship_name}!")

def cli_coordinates_input():
    """
    Get attack coordinates from the command line.

    Returns:
    - tuple: A tuple containing (x, y) coordinates for the attack.
    """
    while True:
        try:
            input_str = input("Enter coordinates for an attack (e.g., 1,4): ")
            x, y = map(int, input_str.split(','))
            return x, y
        except ValueError:
            print("Invalid input. Please enter valid coordinates.")

def simple_game_loop():
    """
    Execute a simple game loop for the Battleships game.
    """
    print("Welcome to Battleships!")

    board = initialise_board()
    ships = create_battleships()
    place_battleships(board, ships)

    while any(ship_size > 0 for ship_size in ships.values()):
        print_board(board)
        coordinates = cli_coordinates_input()
        result = attack(coordinates, board, ships)
        print("Hit!" if result else "Miss!")

    print("Game over! You sunk all the battleships.")

def print_board(board):
    """
    Print the current state of the game board.

    Parameters:
    - board (list of lists): The game board.
    """
    for row in board:
        print(" ".join(str(cell) if cell is not None else '.' for cell in row))
    print()

if __name__ == "__main__":
    simple_game_loop()