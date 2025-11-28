from flask import Flask, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route('/run/<path:game>')
def run_game(game):
    """
    game can be:
    - 'game1.py'
    - 'gridart/gridart/GridArt.py'
    """

    # make sure the file actually exists
    if not os.path.exists(game):
        return f"Error: '{game}' not found on server."

    # run the game
    subprocess.Popen(["python", game])

    return f"Launching {game} on your computer!"

if __name__ == '__main__':
    app.run(debug=True)