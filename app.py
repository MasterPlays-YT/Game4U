from flask import Flask, render_template, redirect, url_for
import subprocess
import sys
import threading
import os

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
    game_script_path = os.path.join('Games', 'game.py')
    subprocess.run([sys.executable, game_script_path])

def start_maze():
    game_script_path2 = os.path.join('Games', 'maze.py')
    subprocess.run([sys.executable, game_script_path2])

def start_snake():
    game_script_path3 = os.path.join('Games', 'Snake.py')
    subprocess.run([sys.executable, game_script_path3])

def start_car():
    game_script_path4 = os.path.join('Games', 'game2.py')
    subprocess.run([sys.executable, game_script_path4])

@app.route('/game_stream/<game_name>')
def game_stream(game_name):
    return render_template('game_stream.html', game_name=game_name)


if __name__ == '__main__':
    app.run(debug=True)
