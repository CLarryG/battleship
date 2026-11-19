import json
import random

from components import place_battleships_custom,place_battleships_random, place_battleships_simple

def create_battleships(filename="battleships.txt"):
    """Load battleships data from a JSON file.

    Parameters:
    - filename (str): The path to the JSON file containing battleships data.

    Returns:
    dict: A dictionary representing battleships data.
    """
    try:
        with open(filename, "r") as file:
            battleships_data = json.load(file)
        return battleships_data
    except FileNotFoundError:
        print(f"File '{filename}' not found. Please check the file path.")
        # Handle the error or return a default value

def place_battleships(board, ships, algorithm="simple"):
    """Place battleships on a board using a specified algorithm.

    Parameters:
    - board (list): A list of lists representing the game board.
    - ships (dict): A dictionary containing ship names as keys and their positions as values.
    - algorithm (str): Optional argument specifying the placement algorithm.
                      Default is "simple," other options are "custom" and "random."

    Returns:
    None
    """
    if algorithm == "simple":
        place_battleships_simple(board, ships)
    elif algorithm == "random":
        place_battleships_random(board, ships)
    elif algorithm == "custom":
        place_battleships_custom(board, ships)

def initialize_board(size=10):
    """Initialize a game board with a default size.

    Parameters:
    - size (int): The size of the square game board.

    Returns:
    list: A 2D list representing the initialized game board.
    """
    return [[None] * size for _ in range(size)]