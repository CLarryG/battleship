#main.py
from flask import Flask, render_template, request,jsonify
from components import initialise_board, create_battleships, place_battleships
from mp_game_engine import generate_attack
from game_engine import attack

app = Flask(__name__)

board = [[None,None,None,None,None],
         [None,None,None,None,None],
         ["SHIP1","SHIP1","SHIP1","SHIP1", None],
         [None,None,None,None,"SHIP2"],
         [None,None,None,None,"SHIP2"]]

# Initialize the user's board and ships
initial_user_board = initialise_board()
initial_user_ships = create_battleships()
place_battleships(initial_user_board, initial_user_ships, algorithm="custom")

# Initialize the AI opponent's board and ships
initial_ai_opponent_board = initialise_board()
initial_ai_opponent_ships = create_battleships()
place_battleships(initial_ai_opponent_board, initial_ai_opponent_ships, algorithm="random")

@app.route('/', methods=['GET'])
def root():
    """Render the main page."""
    return render_template("main.html", player_board=board)


@app.route('/')
def battleships_placement():
    """Render the Battleships Placement page."""
    return render_template('placement.html')

@app.route('/placement')
def placement_interface():
    """Render the placement interface template."""
    # You can customize the template name and pass any additional context data
    return render_template('placement.html')
    ships= {"Battleship": 5,
            "Cruiser": 3,-
            "Submarine": 2,
            }
    board_size = 10
    if request.method =="GET":
        return render_template("placement.html", ships=ships, board_size=board_size)
    if request.method =="POST":
        data = request.get_json()
        board = [[]]
        print(data)
        return jsonify({"message": "success"})


@app.route('/attack', methods=['GET'])
def attack():
    """Handle the attack."""
    if request.args:
        x= request.args.get('x')
        y= request.args.get('y')
        print(x,y)
        
        return jsonify({"hit": True, "AI_Turn":(1,2)})
    

@app.route('/gameplay', methods=['GET', 'POST'])
def gameplay():
    """Handle the game logic for the Gameplay page."""
    global initial_user_board, initial_user_ships, initial_ai_opponent_board, initial_ai_opponent_ships

    if request.method == 'POST':
        # User's turn
        user_coordinates = (int(request.form['x']), int(request.form['y']))
        user_result = attack(user_coordinates, initial_ai_opponent_board, initial_ai_opponent_ships)
        print("User Hit!" if user_result else "User Miss!")

        # Check if the user has won
        if all(ship_size == 0 for ship_size in initial_ai_opponent_ships.values()):
            return render_template('game_over.html', message="Congratulations! You've sunk all of AI Opponent's battleships. You win!")

        # AI Opponent's turn
        ai_opponent_coordinates = generate_attack(len(initial_user_board))
        ai_opponent_result = attack(ai_opponent_coordinates, initial_user_board, initial_user_ships)
        print("AI Opponent Hit!" if ai_opponent_result else "AI Opponent Miss!")

        # Check if the AI opponent has won
        if all(ship_size == 0 for ship_size in initial_user_ships.values()):
            return render_template('game_over.html', message="Game over! AI Opponent has sunk all your battleships. You lose.")

    return render_template('gameplay.html')

@app.route('/attack', methods=['GET'])
def process_attack():
    """Process attack based on X and Y coordinates."""
    if request.method == 'GET':
        # Retrieve X and Y coordinates from the request
        x = request.args.get('x', type=int)
        y = request.args.get('y', type=int)

        # Your game logic to process the attack
        # ...

        # Dummy response for illustration purposes
        response_data = {
            'message': f'Attack processed at coordinates X={x}, Y={y}',
            'result': 'Hit'  # Replace this with your actual game result
        }

        # Respond to the request with JSON data
        return jsonify(response_data)

if __name__ == '__main__':
    app.template_folder = "templates"
    app.run()

