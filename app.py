from flask import Flask, render_template, redirect, url_for
import subprocess
import sys
import threading

app = Flask(__name__)

@app.route('/')
def name():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/Game')
def Game():
    return render_template('Game.html')

@app.route('/play/<game_name>')
def play_game(game_name):
    try:
        if game_name == 'blockdodge':
            threading.Thread(target=start_blockdodge).start()
        elif game_name == 'maze':
            threading.Thread(target=start_maze).start()
        elif game_name == 'snake':
            threading.Thread(target=start_snake).start()
        elif game_name == 'car':
            threading.Thread(target=start_car).start()
        
        # Redirect to game stream page after starting the game
        return redirect(url_for('game_stream', game_name=game_name))
    except Exception as e:
        return f"An error occurred while trying to start the game: {e}"

def start_blockdodge():
    subprocess.run([sys.executable, "game.py"])

def start_maze():
    subprocess.run([sys.executable, "maze.py"])

def start_snake():
    subprocess.run([sys.executable, "Snake.py"])

def start_car():
    subprocess.run([sys.executable, "game2.py"])

@app.route('/game_stream/<game_name>')
def game_stream(game_name):
    return render_template('game_stream.html', game_name=game_name)

@app.route('/stop_game')
def stop_game():
    # Stop game logic here, like closing game windows or killing game processes
    # You can kill the game process if needed using subprocess or other techniques
    # Example: subprocess.Popen("taskkill /F /IM game.exe")
    return redirect(url_for('Game'))  # Redirect back to the home page

if __name__ == '__main__':
    app.run(debug=True)
