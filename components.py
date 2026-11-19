"""module level docstring"""
import json
import random

def initialise_board(size=10):
    """Initialize a battleship game board.

    Parameters:
    - size (int): The size of the square game board (default is 10).

    Returns:
    list: A list of lists representing the game board.
    """
    return [[None] * size for _ in range(size)]

def create_battleships(filename="battleships.txt"):
    """Create battleships data from a file.

    The file should contain a JSON object where each key is a ship name, and the
    corresponding value is a list of positions represented as [x, y, orientation].

    Parameters:
    - filename (str): The path to the file containing battleships data (default is "battleships.txt").

    Returns:
    dict: A dictionary containing ship names as keys and their positions as values.
    """
    try:
        with open(filename, "r") as file:
            battleships_data = json.load(file)

        # Validate the structure of the battleships_data
        if not all(isinstance(battleships_data.get(ship), list) for ship in battleships_data):
            raise ValueError("Invalid battleships data structure")

        return battleships_data
    except FileNotFoundError:
        print(f"File '{filename}' not found. Please check the file path.")
        # Handle the error or return a default value


def place_battleships(board, ships, algorithm="simple"):
    """Place battleships on board using algorithm. 
  
    board is expected as a list of lists that represents the grid, ships are 
    expected to be passed as a dictionary with the ship name as a key and the start coordinates end coordinates and orientation as values.
    :board: list of lists 
    :ships: dictionary
    :algorithm: optional argument with default value simple and options of custom and random"""
    if algorithm == "simple":
        place_battleships_simple(board, ships)
    elif algorithm == "random":
        place_battleships_random(board, ships)
    elif algorithm == "custom":
        place_battleships_custom(board, ships)


def place_battleships_simple(board, ships):
    """Place battleships on the board using a simple algorithm.

    Parameters:
    - board (list): A list of lists representing the game board.
    - ships (dict): A dictionary containing ship names as keys and their sizes as values.

    Returns:
    None
    """
    for ship_name, ship_size in ships.items():
        for i in range(ship_size):
            board[i][0] = ship_name

def place_battleships_random(board, ships):
    """Place battleships on the board using a random algorithm.

    Parameters:
    - board (list): A list of lists representing the game board.
    - ships (dict): A dictionary containing ship names as keys and their sizes as values.

    Returns:
    None
    """
    for ship_name, ship_size in ships.items():
        placed = False
        while not placed:
            direction = random.choice(["horizontal", "vertical"])
            if direction == "horizontal":
                x = random.randint(0, len(board) - 1)
                y = random.randint(0, len(board[0]) - ship_size)
                if all(board[x][y + i] is None for i in range(ship_size)):
                    for i in range(ship_size):
                        board[x][y + i] = ship_name
                    placed = True
            else:
                x = random.randint(0, len(board) - ship_size)
                y = random.randint(0, len(board[0]) - 1)
                if all(board[x + i][y] is None for i in range(ship_size)):
                    for i in range(ship_size):
                        board[x + i][y] = ship_name
                    placed = True

def place_battleships_custom(board, ships, placement_file="placement.json"):
    """Place battleships on the board using custom positions from a file.

    Parameters:
    - board (list): A list of lists representing the game board.
    - ships (dict): A dictionary containing ship names as keys and their sizes as values.
    - placement_file (str): The path to a JSON file containing custom ship placements.

    Returns:
    None
    """
    with open(placement_file, "r") as file:
        placement_data = json.load(file)

    for ship_name, positions in placement_data.items():
        for position in positions:
            if len(position) == 2:
                x, y = position
                board[x][y] = ship_name
            else:
                print(f"Illegal position format: {position}. Skipping...")

if __name__ == "__main__":
    # Test the components
    size = 10
    board = initialise_board(size)
    ships = create_battleships()
    place_battleships(board, ships, algorithm="simple")
    print(board)

def cli_coordinates_input():
    """Prompt the user to enter coordinates for an attack.

    Returns:
    tuple: A tuple containing X and Y coordinates entered by the user.
    """
    while True:
        try:
            input_str = input("Enter coordinates for an attack (e.g., 1,4): ")
            x, y = map(int, input_str.split(','))
            return x, y
        except ValueError:
            print("Invalid input. Please enter valid coordinates.")