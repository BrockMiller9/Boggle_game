from flask import session, make_response
from flask import Flask, request, render_template, redirect, jsonify
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()


app = Flask(__name__)
app.config["SECRET_KEY"] = "4534gdghjk5d#$RGR^HDG"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/board')
def show_board():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    numplays = session.get('numplays', 0)

    return render_template('board.html', board=board, highscore=highscore, numplays=numplays)


@app.route('/check-word')
def check_word():
    """Take the word from the paramaters of our axios GET request and check it agaisnt the board
      we have saved in session"""
    word = request.args['word'].lower()
    board = session['board']
    response_string = boggle_game.check_valid_word(board, word)
    # this variable will return one of three strings - 'ok, not-a-word, not-on-board' depending.

    return jsonify({'response': response_string})


@app.route('/end-game', methods=['POST'])
def end_game():
    """update score with axios post request """
    score = request.json['score']
    # get current highscore
    highscore = session.get('highscore', 0)
    numplays = session.get('numplays', 0)
    # update session with score
    session['highscore'] = max(score, highscore)
    session["numplays"] = numplays + 1
    return 'game over'
