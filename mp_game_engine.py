import random
from components import initialise_board, create_battleships, place_battleships, cli_coordinates_input
from game_engine import attack
players = {}

def generate_attack(board_size):
    """
    Generate random attack coordinates within the board size.

    Parameters:
    - board_size (int): The size of the game board.

    Returns:
    - tuple: A tuple containing (x, y) coordinates for the attack.
    """
    x = random.randint(0, board_size - 1)
    y = random.randint(0, board_size - 1)
    return x, y

def ai_opponent_game_loop():
    """
    Execute the game loop for a single player against an AI opponent.

    The game includes alternating turns between the user and AI opponent, with attacks
    and board updates until one of the players sinks all the battleships.

    """
    print("Welcome to Battleships!")

    user_player = "User"
    ai_opponent_player = "AI Opponent"

    users_board = initialise_board()
    ai_opponent_board = initialise_board()

    users_ships = create_battleships()
    ai_opponent_ships = create_battleships()

    place_battleships(users_board, users_ships, algorithm="custom")
    place_battleships(ai_opponent_board, ai_opponent_ships, algorithm="random")

    while any(ship_size > 0 for ship_size in users_ships.values()) and any(ship_size > 0 for ship_size in ai_opponent_ships.values()):
        print("\nUser's Turn:")
        print_board(users_board)
        user_coordinates = cli_coordinates_input()
        user_result = attack(user_coordinates, ai_opponent_board, ai_opponent_ships)
        print("Hit!" if user_result else "Miss!")

        if all(ship_size == 0 for ship_size in ai_opponent_ships.values()):
            print("Congratulations! You've sunk all of AI Opponent's battleships. You win!")
            break

        print("\nAI Opponent's Turn:")
        ai_opponent_coordinates = generate_attack(len(users_board))
        ai_opponent_result = attack(ai_opponent_coordinates, users_board, users_ships)
        print_board(users_board)
        print("AI Opponent Hit!" if ai_opponent_result else "AI Opponent Miss!")

        if all(ship_size == 0 for ship_size in users_ships.values()):
            print("Game over! AI Opponent has sunk all your battleships. You lose.")
            break

    print("Game over!")

def print_board(board):
    """
    Print the current state of the game board.

    Parameters:
    - board (list of lists): The game board.
    """
    for row in board:
        print(" ".join(str(cell) if cell is not None else '.' for cell in row))
    print()
